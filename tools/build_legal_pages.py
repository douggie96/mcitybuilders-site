#!/usr/bin/env python3
"""Build /terms, /accessibility and /cookie-policy from the privacy-policy shell.

Keeps the site's exact head, header, footer and typography by cloning
privacy-policy/index.html and swapping the <main> block plus the SEO tags.
Idempotent - re-running rewrites the same three pages.
"""
import io, os, re, sys

SITE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(SITE, 'privacy-policy', 'index.html')
BASE = 'https://mcitybuilders.com'
TODAY = 'September 1, 2026'

H1 = 'font-heading text-4xl md:text-5xl font-extrabold tracking-tight mb-4 text-white'
H2 = 'font-heading text-xl font-bold text-white mb-3'
P  = 'text-gray-300 leading-relaxed'
UL = 'text-gray-300 leading-relaxed list-disc pl-6 space-y-2'

def sec(n, title, *paras):
    body = ''.join(paras)
    return (f'<section class="mb-10"><h2 class="{H2}">{n}. {title}</h2>{body}</section>')

def p(t):  return f'<p class="{P} mb-4">{t}</p>'
def ul(items): return f'<ul class="{UL} mb-4">' + ''.join(f'<li>{i}</li>' for i in items) + '</ul>'

CONTACT = ('Maverick City Builders, Lancaster, MA 01523 &middot; '
           '<a href="mailto:douglas@mcitybuilders.com" style="color:#ff6b6b">douglas@mcitybuilders.com</a> '
           '&middot; (508) 656-7436')

PAGES = {
 'terms': dict(
   title='Terms of Service | Maverick City Builders',
   desc='Terms of service for mcitybuilders.com - site use, estimates, quotes, contracts and limitations for Maverick City Builders, Lancaster MA.',
   h1='Terms of Service',
   body=(
    sec(1,'Agreement',p('These terms govern your use of <strong>mcitybuilders.com</strong>. By using the site you accept them. If you do not accept them, please do not use the site.')),
    sec(2,'What This Site Is',p('This site describes the remodeling and general contracting services Maverick City Builders offers in Worcester County and Central Massachusetts. It is informational. Nothing on it is an offer to perform work at a stated price.')),
    sec(3,'Estimates and Quotes',
        p('Any figures shown on this site &mdash; cost ranges, calculator output, typical project pricing &mdash; are illustrative only. They are not quotes and they do not bind either party.'),
        p('A binding price exists only in a written contract signed by both you and Maverick City Builders, after an in-person assessment of your property.')),
    sec(4,'Submitting an Enquiry',
        p('Submitting the contact form does not create a contract and does not reserve a place in our schedule. It is a request for us to get in touch.'),
        p('You agree that the information you submit is accurate and that you are authorised to request work at the property in question.')),
    sec(5,'Intellectual Property',p('The text, photographs, layout and code on this site belong to Maverick City Builders unless stated otherwise. You may not copy or republish them without written permission. Project photographs are of work performed by us and are published with the property owner&rsquo;s permission.')),
    sec(6,'Third-Party Links',p('Where we link to a town building department, a state licensing database or a manufacturer, we do not control that site and are not responsible for its content or availability.')),
    sec(7,'Limitation of Liability',p('The site is provided &ldquo;as is&rdquo;. To the fullest extent Massachusetts law allows, Maverick City Builders is not liable for any loss arising from reliance on information published here. This does not limit any obligation contained in a signed construction contract, and does not limit liability that cannot lawfully be limited.')),
    sec(8,'Governing Law',p('These terms are governed by the laws of the Commonwealth of Massachusetts. Any dispute is subject to the exclusive jurisdiction of the courts of Worcester County, Massachusetts.')),
    sec(9,'Changes',p(f'We may update these terms. The current version is always the one published here. Last updated {TODAY}.')),
    sec(10,'Contact',p(CONTACT)),
   )),
 'accessibility': dict(
   title='Accessibility Statement | Maverick City Builders',
   desc='Accessibility statement for mcitybuilders.com - our commitment to WCAG 2.1 AA, known limitations, and how to report a barrier.',
   h1='Accessibility Statement',
   body=(
    sec(1,'Our Commitment',p('Maverick City Builders wants every homeowner to be able to use this site, including people who browse with a screen reader, a keyboard only, magnification, or reduced motion.')),
    sec(2,'Standard We Aim For',p('We work towards <strong>WCAG 2.1 Level AA</strong>. That is the standard most commonly referenced for public-facing websites in the United States.')),
    sec(3,'What We Have Done',
        ul(['Every form field on the contact page has a programmatic label, so a screen reader announces it correctly.',
            'Every content image carries descriptive alternative text.',
            'One <code>&lt;h1&gt;</code> per page and a logical heading order throughout.',
            'The site is fully responsive and usable at 320px width and at 200% zoom.',
            'Decorative and tracking images are marked as decorative so screen readers skip them.',
            'Colour is never the only way information is conveyed.'])),
    sec(4,'Known Limitations',
        p('We are honest about what is not finished:'),
        ul(['Some interactive elements do not yet show a strong visible focus ring for keyboard users.',
            'The site has no &ldquo;skip to main content&rdquo; link.',
            'Some third-party embeds, such as the map on the contact page, are outside our control and may not meet the same standard.'])),
    sec(5,'Report a Barrier',
        p('If any part of this site stops you doing what you came to do, tell us and we will fix it. We aim to reply within two business days.'),
        p(CONTACT)),
    sec(6,'Alternatives',p('If you cannot use the contact form for any reason, call or text <strong>(508) 656-7436</strong> and we will take your details over the phone. You will never be disadvantaged for contacting us a different way.')),
    sec(7,'Review',p(f'This statement was last reviewed on {TODAY}.')),
   )),
 'cookie-policy': dict(
   title='Cookie Policy | Maverick City Builders',
   desc='Cookie policy for mcitybuilders.com - what cookies we use, why, and how to change your choice at any time.',
   h1='Cookie Policy',
   body=(
    sec(1,'The Short Version',p('This site loads <strong>no analytics or advertising cookies unless you accept them</strong>. When you first visit you are asked. If you decline, nothing is loaded and nothing is stored beyond your choice itself.')),
    sec(2,'Cookies We Use',
        p('<strong>Strictly necessary.</strong> A single entry in your browser&rsquo;s local storage records whether you accepted or declined, so we do not ask again on every page. It contains no personal information and is not shared.'),
        p('<strong>Analytics &mdash; only if you accept.</strong> Google Analytics tells us which pages people read and which searches bring them here, so we know what to write next. It is configured with Google Consent Mode and stays switched off until you accept.'),
        p('<strong>Advertising &mdash; only if you accept.</strong> The Meta Pixel measures whether an advert on Facebook or Instagram led to an enquiry.')),
    sec(3,'What We Never Do',
        ul(['We do not sell personal information.',
            'We do not use cookies to build a profile of you across unrelated websites.',
            'We do not load any tracker before you have made a choice.'])),
    sec(4,'Changing Your Mind',
        p('Your choice is stored in this browser. To change it, clear this site&rsquo;s data in your browser settings &mdash; the banner will appear again on your next visit.'),
        p('You can also block cookies entirely in your browser, or use a private window. The site works normally either way.')),
    sec(5,'Do Not Track',p('Some browsers send a &ldquo;Do Not Track&rdquo; signal. Because nothing loads before you consent, this site behaves as though Do Not Track is always on until you say otherwise.')),
    sec(6,'More Detail',p('For what we do with information you send us through the contact form, see our <a href="/privacy-policy" style="color:#ff6b6b">Privacy Policy</a>.')),
    sec(7,'Contact',p(CONTACT)),
   )),
}

def build():
    shell = io.open(SRC, encoding='utf-8', errors='replace', newline='').read()
    made = []
    for slug, cfg in PAGES.items():
        s = shell
        main_new = (f'<main class="flex-1 bg-black text-white"><div class="container max-w-3xl mx-auto py-16 px-4">'
                    f'<h1 class="{H1}">{cfg["h1"]}</h1>'
                    f'<p class="text-gray-400 text-sm mb-10">Last updated: {TODAY}</p>'
                    + ''.join(cfg['body']) + '</div></main>')
        s = re.sub(r'<main[\s\S]*?</main>', lambda _: main_new, s, count=1)
        s = re.sub(r'<title>[\s\S]*?</title>', f'<title>{cfg["title"]}</title>', s, count=1)
        s = re.sub(r'(<meta name="description" content=")[^"]*(")', lambda m: m.group(1)+cfg['desc']+m.group(2), s)
        s = re.sub(r'(<meta property="og:title" content=")[^"]*(")', lambda m: m.group(1)+cfg['title']+m.group(2), s)
        s = re.sub(r'(<meta property="og:description" content=")[^"]*(")', lambda m: m.group(1)+cfg['desc']+m.group(2), s)
        s = re.sub(r'(<meta name="twitter:title" content=")[^"]*(")', lambda m: m.group(1)+cfg['title']+m.group(2), s)
        s = re.sub(r'(<meta name="twitter:description" content=")[^"]*(")', lambda m: m.group(1)+cfg['desc']+m.group(2), s)
        s = s.replace(f'{BASE}/privacy-policy', f'{BASE}/{slug}')
        # drop the privacy-policy JSON-LD blocks; these pages need none
        s = re.sub(r'<script type="application/ld\+json">[\s\S]*?</script>', '', s)
        d = os.path.join(SITE, slug); os.makedirs(d, exist_ok=True)
        io.open(os.path.join(d, 'index.html'), 'w', encoding='utf-8', newline='').write(s)
        made.append(slug)
    print('built:', ', '.join('/'+m for m in made))

if __name__ == '__main__':
    build()
