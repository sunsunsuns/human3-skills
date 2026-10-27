import os
import re

OCR = os.path.join("_book", "ocr")
OUT = os.path.join("_book", "book.txt")

def main():
    parts = []
    files = sorted(f for f in os.listdir(OCR) if re.match(r"page_\d{3}\.txt$", f))
    for f in files:
        n = int(re.search(r"(\d+)", f).group(1))
        with open(os.path.join(OCR, f), encoding="utf-8") as fh:
            txt = fh.read().strip()
        # OCR often puts a space between every CJK glyph; collapse spaces between CJK chars
        txt = re.sub(r"(?<=[\u3000-\u9fff\uff00-\uffef])\s+(?=[\u3000-\u9fff\uff00-\uffef])", "", txt)
        txt = re.sub(r"[ \t]{2,}", " ", txt)
        parts.append("\n\n===== [P%d] =====\n%s" % (n, txt))
    with open(OUT, "w", encoding="utf-8") as fh:
        fh.write("\n".join(parts))
    print("wrote", OUT, os.path.getsize(OUT), "bytes,", len(files), "pages")

if __name__ == "__main__":
    main()
