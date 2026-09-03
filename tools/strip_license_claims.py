#!/usr/bin/env python3
"""Remove MCB's own licensing / insurance claims from the built site.

Owner decision 2026-09-01 (Doug): the HIC/CSL registration number will not be
published, so every claim that would require substantiation is removed.

KEPT ON PURPOSE:
  * educational copy explaining MA licensing to homeowners ("a HIC registration
    is required over $1,000", "verify the CSL at the DPS lookup") - it claims
    nothing about MCB and it is strong content.
  * copy about the CUSTOMER's insurance adjuster / insurer.

Replacements use claims needing no registration number: written contracts,
fixed-price quotes, permit handling, free estimates, locally owned.

Idempotent.  Usage: python3 tools/strip_license_claims.py [--dry-run]
"""
import glob, io, os, re, sys, collections

SITE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

R = [
# --- badges / footers -------------------------------------------------------
(r'\s*\|\s*Licensed Massachusetts HIC \+ CSL(?=\s*(?:&nbsp;|&middot;|<|\|))',''),
(r'MAVERICK CITY BUILDERS\s*Licensed General Contractor','MAVERICK CITY BUILDERS General Contractor'),
(r'Licensed General Contractor(?=\s*(?:&middot;|·|<|\|))','General Contractor'),
(r'Licensed HIC\s*(?:&amp;|&)\s*CSL\s*&mdash;\s*Fully insured\s*&mdash;\s*',''),
(r'Licensed HIC\s*(?:&amp;|&)\s*CSL\s*(?:·|&middot;)\s*Fully insured\s*(?:·|&middot;)\s*',''),
(r'Fully Licensed\s*(?:&amp;|&)\s*Insured in Massachusetts','Written Contracts on Every Project'),
(r'Fully licensed\s*(?:&amp;|&)\s*insured in Massachusetts','Written contracts on every project'),
# --- MCB-as-subject sentences ----------------------------------------------
(r'\s*Maverick City Builders carries a Massachusetts Home Improvement Contractor \(HIC\) registration,?\s*(?:and\s*)?a?\s*Construction Supervisor License \(CSL\),?\s*(?:and|plus)\s*full general liability (?:plus|and) workers compensation insurance\.',
 ' Maverick City Builders works to a written contract with a fixed price agreed before any work begins.'),
(r'\s*MCB is a fully licensed Massachusetts Home Improvement Contractor and Construction Supervisor License holder, fully insured with general liability and workers compensation coverage\.',
 ' MCB works to a written contract with a fixed price agreed before any work begins.'),
(r'\s*Maverick City Builders operates as a fully licensed Massachusetts Home Improvement Contractor \(HIC\) and Construction Supervisor License \(CSL\) holder\.',
 ' Maverick City Builders works to a written contract on every project.'),
(r'\s*Carries comprehensive general liability insurance and workers compensation coverage\.',''),
(r'Maverick City Builders holds a Massachusetts Construction Supervisor Licence, pulls the permit, and schedules the inspections\.',
 'Maverick City Builders pulls the permit and schedules the inspections.'),
(r'[Ww]e hold a (?:<strong[^>]*>)?Massachusetts Construction Supervisor Licence(?:</strong>)?\s*,\s*so the permit gets pulled properly rather than',
 'We pull the permit properly rather than leaving it'),
(r'\s*MCB has the licensing and experience to navigate both contexts\.',' MCB has the experience to navigate both contexts.'),
(r'\s*Is Maverick City Builders licensed\?','Does Maverick City Builders work to a written contract?'),
# --- "we are fully licensed ... HIC and CSL" family --------------------------
(r'\s*—?\s*we are fully licensed Massachusetts HIC and CSL(?: for all(?: of these)? communities(?: we serve)?)?(?: and pull permits from each town(?:&#x27;|\')?s building department)?\.',
 ' — and we pull permits from each town’s building department.'),
(r'\s*We are fully licensed Massachusetts HIC and CSL(?: for all communities we serve)?\.',''),
(r'\s*We are fully licensed as a Massachusetts HIC and CSL\.',''),
(r'We are a fully licensed Massachusetts HIC and CSL contractor, and we pull the permits','We pull the permits'),
(r'We are a fully licensed Massachusetts HIC and CSL contractor, and every','Every'),
(r'We are a fully licensed Massachusetts Home Improvement Contractor and Construction Supervisor, and we carry full liability insurance\.',
 'We work to a written contract with a fixed price agreed before any work begins.'),
(r'As a fully licensed Massachusetts Home Improvement Contractor and Construction Supervisor License holder, we pull','We pull'),
(r'As a licensed general contractor we run the whole job on a written contract with a fixed-price quote and HIC and CSL supervision\.',
 'We run the whole job on a written contract with a fixed-price quote.'),
(r',?\s*as a fully licensed Massachusetts Home Improvement Contractor \(HIC\) and Construction Supervisor License \(CSL\) holder',''),
(r',?\s*fully licensed Massachusetts Home Improvement Contractor and Construction Supervisor,\s*pulling','. We pull'),
(r'\s*is a (?:Lancaster-based, )?fully licensed Massachusetts HIC and CSL contractor','is a Lancaster-based general contractor'),
(r'\s*is a licensed Massachusetts HIC and CSL contractor','is a general contractor'),
(r'\s*is a licensed general contractor','is a general contractor'),
(r'\s*a licensed general contractor','a general contractor'),
(r'Lancaster-based,?\s*licensed MA contractor','Lancaster-based general contractor'),
(r'as a licensed general contractor','as a general contractor'),
# --- meta-description tails --------------------------------------------------
(r'\s*&mdash;\s*licensed HIC and CSL, written contracts','&mdash; written contracts'),
(r'\s*—\s*licensed,\s*insured,\s*written contracts',' — written contracts'),
(r'\s*—\s*licensed,\s*insured,\s*and\s*',' — '),
(r'\s*Licensed HIC and CSL\.\s*',' '),
(r'\s*Licensed and insured\.\s*',' '),
(r'\s*Licensed,? insured,? and local\.',' Locally owned and operated.'),
(r'\s*Fully licensed Massachusetts (?:HIC and CSL|Home Improvement Contractor and Construction Supervisor)[^.<]*\.',''),
(r'\s*Fully licensed MA contractor\.',''),
(r'\s*Licensed MA(?: HIC)? contractor\.',''),
(r'\s*Licensed MA\.',''),
(r'\s*Fully insured\s*(?:&amp;|&)\s*locally trusted\.',' Locally owned and operated.'),
(r'\s*Fully licensed\.',''),(r'\s*Fully insured\.',''),
(r'free estimates, honest pricing, fully licensed and insured','free estimates, honest pricing, written contracts'),
(r'Free estimates, honest pricing, fully licensed and insured','Free estimates, honest pricing, written contracts'),
# --- subcontractor licensing references (owner: remove all licence wording) --
(r'Our licensed electrician and plumber','Our electrician and plumber'),
(r'We coordinate licensed subcontractors','We coordinate subcontractors'),
(r'coordinates licensed plumbers and electricians','coordinates plumbers and electricians'),
(r'bring in licensed specialty trades','bring in specialty trades'),
(r',?\s*and licensed HIC and CSL supervision(?: from estimate to final walkthrough)?',''),
# --- final pass: remaining unique self-claims -------------------------------
(r'Maverick City Builders holds both HIC and CSL and serves','Maverick City Builders serves'),
(r'Maverick City Builders is fully licensed Massachusetts HIC and CSL, based in Lancaster','Maverick City Builders is based in Lancaster'),
(r'Maverick City Builders is a licensed Massachusetts general contractor','Maverick City Builders is a Massachusetts general contractor'),
(r'Is Maverick City Builders licensed and insured\?','Does Maverick City Builders work to a written contract?'),
(r'Maverick City Builders is a fully licensed Massachusetts Home Improvement Contractor \(HIC\) and Construction Supervisor License \(CSL\) holder, with general liability i',
 'Maverick City Builders works to a written contract on every project, with a fixed price agreed before work begins. Genera'),
(r'Maverick City Builders holds a Massachusetts Construction Supervisor Licence, pulls the permit, and prices it in writing\.',
 'Maverick City Builders pulls the permit and prices the work in writing.'),
(r'We are a licensed Massachusetts HIC and CSL general contractor, not an emergency extraction crew\.',
 'We are a Massachusetts general contractor, not an emergency extraction crew.'),
(r'is a licensed general contracting company','is a general contracting company'),
(r'plus the licensed subs we already work with','plus the subs we already work with'),
(r'brings in licensed ','brings in '),
(r'bringing in licensed ','bringing in '),
(r'Licensed plumbing and electrical subcontractors','Plumbing and electrical subcontractors'),
(r'the standard — licensed, permitted, fixed-price — is','the standard — permitted, fixed-price — is'),
(r'licensed, permitted, fixed-price','permitted, fixed-price'),
# --- /about credentials section: keep the 3-card design, swap the claims -----
(r'Fully Licensed\. Fully Insured\. Fully Accountable\.','Written Contracts. Permits Handled. Fully Accountable.'),
(r'>MA Home Improvement Contractor</h3>','>Written Contracts</h3>'),
(r'Fully licensed for residential remodeling across Massachusetts\.','A fixed price agreed in writing before any work begins.'),
(r'>Construction Supervisor License</h3>','>Permits Handled</h3>'),
(r'Authorized to pull permits and supervise construction projects statewide\.','We pull every required permit and meet the inspector at your town hall.'),
(r'>General Liability \+ Workers Comp</h3>','>Owner-Operator</h3>'),
(r'Fully insured for property and worker safety on every job site\.','Doug runs every job personally - you deal with the owner, not a call centre.'),
(r'>Fully Insured</h3>','>Local &amp; Accountable</h3>'),
(r'Comprehensive coverage for your peace of mind\.','A Worcester County owner-operator you can reach directly.'),
(r'Fully Licensed and Insured in Massachusetts','Written Contracts on Every Project'),
# --- remaining footer / meta / body self-claims ------------------------------
(r'\s*Fully licensed Massachusetts Home Improvement Contractor \(HIC\) and Construction Supervisor License \(CSL\)\.',''),
(r',\s*fully licensed Massachusetts HIC and CSL,',','),
(r'content="Licensed general contractor based in','content="General contractor based in'),
(r'>Licensed general contractor based in','>General contractor based in'),
(r'Licensed HIC and CSL, written contracts','Written contracts'),
(r'Licensed HIC and CSL,\s*',''),
(r'\bMassachusetts-licensed structural engineer','Massachusetts structural engineer'),
# --- meta-description list forms --------------------------------------------
(r'by a licensed,\s*insured Massachusetts general contractor','by a Massachusetts general contractor'),
(r'by a licensed Worcester County','by a Worcester County'),
(r'[Ll]icensed and insured,\s*serving','Serving'),
(r',\s*licensed and insured,',','),
(r'[Ll]icensed,\s*insured,\s*and permitted\.','Written contracts and permits handled.'),
(r'[Ll]icensed,\s*insured,\s*permitted\.','Written contracts, permits handled.'),
(r'[Ll]icensed,\s*insured,\s*and permitted','permitted'),
(r'[Ll]icensed,\s*insured,\s*permitted','permitted'),
(r'[Ll]icensed and insured\.','Written contracts on every project.'),
(r',\s*[Ll]icensed and insured',''),
(r'[Ll]icensed and insured',''),
(r'a licensed,\s*insured ','a '),
(r'a licensed ','a '),
(r'A licensed ','A '),
(r'\bfully licensed\b',''),(r'\bFully licensed\b',''),
(r'\bfully insured\b',''),(r'\bFully insured\b',''),
(r'\s*with licensed HIC and CSL supervision',''),
(r'[Ll]icensed HIC and CSL serving','Serving'),
(r'[Ll]icensed Massachusetts builder','Massachusetts builder'),
(r'[Ll]icensed general contractor','general contractor'),
(r'\bLicensed (?=Massachusetts|HIC|MA\b|general)',''),
(r'\blicensed (?=Massachusetts|HIC|MA\b|general)',''),
(r'\s*Licensed HIC and CSL\b',''),
(r'\s*licensed HIC and CSL\b',''),



(r'the city requires a licensed contractor with a tradesperson license and workers-comp on file to pull the permit, which is exactly what we do, so you never stand at that counter',
 'the city requires the permit to be pulled at the counter, which we handle, so you never stand there'),
]

TIDY=[(r'[ \t]{2,}',' '),(r'\s+\.','.'),(r'\.\s*\.','.'),(r',\s*,',','),(r',\s*\.','.'),
      (r'(?:&middot;|·)\s*(?:&middot;|·)','&middot;'),(r'\|\s*\|','|'),(r'>\s+<','><'),
      (r'\s+—\s*—\s*',' — '),(r'^\s*—\s*','')]

TERMS=re.compile(r'licen[sc]|insur|\bHIC\b|\bCSL\b',re.I)
SELF=re.compile(r"Maverick City Builders|\bMCB\b|\bWe \b|\bwe \b|\bour \b|\bOur \b")
SENT=re.compile(r'[^.<>"]{0,200}?(?:licen[sc]|insur|\bHIC\b|\bCSL\b)[^.<>"]{0,200}?[.\"]',re.I)
KEEP=re.compile(r'insurance (?:adjuster|company|documentation|requirements)|your insurance|mitigation company|insurance documentation',re.I)

def main():
    dry='--dry-run' in sys.argv; changed=0; resid=collections.Counter()
    for f in sorted(glob.glob(os.path.join(SITE,'**','*.html'),recursive=True)):
        if os.sep+'assets'+os.sep in f: continue
        s=io.open(f,encoding='utf-8',errors='replace',newline='').read(); o=s
        for p,rep in R: s=re.sub(p,rep,s)
        for p,rep in TIDY: s=re.sub(p,rep,s)
        if s!=o:
            changed+=1
            if not dry: io.open(f,'w',encoding='utf-8',newline='').write(s)
        for m in SENT.finditer(s):
            t=re.sub(r'\s+',' ',m.group(0)).strip()
            if SELF.search(t) and not KEEP.search(t) and len(t)<260: resid[t]+=1
    print(f'files changed: {changed}')
    print(f'remaining SELF-claims: {sum(resid.values())} in {len(resid)} sentences')
    for t,n in resid.most_common(30): print(f'  {n:3d}  {t[:165]}')

if __name__=='__main__': main()
