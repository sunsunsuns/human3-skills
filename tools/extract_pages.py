"""Extract scanned page JPEGs from a PDF that uses only DCTDecode image streams.

Pure stdlib (no PyMuPDF/pypdf needed). Builds page order from the /Pages tree when
possible, else falls back to object order.

Usage:
    python tools/extract_pages.py "path/to/book.pdf" [out_dir]

Outputs:
    <out_dir>/page_001.jpg ... + pages_manifest.json
"""
import json
import os
import re
import sys


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return 1
    pdf = sys.argv[1]
    out = sys.argv[2] if len(sys.argv) > 2 else os.path.join("_book", "pages")
    os.makedirs(out, exist_ok=True)

    with open(pdf, "rb") as f:
        data = f.read()
    print("pdf bytes:", len(data))

    # index object offsets
    obj_offsets = {}
    for m in re.finditer(rb"(?m)^(\d+)\s+0\s+obj\b", data):
        obj_offsets[int(m.group(1))] = m.start()
    print("objects:", len(obj_offsets))

    def obj_body(num):
        """Return (dict_bytes, stream_bytes_or_None)."""
        start = obj_offsets.get(num)
        if start is None:
            return None, None
        end = data.find(b"endobj", start)
        if end < 0:
            end = len(data)
        body = data[start:end]
        sm = re.search(rb"stream\r?\n", body)
        if not sm:
            return body, None
        s = sm.end()
        em = body.rfind(b"endstream")
        return body[: sm.start()], body[s:em]

    # page tree walk
    pages = []
    roots = []
    for num in obj_offsets:
        body, _ = obj_body(num)
        if body is None:
            continue
        head = body[:2000]
        if re.search(rb"/Type\s*/Pages", head) and b"/Parent" not in head:
            roots.append(num)

    def walk(num, depth=0, seen=None):
        seen = seen or set()
        if num in seen or depth > 20:
            return
        seen.add(num)
        body, _ = obj_body(num)
        if body is None:
            return
        if re.search(rb"/Type\s*/Page\b", body) and not re.search(rb"/Type\s*/Pages", body):
            pages.append(num)
            return
        km = re.search(rb"/Kids\s*\[(.*?)\]", body, re.S)
        if not km:
            return
        for kid in re.finditer(rb"(\d+)\s+0\s+R", km.group(1)):
            walk(int(kid.group(1)), depth + 1, seen)

    if roots:
        print("pages tree roots:", roots)
        walk(sorted(roots)[0])
    print("pages found via tree:", len(pages))

    obj_order_pages = [
        n for n in sorted(obj_offsets)
        if re.search(rb"/Type\s*/Page\b", (obj_body(n)[0] or b"")[:2000])
        and not re.search(rb"/Type\s*/Pages", (obj_body(n)[0] or b"")[:2000])
    ]
    print("page objects in object order:", len(obj_order_pages))

    order = pages if len(pages) == len(obj_order_pages) and pages else obj_order_pages

    manifest = []
    for i, pnum in enumerate(order, 1):
        pbody, _ = obj_body(pnum)
        refs = [int(m.group(1)) for m in re.finditer(rb"(\d+)\s+0\s+R", pbody or b"")]
        picked = None
        for r in refs:
            b2, s2 = obj_body(r)
            if s2 is not None and b"/DCTDecode" in (b2 or b""):
                picked = (r, s2)
                break
        if not picked:
            for r in refs:
                b2, s2 = obj_body(r)
                if s2 is not None:
                    picked = (r, s2)
                    break
        if not picked:
            print("!! no image for page", i, "obj", pnum)
            manifest.append({"page": i, "obj": pnum, "file": None})
            continue
        r, stream = picked
        fn = "page_%03d.jpg" % i
        with open(os.path.join(out, fn), "wb") as f:
            f.write(stream.lstrip(b"\r\n"))
        manifest.append({"page": i, "obj": pnum, "img_obj": r, "file": fn, "bytes": len(stream)})

    with open(os.path.join(out, "pages_manifest.json"), "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=1)
    ok = sum(1 for m in manifest if m.get("file"))
    print("wrote", ok, "page images to", os.path.abspath(out))
    print("page order head:", order[:8])
    return 0


if __name__ == "__main__":
    sys.exit(main())
