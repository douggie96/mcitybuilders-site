import os,re,glob,html,json,io,collections
SITE=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
man=json.load(open("_phase2_manifest.json"))
BASE="https://mcitybuilders.com"
# map every CDN url form (bare, wsrv-wrapped, with params) -> manifest entry
by_uuid={}
for u,v in man.items():
    by_uuid[re.search(r'/([0-9a-f-]{36})\.', u).group(1)]=v
def lookup(url):
    m=re.search(r'([0-9a-f-]{36})', html.unescape(url))
    return by_uuid.get(m.group(1)) if m else None
def webp(v,w): return f"/assets/img/{v['name']}-{w}.webp"
def fb(v):     return f"/assets/img/{v['fallback']}"
def srcset(v): return ", ".join(f"{webp(v,w)} {w}w" for w in v["widths"])

stats=collections.Counter()

def rewrite_img(tag):
    m=re.search(r'src="([^"]+)"',tag)
    if not m: return tag
    v=lookup(m.group(1))
    if not v: return tag
    attrs=dict(re.findall(r'(\w[\w-]*)="([^"]*)"',tag))
    keep={k:val for k,val in attrs.items() if k not in ("src","srcset","sizes")}
    keep.setdefault("width",str(v["w"])); keep.setdefault("height",str(v["h"]))
    keep.setdefault("loading","lazy"); keep.setdefault("decoding","async")
    a=" ".join(f'{k}="{val}"' for k,val in keep.items())
    stats["img"]+=1
    return (f'<picture><source type="image/webp" srcset="{srcset(v)}" sizes="(max-width:768px) 100vw, 1408px">'
            f'<img src="{fb(v)}" {a}></picture>')

for f in sorted(glob.glob(SITE+"/**/*.html",recursive=True)):
    if "/assets/" in f.replace("\\","/"): continue
    s=io.open(f,encoding='utf-8',newline='').read(); orig=s

    # 1. <img> -> <picture>
    s=re.sub(r'(?is)<img\b[^>]*>', lambda m: rewrite_img(m.group(0)), s)

    # 2. favicon
    def _icon(m):
        stats["icon"]+=1
        return '<link rel="icon" type="image/png" sizes="32x32" href="/assets/img/favicon-32.png"><link rel="apple-touch-icon" sizes="180x180" href="/assets/img/apple-touch-icon.png">'
    s=re.sub(r'(?is)<link[^>]+rel="icon"[^>]*>', _icon, s)

    # 3. drop wsrv preconnect/dns-prefetch
    n=len(re.findall(r'(?is)<link[^>]+href="https://wsrv\.nl"[^>]*>',s))
    if n: stats["preconnect"]+=n
    s=re.sub(r'(?is)<link[^>]+href="https://wsrv\.nl"[^>]*>','',s)

    # 4. og:image / twitter:image -> absolute local
    def _meta(m):
        v=lookup(m.group(2))
        if not v: return m.group(0)
        stats["meta"]+=1
        return m.group(0).replace(m.group(2), BASE+fb(v))
    s=re.sub(r'(?is)(<meta[^>]+(?:property|name)="(?:og:image|twitter:image)"[^>]+content=")([^"]+)"',
             lambda m: _meta(m) if lookup(m.group(2)) else m.group(0), s)

    # 5. preload as=image -> local webp 800 (or largest available)
    def _preload(m):
        v=lookup(m.group(0))
        if not v: return m.group(0)
        stats["preload"]+=1
        w=800 if 800 in v["widths"] else v["widths"][-1]
        return (f'<link rel="preload" as="image" href="{webp(v,w)}" '
                f'imagesrcset="{srcset(v)}" imagesizes="(max-width:768px) 100vw, 1408px">')
    s=re.sub(r'(?is)<link[^>]+rel="preload"[^>]*as="image"[^>]*>', _preload, s)

    # 6. CSS background-image url()
    def _css(m):
        v=lookup(m.group(1))
        if not v: return m.group(0)
        stats["css"]+=1
        return m.group(0).replace(m.group(1), fb(v))
    s=re.sub(r'url\(&quot;((?:https://)[^&]*?(?:vibe\.filesafe|wsrv)[^&]*)&quot;\)', _css, s)
    s=re.sub(r'url\((https://[^)\'"]*(?:vibe\.filesafe|wsrv)[^)\'"]*)\)', _css, s)

    if s!=orig:
        io.open(f,'w',encoding='utf-8',newline='').write(s); stats["files"]+=1

print("rewrites:",dict(stats))
