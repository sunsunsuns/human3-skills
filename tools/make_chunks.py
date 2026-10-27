import json
import os
import re

BOOK = os.path.join("_book", "book.txt")
OUTDIR = os.path.join("outputs", "humans-3.0-peter-nowak", "candidates")

CHUNKS = [
    ("A", 9, 49, "第1章 进化 + 第2章 经济"),
    ("B", 50, 112, "第3章 健康 + 第4章 工作 + 第5章 艺术"),
    ("C", 113, 172, "第6章 关系 + 第7章 身份 + 第8章 信仰"),
    ("D", 173, 229, "第9章 幸福 + 第10章 结论 + 致谢/注释"),
]


def main():
    os.makedirs(OUTDIR, exist_ok=True)
    with open(BOOK, encoding="utf-8") as f:
        text = f.read()
    # split on page markers while keeping them
    parts = re.split(r"\n\n===== \[P(\d+)\] =====\n", "\n" + text)
    pages = {}
    # parts: [pre, num, body, num, body, ...]
    for i in range(1, len(parts) - 1, 2):
        pages[int(parts[i])] = parts[i + 1]
    print("pages parsed:", len(pages))
    manifest = []
    for name, start, end, label in CHUNKS:
        buf = []
        for p in range(start, end + 1):
            if p in pages:
                buf.append("\n===== [P%d] =====\n%s" % (p, pages[p]))
        fp = os.path.join(OUTDIR, "chunk-%s.txt" % name)
        with open(fp, "w", encoding="utf-8") as f:
            f.write("".join(buf))
        size = os.path.getsize(fp)
        chars = sum(len(pages.get(p, "")) for p in range(start, end + 1))
        manifest.append({"chunk": name, "pages": [start, end], "label": label, "file": fp, "bytes": size, "chars": chars})
        print(name, start, end, label, size, "bytes", chars, "chars")
    with open(os.path.join(OUTDIR, "chunks.json"), "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=1)


if __name__ == "__main__":
    main()
