#!/usr/bin/env python3
"""
Infra Atlas — homepage section-rhythm guard.

The homepage paints every top-level section as a translucent box
(`background: rgba(10, 9, 7, 0.88)`) sitting over a `position: fixed` globe
canvas. Two failure modes keep recurring when a section is added or edited:

  1. Horizontal drift. A section that doesn't use the shared container
     (`max-width` + horizontal padding) sits ~48px off from its siblings.
     This shipped on .dispatches (re-aligned 2026-06-12) and again on
     .providers/.manifesto/.colophon (re-aligned 2026-06-16).

  2. Globe seam. A section that spaces itself with a vertical *margin* opens a
     transparent band between the boxes, and the globe shows through, so the
     section looks detached. This shipped on .dispatches with `margin-top:100px`
     (fixed 2026-06-16: padding tiles the boxes, margin does not).

This guard reads the inline CSS in index.html and, for every section in the
translucent-background group, asserts:
  - it sizes with the container token  `max-width: var(--ia-section-max)`
  - it insets with the padding token   `... var(--ia-section-pad-x) ...`
  - its vertical padding is 0 or a `--ia-space-*` scale token (no ad-hoc px)
  - it does NOT space itself with a non-zero vertical margin
The container tokens and the `--ia-space-*` scale must be defined in :root.

`.signature` (a centred one-line credit, not a container) is exempt from the
container checks. `.colophon` keeps a deliberate `margin-top` that separates the
footer from the content, so it is allow-listed for the vertical-margin check.
Add a new section to the right set ON PURPOSE, or fix the section — don't widen
the allow-list to silence a real drift.

Run from repo root:  python3 scripts/check_section_rhythm.py
No third-party deps; credential-free. Sibling of check_html_attrs.py.
"""
import os
import re
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
INDEX = os.path.join(ROOT, "index.html")

BG_MARKER = "rgba(10, 9, 7, 0.88)"
MAX_TOKEN = "var(--ia-section-max)"
PADX_TOKEN = "var(--ia-section-pad-x)"
SCALE_TOKENS = ("--ia-space-2xl", "--ia-space-xl", "--ia-space-m")
SCALE_PREFIX = "var(--ia-space-"

# Centred credit line, not a content rectangle — no container contract.
EXEMPT_CONTAINER = {".signature"}
# Footer keeps an intentional top margin to detach from the content above.
ALLOW_VMARGIN = {".colophon", ".signature"}

ZERO = {"0", "0px", "auto"}


def css_of(html):
    """Concatenated inline <style> CSS, with comments stripped so braces only
    ever delimit rules."""
    blocks = re.findall(r"<style[^>]*>(.*?)</style>", html, re.S)
    css = "\n".join(blocks)
    return re.sub(r"/\*.*?\*/", "", css, flags=re.S)


def rules(css):
    """Yield (selector, body) for every declaration block at any nesting.
    The selector is the text since the previous brace; the body is the text up
    to its closing brace. Good enough because braces only delimit rules here."""
    sel = ""
    token = ""
    stack = []
    for ch in css:
        if ch == "{":
            stack.append(token.strip())
            token = ""
        elif ch == "}":
            body = token
            sel = stack.pop() if stack else ""
            yield sel, body
            token = ""
        else:
            token += ch


def section_classes(rule_list):
    """The selector list of the translucent-background rule, as bare classes."""
    for sel, body in rule_list:
        if BG_MARKER in body:
            return [s.strip() for s in sel.split(",") if s.strip()]
    return []


def vertical_margin_offender(body):
    """Return the offending margin declaration if `body` sets a non-zero, non-
    auto top/bottom margin, else None."""
    for prop in ("margin-top", "margin-bottom"):
        # negative lookbehind so `scroll-margin-top` (a scroll-anchor offset,
        # not a layout margin) doesn't trip the check.
        m = re.search(r"(?<![\w-])" + prop + r"\s*:\s*([^;]+);", body)
        if m and m.group(1).strip() not in ZERO:
            return prop + ": " + m.group(1).strip()
    m = re.search(r"(?<![\w-])margin\s*:\s*([^;]+);", body)
    if m:
        vals = m.group(1).split()
        top = vals[0] if vals else "0"
        bottom = vals[2] if len(vals) >= 3 else top
        if top not in ZERO or bottom not in ZERO:
            return "margin: " + m.group(1).strip()
    return None


def vertical_padding_offender(body):
    """Return the offending value if a `padding` shorthand sets a top/bottom
    that is neither 0 nor a --ia-space-* scale token, else None. (Horizontal is
    the --ia-section-pad-x token and is checked separately.)"""
    m = re.search(r"(?<![\w-])padding\s*:\s*([^;]+);", body)
    if not m:
        return None
    vals = m.group(1).split()  # token values have no spaces (var(...) / 0)
    if not vals:
        return None
    top = vals[0]
    bottom = vals[2] if len(vals) >= 3 else top
    for side in (top, bottom):
        if side in ("0", "0px") or side.startswith(SCALE_PREFIX):
            continue
        return "padding vertical `" + side + "`"
    return None


def main():
    html = open(INDEX, encoding="utf-8").read()
    css = css_of(html)
    rule_list = list(rules(css))

    errors = []

    if "--ia-section-max:" not in css:
        errors.append("--ia-section-max is not defined in :root.")
    if "--ia-section-pad-x:" not in css:
        errors.append("--ia-section-pad-x is not defined in :root.")
    for tok in SCALE_TOKENS:
        if tok + ":" not in css:
            errors.append(f"{tok} (vertical scale) is not defined in :root.")

    sections = section_classes(rule_list)
    if not sections:
        print(f"::error:: could not find the translucent-background rule "
              f"({BG_MARKER!r}) in index.html — has the section system moved?")
        return 1

    # bare single-selector rules grouped by class
    by_class = {}
    for sel, body in rule_list:
        s = sel.strip()
        if s in sections:  # exact single-selector rule (skips ".a, .b" groups)
            by_class.setdefault(s, []).append(body)

    for cls in sections:
        bodies = by_class.get(cls, [])
        if not bodies:
            errors.append(f"{cls}: no standalone rule found to carry the "
                          f"container contract.")
            continue
        joined = "\n".join(bodies)

        if cls not in EXEMPT_CONTAINER:
            if MAX_TOKEN not in joined:
                errors.append(f"{cls}: missing `max-width: {MAX_TOKEN}` — use "
                              f"the shared container so it can't drift "
                              f"horizontally.")
            if PADX_TOKEN not in joined:
                errors.append(f"{cls}: missing `{PADX_TOKEN}` in padding — inset "
                              f"with the shared token, not a literal/zero.")
            for body in bodies:
                off = vertical_padding_offender(body)
                if off:
                    errors.append(f"{cls}: {off} is off the vertical scale — "
                                  f"use a --ia-space-* token (or 0).")

        if cls not in ALLOW_VMARGIN:
            for body in bodies:
                off = vertical_margin_offender(body)
                if off:
                    errors.append(f"{cls}: spaces itself with a vertical margin "
                                  f"(`{off}`) — over the fixed globe canvas that "
                                  f"opens a transparent seam. Use padding so the "
                                  f"box tiles with its neighbours.")

    if errors:
        for e in errors:
            print(f"::error file=index.html:: {e}")
        print(f"::error:: {len(errors)} homepage section-rhythm issue(s) — see "
              f"scripts/check_section_rhythm.py for the contract.")
        return 1

    checked = ", ".join(sorted(sections))
    print(f"OK — {len(sections)} homepage sections share the container token, "
          f"sit on the vertical scale, and tile without globe seams ({checked}).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
