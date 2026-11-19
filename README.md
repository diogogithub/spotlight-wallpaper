# Spotlight Wallpaper for GNU/Linux

Download a Microsoft Spotlight landscape image to a stable local file. The Python 3 client uses only the standard library, rejects invalid or undersized images, and replaces the previous wallpaper atomically. If Microsoft does not supply a valid image, the previous file is untouched.

## Usage

```sh
./bin/spotlight-wallpaper --output "$HOME/.local/share/backgrounds/spotlight.jpg" \
  --width 3440 --height 1440 --min-width 1600 --min-height 900
```

Resolution arguments request an appropriately sized image from Microsoft and define the minimum acceptable image. The service can still return a 16:9 picture for an ultrawide monitor. Your desktop wallpaper setter controls whether to crop it or show borders.

Environment overrides: `SPOTLIGHT_OUTPUT`, `SPOTLIGHT_WIDTH`, `SPOTLIGHT_HEIGHT`, `SPOTLIGHT_MIN_WIDTH`, `SPOTLIGHT_MIN_HEIGHT`, `SPOTLIGHT_LOCALE` and `SPOTLIGHT_COUNTRY`.

This client only downloads images; it does not change the active wallpaper. Use a compositor-aware wallpaper setter such as `feh --bg-fill` on X11, and a systemd user timer for periodic updates.

## Test

```sh
python3 tests/test_extract_url.py
python3 tests/test_cli.py
```

These tests work offline. Microsoft endpoints and image availability may change.

## License

MIT for this project's code. Spotlight images belong to their respective rights holders.
