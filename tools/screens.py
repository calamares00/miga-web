"""Turns the app's screenshots into the website's phone screens (assets/img/screens/<lang>/*.webp).

The screenshots come from StoreShotsEsTest and StoreShotsEnTest in calamares00/miga-app: the real
app, with recipe packs from miga-packs installed, driven through its interface. Run them with

    MIGA_SHOTS_DIR=/tmp/shots/es MIGA_PACKS_DIST=<miga-packs>/dist \\
        ./gradlew recordRoborazziDebug --tests '*StoreShotsEsTest'

(and the same with "en"), then

    python3 tools/screens.py /tmp/shots

Needs Pillow.
"""
import sys
from pathlib import Path

from PIL import Image

OUT = Path(__file__).resolve().parent.parent / "assets" / "img" / "screens"
WIDTH = 720  # Twice the widest phone on the page, for sharp screens on high-density displays.


def main():
    source = Path(sys.argv[1])
    for lang in ("es", "en"):
        target = OUT / lang
        target.mkdir(parents=True, exist_ok=True)
        for png in sorted((source / lang).glob("[0-9]*.png")):
            image = Image.open(png).convert("RGB")
            height = round(image.height * WIDTH / image.width)
            name = png.stem.split("_", 1)[1]
            image.resize((WIDTH, height), Image.LANCZOS).save(target / f"{name}.webp", "WEBP", quality=82, method=6)
            print(target / f"{name}.webp")


if __name__ == "__main__":
    main()
