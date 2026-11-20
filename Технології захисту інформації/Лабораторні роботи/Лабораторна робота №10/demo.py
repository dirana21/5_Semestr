"""Порівняння власного LSB і Stegano на одному тестовому PNG."""

import json
from pathlib import Path

from PIL import Image, ImageDraw
from stegano import lsb

import lsb_manual


def create_cover() -> Image.Image:
    """Створити тестове зображення без зовнішніх файлів."""
    image = Image.new("RGB", (256, 160), (121, 160, 205))
    draw = ImageDraw.Draw(image)
    for y in range(1, 112):
        draw.line((0, y, 255, y), fill=(121 + y, 160 + y // 2, 205 + y // 4))
    draw.ellipse((174, 18, 215, 59), fill=(255, 227, 145))
    draw.polygon(
        [(0, 117), (77, 50), (157, 120), (217, 78), (255, 111), (255, 159), (0, 159)],
        fill=(58, 100, 123),
    )
    draw.polygon(
        [(0, 128), (54, 103), (120, 134), (191, 97), (255, 126), (255, 159), (0, 159)],
        fill=(35, 76, 91),
    )
    return image


def report_result(
    cover: Image.Image,
    output: Path,
    recovered: str,
    original: str,
    is_json: bool,
) -> None:
    if recovered != original:
        raise RuntimeError(f"{output.name}: відновлене повідомлення відрізняється.")
    with Image.open(output) as saved:
        if saved.size != cover.size or saved.mode != "RGB":
            raise RuntimeError(f"{output.name}: змінився розмір або режим PNG.")
        changes = [
            before ^ after
            for before, after in zip(cover.tobytes(), saved.tobytes(), strict=True)
        ]
    max_change = max(changes)
    if max_change > 1:
        raise RuntimeError(f"{output.name}: змінився старший біт каналу.")
    restored = json.dumps(json.loads(recovered), ensure_ascii=False) if is_json else recovered
    print(f"{output.name}: {restored}")
    print(f"  Збіг: так | змінено каналів: {sum(changes)} | max: {max_change}")


def main() -> None:
    output_dir = Path(__file__).resolve().parent / "result"
    output_dir.mkdir(exist_ok=True)
    cover_path = output_dir / "cover.png"
    cover = create_cover()
    cover.save(cover_path)

    print(f"Вхід: {cover_path.name}, RGB {cover.width} × {cover.height}")
    samples = {
        "text": "Привіт! Це повідомлення для ЛР №10.",
        "json": json.dumps({"робота": 10, "метод": "LSB"}, ensure_ascii=False),
    }
    for kind, original in samples.items():
        print(f"\n{kind.upper()} — {len(original.encode('utf-8'))} байтів UTF-8")
        manual_path = output_dir / f"manual-{kind}.png"
        lsb_manual.hide(cover, original).save(manual_path)
        with Image.open(manual_path) as saved:
            recovered = lsb_manual.reveal(saved)
            if kind == "text":
                print(f"Перший піксель: {cover.getpixel((0, 0))} → {saved.getpixel((0, 0))}")
        report_result(cover, manual_path, recovered, original, is_json=kind == "json")

        library_path = output_dir / f"stegano-{kind}.png"
        lsb.hide(str(cover_path), original).save(library_path)
        recovered = lsb.reveal(str(library_path))
        report_result(cover, library_path, recovered, original, is_json=kind == "json")


if __name__ == "__main__":
    main()
