#!/usr/bin/env python3
from __future__ import annotations

import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    result = subprocess.run(
        ["python3", str(ROOT / "lib" / "extract_url.py")],
        input=(ROOT / "tests" / "fixture.json").read_bytes(),
        stdout=subprocess.PIPE,
        check=True,
    )
    assert result.stdout.decode().strip() == "https://example.invalid/images/landscape.jpg"


if __name__ == "__main__":
    main()
