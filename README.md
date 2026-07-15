# Spotlight Wallpaper for GNU/Linux

A small, dependency-light command that downloads a Microsoft Spotlight
landscape image and atomically updates a wallpaper file.

## Requirements

- a POSIX shell;
- `curl`;
- Python 3 (standard library only);
- optionally, `file` for image-type validation.

## Usage

```sh
./bin/spotlight-wallpaper --output "$HOME/.local/share/backgrounds/spotlight.jpg"
```

The output, locale and country can also be set with `SPOTLIGHT_OUTPUT`,
`SPOTLIGHT_LOCALE`, and `SPOTLIGHT_COUNTRY`.

The script uses timeouts, rejects failed HTTP responses, checks that the
download is non-empty, validates its media type when `file` is available, and
only then replaces the configured wallpaper.

Use a systemd user timer, cron, or your desktop's startup facility to run it
periodically. Point the desktop or display manager at the same output path.

## Test

```sh
python3 tests/test_extract_url.py
```

The test is offline and uses a synthetic API fixture.

## History and attribution

The Microsoft endpoint was originally identified through KoalaBR's Spotlight
client, as documented in the earlier repository.

Microsoft Spotlight is a Microsoft service and can change or disappear without
notice. Images and their associated metadata remain subject to their respective
rights; this repository licenses only its own code.

## Licence

MIT. See `LICENSE`.
