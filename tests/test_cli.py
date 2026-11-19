#!/usr/bin/env python3
from __future__ import annotations

import importlib.machinery
import importlib.util
import json
import struct
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
loader = importlib.machinery.SourceFileLoader("spotlight_cli", str(ROOT / "bin/spotlight-wallpaper"))
spec = importlib.util.spec_from_loader("spotlight_cli", loader)
assert spec is not None
module = importlib.util.module_from_spec(spec)
loader.exec_module(module)


def main() -> None:
    payload = {"batchrsp": {"items": [{"item": json.dumps({"ad": {
        "landscapeImage": {"asset": "https://example.invalid/landscape.jpg"},
        "portraitImage": {"asset": "https://example.invalid/portrait.jpg"}
    }})}]}}
    result = subprocess.run(
        ["python3", str(ROOT / "lib/extract_url.py")],
        input=json.dumps(payload).encode(), stdout=subprocess.PIPE, check=True
    )
    assert result.stdout.decode().strip() == "https://example.invalid/landscape.jpg"
    png = b"\x89PNG\r\n\x1a\n" + struct.pack(">I", 13) + b"IHDR" + struct.pack(">II", 2560, 1440)
    assert module.image_size(png) == (2560, 1440)
    try:
        module.image_size(b"<html>not an image</html>")
    except ValueError:
        pass
    else:
        raise AssertionError("Invalid image accepted")


if __name__ == "__main__":
    main()
