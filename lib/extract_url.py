#!/usr/bin/env python3
"""Extract the best landscape-image URL from a Spotlight JSON response."""

from __future__ import annotations

import json
import sys
from collections.abc import Iterable


def strings(value: object, path: tuple[str, ...] = ()) -> Iterable[tuple[tuple[str, ...], str]]:
    if isinstance(value, dict):
        for key, child in value.items():
            yield from strings(child, (*path, str(key).lower()))
    elif isinstance(value, list):
        for child in value:
            yield from strings(child, path)
    elif isinstance(value, str):
        yield path, value.replace("\\/", "/")


def score(path: tuple[str, ...], value: str) -> int:
    lowered = value.lower()
    if not lowered.startswith("https://"):
        return -1
    joined = ".".join(path)
    points = 0
    if "landscape" in joined or "landscape" in lowered:
        points += 8
    if "image" in joined or "image" in lowered:
        points += 5
    if "url" in joined:
        points += 3
    if "binary" in lowered:
        points += 3
    if any(lowered.split("?", 1)[0].endswith(ext) for ext in (".jpg", ".jpeg", ".png", ".webp")):
        points += 4
    return points


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except (json.JSONDecodeError, UnicodeDecodeError) as exc:
        print(f"Invalid Spotlight JSON: {exc}", file=sys.stderr)
        return 2

    candidates = [(score(path, value), value) for path, value in strings(payload)]
    candidates = [candidate for candidate in candidates if candidate[0] >= 5]
    if not candidates:
        return 1
    candidates.sort(key=lambda item: item[0], reverse=True)
    print(candidates[0][1])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
