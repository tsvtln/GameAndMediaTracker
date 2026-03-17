#!/usr/bin/env python3
"""
CSS deduplicator — removes fighting/duplicate declarations.

For each selector block:
  1. If a property appears more than once, keep only the LAST value (what the browser uses anyway)
  2. If the same selector appears multiple times, merge into one block (later values win)

Usage: python3 css_dedup.py input.css > cleaned.css
       python3 css_dedup.py input.css --in-place
"""

import re
import sys
from collections import OrderedDict


def tokenize_css(css):
    """Split CSS into (selector, declarations_block) pairs, preserving @rules and comments."""
    tokens = []
    css = re.sub(r'/\*.*?\*/', '', css, flags=re.DOTALL)  # strip comments
    pos = 0
    while pos < len(css):
        # skip whitespace
        m = re.match(r'\s+', css[pos:])
        if m:
            pos += m.end()
            continue
        # @keyframes / @media — grab entire nested block
        m = re.match(r'(@(?:keyframes|media|supports|font-face)[^{]*)\{', css[pos:])
        if m:
            # find matching closing brace (handles nesting)
            start = pos + m.end()
            depth = 1
            i = start
            while i < len(css) and depth > 0:
                if css[i] == '{': depth += 1
                elif css[i] == '}': depth -= 1
                i += 1
            block = css[pos:i]
            tokens.append(('__raw__', block))
            pos = i
            continue
        # @import and other single-line @rules
        m = re.match(r'@[^{;]+;', css[pos:])
        if m:
            tokens.append(('__raw__', m.group()))
            pos += m.end()
            continue
        # normal rule: selector { declarations }
        m = re.match(r'([^{}]+?)\{([^}]*)\}', css[pos:])
        if m:
            selector = m.group(1).strip()
            declarations = m.group(2).strip()
            tokens.append((selector, declarations))
            pos += m.end()
            continue
        # skip any stray character
        pos += 1
    return tokens


def dedup_declarations(decl_str):
    """Remove duplicate properties in a declaration block, keeping the last."""
    props = OrderedDict()
    for line in decl_str.split(';'):
        line = line.strip()
        if not line or ':' not in line:
            continue
        # split on first colon only (values can contain colons like url())
        key, val = line.split(':', 1)
        key = key.strip()
        val = val.strip()
        if key in props and props[key] != val:
            pass  # will overwrite — later wins
        props[key] = val
    return props


def rebuild(props):
    """Turn an OrderedDict of properties back into a declaration block."""
    lines = [f"    {k}: {v};" for k, v in props.items()]
    return '\n'.join(lines)


def dedup_css(css_text):
    tokens = tokenize_css(css_text)

    # merge duplicate selectors — later values win, order preserved by first appearance
    merged = OrderedDict()
    raw_order = []  # track insertion order including raw blocks

    for selector, content in tokens:
        if selector == '__raw__':
            raw_order.append(('__raw__', content))
        else:
            norm = normalize_selector(selector)
            if norm not in merged:
                raw_order.append(('rule', norm))
                merged[norm] = OrderedDict()
            # merge properties — later wins
            props = dedup_declarations(content)
            merged[norm].update(props)

    # rebuild
    parts = []
    seen = set()
    for kind, val in raw_order:
        if kind == '__raw__':
            parts.append(val)
        else:
            if val in seen:
                continue
            seen.add(val)
            props = merged[val]
            if props:
                parts.append(f"{val} {{\n{rebuild(props)}\n}}")

    return '\n\n'.join(parts) + '\n'


def normalize_selector(sel):
    """Normalize whitespace in selector for comparison."""
    return re.sub(r'\s+', ' ', sel).strip()


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 css_dedup.py <file.css> [--in-place]", file=sys.stderr)
        sys.exit(1)

    path = sys.argv[1]
    in_place = '--in-place' in sys.argv

    with open(path, 'r') as f:
        css = f.read()

    result = dedup_css(css)

    if in_place:
        with open(path, 'w') as f:
            f.write(result)
        # count savings
        before = len(css.split('\n'))
        after = len(result.split('\n'))
        removed = before - after
        print(f"Cleaned {path}: {before} -> {after} lines ({removed} removed)", file=sys.stderr)
    else:
        print(result)


if __name__ == '__main__':
    main()
