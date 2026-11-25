"""Copy the entry line to the make.fun output directory.

Reads entry.txt sitting next to this script and writes its exact bytes
to <MAKEFUN_OUTPUT_DIR>/entry.txt, then verifies the copy with SHA-256.
Standard library only.
"""

import hashlib
import os
import sys
from pathlib import Path

MAX_CHARS = 200


def sha256_hex(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def main() -> int:
    here = Path(__file__).resolve().parent
    source = here / "entry.txt"
    if not source.is_file():
        print("error: entry.txt not found next to main.py", file=sys.stderr)
        return 1

    data = source.read_bytes()
    if not data:
        print("error: entry.txt is empty", file=sys.stderr)
        return 1

    text = data.decode("utf-8")
    if not text.strip():
        print("error: entry.txt contains only whitespace", file=sys.stderr)
        return 1
    if text != text.strip():
        print("error: entry has leading or trailing whitespace", file=sys.stderr)
        return 1
    if len(text) > MAX_CHARS:
        print(
            f"error: entry is {len(text)} characters, over the {MAX_CHARS} limit",
            file=sys.stderr,
        )
        return 1

    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    target = out_dir / "entry.txt"
    target.write_bytes(data)

    if sha256_hex(target.read_bytes()) != sha256_hex(data):
        print("error: output bytes do not match entry.txt", file=sys.stderr)
        return 1

    print(f"wrote {target} ({len(text)} chars, sha256 {sha256_hex(data)})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
