"""Quality gate for the Humans 3.0 skill package.

Checks:
1. Every skill dir has SKILL.md + test-prompts.json and required frontmatter.
2. Every SKILL.md has R/I/A1/A2/E/B sections.
3. Every cross-reference ./humans30-* points to an existing dir.
4. test-prompts.json parses and has >=5 prompts incl. >=2 decoys.
5. Every knowledge card's related_skills point to existing skills.
"""
import json
import os
import re
import sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKILL_GLOB = re.compile(r"^humans30-[a-z0-9-]+$")
REQUIRED_FM = ["name", "slug", "displayName", "description", "version"]


def skill_dirs():
    return sorted(
        d for d in os.listdir(BASE)
        if os.path.isdir(os.path.join(BASE, d)) and SKILL_GLOB.match(d)
    )


def frontmatter(text):
    m = re.match(r"^---\r?\n(.*?)\r?\n---", text, re.S)
    if not m:
        return {}
    fm = {}
    for line in m.group(1).splitlines():
        if ":" in line and not line.startswith(" "):
            k, v = line.split(":", 1)
            fm[k.strip()] = v.strip()
    return fm


def main():
    errors = []
    warns = []
    dirs = skill_dirs()
    print("skills found:", len(dirs))

    for d in dirs:
        sp = os.path.join(BASE, d, "SKILL.md")
        tp = os.path.join(BASE, d, "test-prompts.json")
        if not os.path.exists(sp):
            errors.append(f"{d}: missing SKILL.md")
            continue
        text = open(sp, encoding="utf-8").read()
        fm = frontmatter(text)
        for k in REQUIRED_FM:
            if not fm.get(k):
                errors.append(f"{d}: frontmatter missing {k}")
        if fm.get("slug") and fm["slug"] != d:
            errors.append(f"{d}: slug mismatch ({fm['slug']})")
        for sec in ["## R —", "## I —", "## A1 —", "## A2 —", "## E —", "## B —"]:
            if sec not in text:
                errors.append(f"{d}: missing section {sec}")
        # R quotes length check (rough: lines starting with > "..." )
        for q in re.findall(r"^> \"(.*?)\"", text, re.M):
            if len(q) > 150:
                warns.append(f"{d}: R quote {len(q)} chars > 150")
        # cross refs
        for ref in set(re.findall(r"`(humans30-[a-z0-9-]+)`", text)):
            if ref not in dirs:
                errors.append(f"{d}: dangling cross-ref {ref}")

        if not os.path.exists(tp):
            errors.append(f"{d}: missing test-prompts.json")
            continue
        try:
            prompts = json.load(open(tp, encoding="utf-8"))
        except Exception as e:
            errors.append(f"{d}: test-prompts.json invalid: {e}")
            continue
        if len(prompts) < 5:
            errors.append(f"{d}: only {len(prompts)} test prompts (<5)")
        decoys = [p for p in prompts if p.get("expect_call") is False]
        if len(decoys) < 2:
            errors.append(f"{d}: only {len(decoys)} decoys (<2)")
        for p in prompts:
            if "prompt" not in p or "expect_call" not in p:
                errors.append(f"{d}: prompt item missing fields: {p}")

    # knowledge cards
    cards_root = os.path.join(BASE, "knowledge", "cards")
    cards = 0
    if os.path.isdir(cards_root):
        for root, _dirs, files in os.walk(cards_root):
            for f in files:
                if not f.startswith("card-") or not f.endswith(".md"):
                    continue
                cards += 1
                text = open(os.path.join(root, f), encoding="utf-8").read()
                for ref in re.findall(r"related_skills:\s*\[(.*?)\]", text):
                    for r in [x.strip() for x in ref.split(",") if x.strip()]:
                        if r not in dirs:
                            errors.append(f"{f}: card related_skill missing {r}")
    print("knowledge cards:", cards)

    # index links
    idx = os.path.join(BASE, "INDEX.md")
    if os.path.exists(idx):
        text = open(idx, encoding="utf-8").read()
        for ref in set(re.findall(r"\./(humans30-[a-z0-9-]+)/", text)):
            if ref not in dirs:
                errors.append(f"INDEX.md: dangling {ref}")

    print("warnings:", len(warns))
    for w in warns:
        print("  WARN", w)
    print("errors:", len(errors))
    for e in errors:
        print("  ERR ", e)
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
