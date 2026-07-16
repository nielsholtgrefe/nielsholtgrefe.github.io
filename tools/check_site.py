#!/usr/bin/env python3
"""Pre-deploy checks for the site. Run against a built _site/ directory.

A successful `jekyll build` is a weak guarantee: Liquid resolves a bad id or a
missing file to an empty string and carries on, so the page still builds and
still deploys. Everything checked here is something that builds green but is
wrong once it is online.

    python3 tools/check_site.py [--site _site]

Exits non-zero, listing every problem found, if anything fails.
"""

import argparse
import os
import re
import sys
from urllib.parse import urlsplit, unquote

import yaml

DATA = "_data"
problems = []


def fail(check, msg):
    problems.append((check, msg))


def load(name):
    path = os.path.join(DATA, name)
    if not os.path.exists(path):
        fail("data", "missing data file: " + path)
        return None
    with open(path, encoding="utf8") as fh:
        return yaml.safe_load(fh)


def check_pub_ids():
    """Every pub has a unique id, and every reference to one resolves.

    This is the check that matters most: the site refers to publications by id
    from four other files, and a typo renders nothing at all rather than
    erroring, so it would ship silently.
    """
    pubs = load("pubs.yml")
    if not pubs:
        return set()

    ids = []
    for i, p in enumerate(pubs):
        pid = p.get("id")
        if not pid:
            fail("pubs", "entry %d (%r) has no id" % (i, str(p.get("title"))[:50]))
        else:
            ids.append(pid)
        for required in ("title", "type"):
            if not p.get(required):
                fail("pubs", "%s: missing required field %r" % (pid, required))

    dupes = {x for x in ids if ids.count(x) > 1}
    for d in sorted(dupes):
        fail("pubs", "duplicate id: %s" % d)
    known = set(ids)

    # research.yml: ordered per-theme id lists
    for theme in load("research.yml") or []:
        for pid in theme.get("pubs") or []:
            if pid not in known:
                fail("research.yml", "theme %r references unknown pub id %r"
                     % (theme.get("id"), pid))

    # software.yml: each package's related papers
    for pkg in load("software.yml") or []:
        for pid in pkg.get("pubs") or []:
            if pid not in known:
                fail("software.yml", "package %r references unknown pub id %r"
                     % (pkg.get("name"), pid))

    # selected.yml: homepage + CV highlights
    for pid in load("selected.yml") or []:
        if pid not in known:
            fail("selected.yml", "unknown pub id %r" % pid)

    # corrections.yml: may legitimately be empty
    for corr in load("corrections.yml") or []:
        if corr.get("paper") not in known:
            fail("corrections.yml", "unknown pub id %r" % corr.get("paper"))

    return known


def check_links(site):
    """No internal link or asset reference 404s."""
    def exists(p):
        p = unquote(p).lstrip("/")
        if not p:
            return True
        return any(os.path.exists(c) for c in (
            os.path.join(site, p),
            os.path.join(site, p, "index.html"),
            os.path.join(site, p + ".html"),
        ))

    pages = [os.path.join(d, f) for d, _, fs in os.walk(site)
             for f in fs if f.endswith(".html")]
    if not pages:
        fail("links", "no pages found in %s - did the build run?" % site)
        return

    seen = set()
    for page in pages:
        with open(page, encoding="utf8", errors="replace") as fh:
            html = fh.read()
        rel = page.replace(site, "") or "/"
        for m in re.finditer(r'(?:href|src)="([^"]+)"', html):
            url = m.group(1).replace("&amp;", "&")
            if url.startswith(("http://", "https://", "//", "#", "mailto:",
                               "data:", "javascript:", "tel:")):
                continue
            path = urlsplit(url).path
            if path and not exists(path):
                key = (rel, url)
                if key not in seen:
                    seen.add(key)
                    fail("links", "%s -> %s" % (rel, url))


def check_unrendered_liquid(site):
    """A Liquid tag left in the output means a template silently misfired."""
    for d, _, fs in os.walk(site):
        for f in fs:
            if not f.endswith((".html", ".xml")):
                continue
            path = os.path.join(d, f)
            with open(path, encoding="utf8", errors="replace") as fh:
                text = fh.read()
            if "{%" in text:
                fail("liquid", "unrendered Liquid tag in " + path.replace(site, ""))


def check_expected_pages(site):
    """The pages that must exist for the site to be usable."""
    for page in ("index.html", "research/index.html", "publications/index.html",
                 "software/index.html", "cv/index.html", "teaching/index.html",
                 "conferences/index.html", "404.html", "publications.bib",
                 "sitemap.xml", "feed.xml"):
        if not os.path.exists(os.path.join(site, page)):
            fail("pages", "expected output missing: " + page)


def check_bib(site):
    """The .bib download must be complete and syntactically sound."""
    path = os.path.join(site, "publications.bib")
    if not os.path.exists(path):
        return
    with open(path, encoding="utf8") as fh:
        bib = fh.read()
    pubs = load("pubs.yml") or []
    n = bib.count("@")
    if n != len(pubs):
        fail("bib", "publications.bib has %d entries, pubs.yml has %d" % (n, len(pubs)))
    if bib.count("{") != bib.count("}"):
        fail("bib", "publications.bib has unbalanced braces")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--site", default="_site")
    args = ap.parse_args()

    check_pub_ids()
    check_expected_pages(args.site)
    check_links(args.site)
    check_unrendered_liquid(args.site)
    check_bib(args.site)

    if not problems:
        print("All checks passed.")
        return 0

    by_check = {}
    for check, msg in problems:
        by_check.setdefault(check, []).append(msg)
    print("%d problem(s) found:\n" % len(problems))
    for check in sorted(by_check):
        print("  [%s]" % check)
        for msg in by_check[check]:
            print("     " + msg)
        print()
    return 1


if __name__ == "__main__":
    sys.exit(main())
