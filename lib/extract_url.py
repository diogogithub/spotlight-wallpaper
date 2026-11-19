#!/usr/bin/env python3
"""Extract landscape-image URLs from Spotlight JSON, including nested item strings."""
from __future__ import annotations

import json
import sys
from collections.abc import Iterable


def strings(value: object, path: tuple[str, ...] = (), depth: int = 0) -> Iterable[tuple[tuple[str, ...], str]]:
    if isinstance(value, dict):
        for key, child in value.items():
            yield from strings(child, (*path, str(key).lower()), depth)
    elif isinstance(value, list):
        for child in value:
            yield from strings(child, path, depth)
    elif isinstance(value, str):
        normalized = value.replace("\\/", "/")
        if depth < 3 and normalized.lstrip().startswith(("{", "[")):
            try:
                nested = json.loads(normalized)
            except json.JSONDecodeError:
                pass
            else:
                yield from strings(nested, path, depth + 1)
                return
        yield path, normalized


def score(path: tuple[str, ...], value: str) -> int:
    lowered = value.lower()
    if not lowered.startswith("https://"):
        return -1
    joined = ".".join(path)
    points = 0
    if "landscape" in joined or "landscape" in lowered:
        points += 12
    if "image" in joined or "image" in lowered:
        points += 5
    if "asset" in joined or "url" in joined or joined.endswith(".u"):
        points += 3
    if "binary" in lowered:
        points += 3
    if any(lowered.split("?", 1)[0].endswith(ext) for ext in (".jpg", ".jpeg", ".png", ".webp")):
        points += 4
    if "thumbnail" in joined or "portrait" in joined:
        points -= 20
    return points


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except (json.JSONDecodeError, UnicodeDecodeError) as exc:
        print(f"Invalid Spotlight JSON: {exc}", file=sys.stderr)
        return 2
    candidates = [(score(path, url), url) for path, url in strings(payload)]
    candidates = [item for item in candidates if item[0] >= 5]
    if not candidates:
        return 1
    candidates.sort(key=lambda item: item[0], reverse=True)
    print(candidates[0][1])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
