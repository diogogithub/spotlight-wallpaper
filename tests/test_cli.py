#!/usr/bin/env python3
"""Offline tests for nested Spotlight JSON, image dimensions, and atomic updates."""
from __future__ import annotations

import contextlib
import importlib.machinery
import importlib.util
import io
import json
import struct
import subprocess
import sys
import tempfile
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
loader = importlib.machinery.SourceFileLoader("spotlight_cli", str(ROOT / "bin/spotlight-wallpaper"))
spec = importlib.util.spec_from_loader("spotlight_cli", loader)
assert spec is not None
module = importlib.util.module_from_spec(spec)
loader.exec_module(module)


def main() -> None:
    payload = {"batchrsp": {"items": [{"item": json.dumps({"ad": {
        "landscapeImage": {"asset": "https://example.invalid/landscape.jpg"},
        "portraitImage": {"asset": "https://example.invalid/portrait.jpg"},
    }})}]}}
    result = subprocess.run(
        ["python3", str(ROOT / "lib/extract_url.py")],
        input=json.dumps(payload).encode(), stdout=subprocess.PIPE, check=True,
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

    with tempfile.TemporaryDirectory() as d:
        target = Path(d) / "wallpaper.jpg"
        argv = ["spotlight-wallpaper", "--output", str(target), "--width", "3440", "--height", "1440"]
        def mock_fetch(url: str, _limit: int) -> bytes:
            return json.dumps(payload).encode() if url.startswith("https://arc.msn.com/") else png

        with patch.object(module, "fetch", side_effect=mock_fetch), patch.object(sys, "argv", argv):
            with contextlib.redirect_stdout(io.StringIO()):
                assert module.main() == 0
        assert target.read_bytes() == png

        with patch.object(module, "fetch", side_effect=lambda url, lim: b"<html>broken</html>"), patch.object(sys, "argv", argv):
            with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
                assert module.main() == 1
        assert target.read_bytes() == png, "A failed fetch replaced the last good image"


if __name__ == "__main__":
    main()
