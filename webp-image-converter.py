from pathlib import Path
from PIL import Image

# Image extensions to convert
SUPPORTED_EXTENSIONS = {
    ".jpg",
    ".jpeg",
    ".png",
    ".bmp",
    ".gif",
    ".tif",
    ".tiff",
    ".ico",
}

# True = No quality loss
LOSSLESS = True

# Used only if LOSSLESS = False
QUALITY = 100

# Compression effort (0-6)
METHOD = 6


def convert_image(image_path: Path):
    output_path = image_path.with_suffix(".webp")

    # Skip if already converted
    if output_path.exists():
        print(f"Skipped: {output_path}")
        return

    try:
        with Image.open(image_path) as img:

            # Preserve transparency
            if img.mode not in ("RGB", "RGBA"):
                if "A" in img.getbands():
                    img = img.convert("RGBA")
                else:
                    img = img.convert("RGB")

            if LOSSLESS:
                img.save(
                    output_path,
                    "WEBP",
                    lossless=True,
                    method=METHOD,
                )
            else:
                img.save(
                    output_path,
                    "WEBP",
                    quality=QUALITY,
                    method=METHOD,
                )
            
            image_path.unlink()

        print(f"Converted: {image_path} -> {output_path}")

    except Exception as e:
        print(f"Failed: {image_path}")
        print(e)


def main():
    current_dir = Path.cwd()

    print(f"Scanning: {current_dir}\n")

    count = 0

    for file in current_dir.rglob("*"):
        if file.is_file() and file.suffix.lower() in SUPPORTED_EXTENSIONS:
            convert_image(file)
            count += 1

    print(f"\nDone! Processed {count} image(s).")


if __name__ == "__main__":
    main()