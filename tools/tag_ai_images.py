#!/usr/bin/env python3
"""Stamp AI-generated JPEGs with IPTC DigitalSourceType = trainedAlgorithmicMedia.

No exiftool, pyexiv2, iptcinfo3 or piexif is available in this environment, so the
XMP packet is written directly as a JPEG APP1 segment (the same container exiftool
would use).  Idempotent: a file that already carries the property is skipped.
"""
import os, sys, glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG = os.path.join(ROOT, 'assets', 'img')

NS = b'http://ns.adobe.com/xap/1.0/\x00'
SOURCE_TYPE = 'http://cv.iptc.org/newscodes/digitalsourcetype/trainedAlgorithmicMedia'

XMP = ('''<?xpacket begin="﻿" id="W5M0MpCehiHzreSzNTczkc9d"?>
<x:xmpmeta xmlns:x="adobe:ns:meta/">
 <rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about=""
   xmlns:Iptc4xmpExt="http://iptc.org/std/Iptc4xmpExt/2008-02-29/"
   xmlns:dc="http://purl.org/dc/elements/1.1/"
   Iptc4xmpExt:DigitalSourceType="''' + SOURCE_TYPE + '''">
   <dc:description>
    <rdf:Alt><rdf:li xml:lang="x-default">AI-generated design illustration. Not a photograph of a Maverick City Builders project.</rdf:li></rdf:Alt>
   </dc:description>
  </rdf:Description>
 </rdf:RDF>
</x:xmpmeta>
<?xpacket end="w"?>''').encode('utf-8')


def already_tagged(data):
    return SOURCE_TYPE.encode('ascii') in data


def insert_xmp(data):
    """Insert an XMP APP1 segment after SOI and any leading APP0/APP1 segments."""
    if data[:2] != b'\xff\xd8':
        raise ValueError('not a JPEG')
    pos = 2
    # skip existing APPn segments so the new one sits with its peers
    while pos + 4 <= len(data) and data[pos] == 0xFF and 0xE0 <= data[pos + 1] <= 0xEF:
        seglen = int.from_bytes(data[pos + 2:pos + 4], 'big')
        pos += 2 + seglen
    payload = NS + XMP
    seglen = len(payload) + 2
    if seglen > 0xFFFF:
        raise ValueError('XMP packet too large for one APP1 segment')
    seg = b'\xff\xe1' + seglen.to_bytes(2, 'big') + payload
    return data[:pos] + seg + data[pos:]


def main():
    files = sorted(glob.glob(os.path.join(IMG, 'ai-*.jpg')))
    if not files:
        print('no ai-*.jpg found')
        return 1
    for p in files:
        data = open(p, 'rb').read()
        name = os.path.basename(p)
        if already_tagged(data):
            print('skip (already tagged):', name)
            continue
        out = insert_xmp(data)
        with open(p, 'wb') as fh:
            fh.write(out)
        print('tagged:', name, '%d -> %d bytes' % (len(data), len(out)))
    return 0


if __name__ == '__main__':
    sys.exit(main())
