#!/usr/bin/env python3
"""Wire the new legal pages into the site: footers, sitemap, privacy policy.

1. Adds Terms / Accessibility / Cookie Policy beside the existing Privacy Policy
   link in all three footer variants.
2. Adds the three URLs to sitemap.xml.
3. Rewrites the Cookies section of the privacy policy to match the consent gate,
   and adds a Your Rights section (access, correction, deletion, opt-out) plus a
   California note.
Idempotent.
"""
import glob, io, os, re

SITE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = 'https://mcitybuilders.com'
NEW = [('/terms','Terms'), ('/accessibility','Accessibility'), ('/cookie-policy','Cookie Policy')]

def footers():
    n = 0
    for f in sorted(glob.glob(os.path.join(SITE,'**','*.html'), recursive=True)):
        if os.sep+'assets'+os.sep in f: continue
        s = io.open(f, encoding='utf-8', errors='replace', newline='').read(); o = s
        for m in list(re.finditer(r'<a href="/privacy-policy"([^>]*)>Privacy Policy</a>', s)):
            attrs = m.group(1)
            if '/cookie-policy' in s[m.end():m.end()+400]: continue
            extra = ''.join(f'<a href="{u}"{attrs}>{t}</a>' for u,t in NEW)
            sep = '&nbsp;&middot;&nbsp;' if 'hover:text-white' in attrs else ' '
            add = sep + sep.join(f'<a href="{u}"{attrs}>{t}</a>' for u,t in NEW) if sep.strip() else extra
            s = s[:m.end()] + add + s[m.end():]
            break
        if s != o:
            io.open(f,'w',encoding='utf-8',newline='').write(s); n += 1
    print(f'footers updated: {n}')

def sitemap():
    p = os.path.join(SITE,'sitemap.xml')
    s = io.open(p,encoding='utf-8',newline='').read(); o = s
    for u,_ in NEW:
        if f'{BASE}{u}<' in s: continue
        s = s.replace('</urlset>', f'<url><loc>{BASE}{u}</loc><changefreq>yearly</changefreq><priority>0.3</priority></url>\n</urlset>')
    if s != o:
        io.open(p,'w',encoding='utf-8',newline='').write(s)
    print('sitemap entries:', s.count('<loc>'))

COOKIES_NEW = ('<section class="mb-10"><h2 class="font-heading text-xl font-bold text-white mb-3">6. Cookies and Tracking</h2>'
 '<p class="text-gray-300 leading-relaxed mb-4">This site loads <strong>no analytics or advertising cookies unless you accept them</strong>. '
 'On your first visit you are asked to accept or decline. Google Analytics and the Meta Pixel are configured with Google Consent Mode and stay '
 'switched off until you accept. If you decline, nothing is loaded.</p>'
 '<p class="text-gray-300 leading-relaxed">Your choice is stored in your browser. Clearing this site&rsquo;s data will bring the banner back. '
 'Full detail is in our <a href="/cookie-policy" style="color:#ff6b6b">Cookie Policy</a>.</p></section>')

RIGHTS = ('<section class="mb-10"><h2 class="font-heading text-xl font-bold text-white mb-3">8a. Your Rights Over Your Information</h2>'
 '<p class="text-gray-300 leading-relaxed mb-4">Whatever state you live in, you may ask us to:</p>'
 '<ul class="text-gray-300 leading-relaxed list-disc pl-6 space-y-2 mb-4">'
 '<li><strong>Tell you what we hold</strong> about you and where it came from.</li>'
 '<li><strong>Correct</strong> anything inaccurate.</li>'
 '<li><strong>Delete it.</strong> We will erase your enquiry and contact details unless we are required to keep records tied to a signed construction contract.</li>'
 '<li><strong>Opt out</strong> of analytics and advertising cookies at any time, by declining the banner or clearing this site&rsquo;s data.</li>'
 '<li><strong>Stop contacting you.</strong> Ask once and we stop.</li></ul>'
 '<p class="text-gray-300 leading-relaxed mb-4">Email <a href="mailto:douglas@mcitybuilders.com" style="color:#ff6b6b">douglas@mcitybuilders.com</a> '
 'or call (508) 656-7436. We respond within 30 days and we never charge for a request or treat you differently for making one.</p>'
 '<p class="text-gray-300 leading-relaxed"><strong>California residents.</strong> The rights above are the ones the CCPA/CPRA provides. '
 'We do not sell or share personal information as those terms are defined, and we do not use it for cross-context behavioural advertising '
 'beyond the advertising cookies you can decline.</p></section>')

def privacy():
    p = os.path.join(SITE,'privacy-policy','index.html')
    s = io.open(p,encoding='utf-8',errors='replace',newline='').read(); o = s
    s = re.sub(r'<section class="mb-10"><h2[^>]*>6\. Cookies</h2>[\s\S]*?</section>', COOKIES_NEW, s, count=1)
    if 'Your Rights Over Your Information' not in s:
        m = re.search(r'(<section class="mb-10"><h2[^>]*>9\. Security</h2>)', s)
        if m: s = s[:m.start()] + RIGHTS + s[m.start():]
    s = re.sub(r'Last updated: July 7, 2026', 'Last updated: September 1, 2026', s)
    if s != o:
        io.open(p,'w',encoding='utf-8',newline='').write(s)
    print('privacy policy updated:', s != o)

if __name__ == '__main__':
    footers(); sitemap(); privacy()
