#!/usr/bin/env python3
"""Write one debugging haiku (5-7-5) to /output/entry.txt.

Deterministic: the haiku is a fixed string, so every run writes the
same bytes. No network, no secrets, no input files.
"""

import os
import re

HAIKU = (
    "the cursor blinks, waits\n"
    "ask the logs what changed last night\n"
    "nothing changed but me"
)

# Expected syllable counts per line (5-7-5).
EXPECTED_SYLLABLES = (5, 7, 5)


def _syllables(word: str) -> int:
    """Rough syllable count: vowel groups, with a silent trailing 'e' dropped."""
    w = re.sub(r"[^a-z]", "", word.lower())
    if not w:
        return 0
    if w.endswith("e") and len(w) > 2 and not w.endswith("le"):
        w = w[:-1]
    elif w.endswith("ed") and len(w) > 3 and w[-3] not in "td":
        # Silent 'e' before a final 'd' (e.g. "changed" -> "changd").
        w = w[:-2] + "d"
    return max(1, len(re.findall(r"[aeiouy]+", w)))


def _validate(text: str) -> None:
    """Fail loudly instead of shipping an entry the gate would score 0."""
    if not 1 <= len(text) <= 200:
        raise SystemExit(f"entry is {len(text)} characters, must be 1..200")
    lines = text.split("\n")
    if len(lines) != 3:
        raise SystemExit(f"entry has {len(lines)} lines, must be 3")
    for line, expected in zip(lines, EXPECTED_SYLLABLES):
        got = sum(_syllables(w) for w in line.split())
        if got != expected:
            raise SystemExit(
                f"line {line!r} has {got} syllables, expected {expected}"
            )


def main() -> None:
    _validate(HAIKU)
    os.makedirs("/output", exist_ok=True)
    with open("/output/entry.txt", "w", encoding="utf-8", newline="") as f:
        f.write(HAIKU)


if __name__ == "__main__":
    main()
