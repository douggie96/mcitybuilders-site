#!/usr/bin/env python3
"""Gate Google Analytics and the Meta Pixel behind explicit consent.

Before: gtag.js, fbevents.js and a <noscript> tracking pixel all fired on page
load with no notice and no choice.

After:
  * Google Consent Mode v2 defaults are set to DENIED before any tag loads.
  * Tracking scripts are inert (type="text/plain") until the visitor accepts.
  * A banner offers Accept / Decline; the choice is stored in localStorage.
  * The <noscript> pixel is removed - it cannot be gated by JavaScript.
  * Declining loads nothing. No cookies are set by GA or Meta.

Also restores GA to the area pages that were missing it - gated like the rest.

Idempotent: pages already carrying the marker are skipped.
Usage: python3 tools/consent_gate.py [--dry-run]
"""
import glob, io, os, re, sys

SITE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MARK = 'mcb-consent-v1'
GA_ID, GA4_ID, PIXEL_ID = 'GT-NM846W2P', 'G-7HXJQJL5Q2', '1750236342810025'

BOOTSTRAP = f'''<!-- {MARK}: consent defaults must run before any tag -->
<script>
window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}
gtag('consent','default',{{ad_storage:'denied',ad_user_data:'denied',ad_personalization:'denied',
analytics_storage:'denied',functionality_storage:'granted',security_storage:'granted'}});
window.__mcbConsent={{
 get:function(){{try{{return localStorage.getItem('mcb-consent');}}catch(e){{return null;}}}},
 set:function(v){{try{{localStorage.setItem('mcb-consent',v);}}catch(e){{}}}},
 load:function(){{
   if(window.__mcbLoaded)return; window.__mcbLoaded=1;
   gtag('consent','update',{{ad_storage:'granted',ad_user_data:'granted',
   ad_personalization:'granted',analytics_storage:'granted'}});
   document.querySelectorAll('script[data-mcb-src]').forEach(function(s){{
     var n=document.createElement('script'); n.async=true; n.src=s.getAttribute('data-mcb-src');
     document.head.appendChild(n);
   }});
 }}
}};
</script>
'''

BANNER = f'''<!-- {MARK}: banner -->
<div id="mcb-cookie-banner" hidden role="dialog" aria-live="polite" aria-label="Cookie choices"
 style="position:fixed;left:0;right:0;bottom:0;z-index:99999;background:#0b0b0b;border-top:2px solid #E10600;
 color:#e6e6e6;padding:18px 20px;font-family:Inter,system-ui,sans-serif;font-size:14px;line-height:1.55;
 display:flex;flex-wrap:wrap;gap:14px;align-items:center;justify-content:center;box-shadow:0 -8px 30px rgba(0,0,0,.5)">
 <span style="max-width:640px">We use analytics cookies to understand how the site is used. They load only if you accept.
 Read our <a href="/cookie-policy" style="color:#ff6b6b;text-decoration:underline">Cookie Policy</a>.</span>
 <span style="display:flex;gap:10px">
  <button type="button" id="mcb-cookie-decline" style="background:transparent;color:#e6e6e6;border:1px solid #555;
   padding:10px 20px;border-radius:4px;font-weight:600;cursor:pointer;font-family:inherit;font-size:13px">Decline</button>
  <button type="button" id="mcb-cookie-accept" style="background:#E10600;color:#fff;border:0;padding:10px 22px;
   border-radius:4px;font-weight:700;cursor:pointer;font-family:inherit;font-size:13px">Accept</button>
 </span>
</div>
<script>
(function(){{
 var C=window.__mcbConsent,b=document.getElementById('mcb-cookie-banner');
 if(!C||!b)return;
 var v=C.get();
 if(v==='granted'){{C.load();return;}}
 if(v==='denied')return;
 b.hidden=false;
 document.getElementById('mcb-cookie-accept').addEventListener('click',function(){{C.set('granted');b.hidden=true;C.load();}});
 document.getElementById('mcb-cookie-decline').addEventListener('click',function(){{C.set('denied');b.hidden=true;}});
}})();
</script>
'''

GA_INERT = (f'<script type="text/plain" data-mcb-src="https://www.googletagmanager.com/gtag/js?id={GA_ID}"></script>'
            f'<script>gtag("js",new Date());gtag("config","{GA_ID}");gtag("config","{GA4_ID}");</script>')

def gate(s):
    # 1. neutralise tracking script tags -> inert until consent
    def inert(m):
        tag = m.group(0)
        src = re.search(r'src="([^"]+)"', tag)
        if not src:
            return tag
        return f'<script type="text/plain" data-mcb-src="{src.group(1)}"></script>'
    s = re.sub(r'<script[^>]*src="https://www\.googletagmanager\.com/gtag/js[^"]*"[^>]*>\s*</script>', inert, s)
    s = re.sub(r'<script[^>]*src="https://connect\.facebook\.net/[^"]*"[^>]*>\s*</script>', inert, s)
    # 2. remove <noscript> tracking pixels - JS cannot gate them
    s = re.sub(r'<noscript>\s*<img[^>]*facebook\.com/tr[^>]*>\s*</noscript>', '', s, flags=re.I)
    s = re.sub(r'<img[^>]*facebook\.com/tr[^>]*>', '', s, flags=re.I)
    # 3. strip duplicate dataLayer/gtag bootstraps (ours defines them first)
    s = re.sub(r'<script>\s*window\.dataLayer\s*=\s*window\.dataLayer\s*\|\|?\s*\[\];\s*'
               r'function gtag\(\)\{dataLayer\.push\(arguments\);\}\s*', '<script>', s)
    return s

def main():
    dry = '--dry-run' in sys.argv
    done = added_ga = 0
    for f in sorted(glob.glob(os.path.join(SITE, '**', '*.html'), recursive=True)):
        if os.sep + 'assets' + os.sep in f:
            continue
        s = io.open(f, encoding='utf-8', errors='replace', newline='').read()
        if MARK in s:
            continue
        o = s
        s = gate(s)
        # restore GA on pages that have none (gated)
        if 'googletagmanager.com/gtag/js' not in s and '</head>' in s:
            s = s.replace('</head>', GA_INERT + '</head>', 1)
            added_ga += 1
        # bootstrap first in <head>
        m = re.search(r'<head[^>]*>', s)
        if m:
            s = s[:m.end()] + '\n' + BOOTSTRAP + s[m.end():]
        # banner before </body>
        if '</body>' in s:
            s = s.replace('</body>', BANNER + '</body>', 1)
        if s != o:
            done += 1
            if not dry:
                io.open(f, 'w', encoding='utf-8', newline='').write(s)
    print(f'pages gated: {done}')
    print(f'pages given GA back (gated): {added_ga}')

if __name__ == '__main__':
    main()
