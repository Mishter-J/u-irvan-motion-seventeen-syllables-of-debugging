#!/usr/bin/env python3
"""Write one debugging haiku (5-7-5) to /output/entry.txt.

Deterministic: the haiku is a fixed string, so every run writes the
same bytes. No network, no secrets, no input files.
"""

import os

HAIKU = (
    "the cursor blinks, waits\n"
    "ask the logs what changed last night\n"
    "nothing changed but me"
)


def main() -> None:
    os.makedirs("/output", exist_ok=True)
    with open("/output/entry.txt", "w", encoding="utf-8", newline="") as f:
        f.write(HAIKU)


if __name__ == "__main__":
    main()
