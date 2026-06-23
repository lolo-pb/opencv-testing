from dataclasses import dataclass
from pathlib import Path

import numpy as np

from src.labels import (
    decode_mask,
    encode_mask,
    read_rgb,
    repair_invalid_colors,
    write_rgb,
)


IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".tif", ".tiff", ".webp"}


@dataclass(frozen=True)
class Pair:
    name: str
    image_path: Path
    mask_path: Path


@dataclass
class ValidationResult:
    pairs: list[Pair]
    errors: list[str]
    warnings: list[str]

    @property
    def ok(self) -> bool:
        return not self.errors


def find_images(directory: Path) -> dict[str, Path]:
    return {
        path.stem: path
        for path in sorted(directory.iterdir())
        if path.is_file() and path.suffix.lower() in IMAGE_EXTENSIONS
    }


def validate_dataset(
    image_dir: Path,
    mask_dir: Path,
    clean_dir: Path | None = None,
) -> ValidationResult:
    images = find_images(image_dir)
    masks = {
        path.stem: path
        for path in sorted(mask_dir.glob("*.png"))
        if path.is_file()
    }
    errors: list[str] = []
    warnings: list[str] = []
    pairs: list[Pair] = []

    for name in sorted(images.keys() - masks.keys()):
        errors.append(f"{name}: missing PNG mask")
    for name in sorted(masks.keys() - images.keys()):
        errors.append(f"{name}: mask has no matching image")

    for name in sorted(images.keys() & masks.keys()):
        image_path = images[name]
        mask_path = masks[name]
        image = read_rgb(image_path)
        mask = read_rgb(mask_path)

        if image.shape[:2] != mask.shape[:2]:
            errors.append(
                f"{name}: image is {image.shape[1]}x{image.shape[0]}, "
                f"mask is {mask.shape[1]}x{mask.shape[0]}"
            )
            continue

        class_ids, invalid = encode_mask(mask)
        invalid_count = int(invalid.sum())
        valid_ratio = 1.0 - invalid_count / invalid.size
        mean_difference = float(
            np.mean(np.abs(image.astype(np.int16) - mask.astype(np.int16)))
        )

        if valid_ratio < 0.5:
            errors.append(
                f"{name}: only {valid_ratio:.1%} of mask pixels use valid colors; "
                "this does not look like a painted mask"
            )
            continue
        if mean_difference < 5:
            errors.append(f"{name}: mask appears to be a copy of the original image")
            continue

        if invalid_count:
            class_ids = repair_invalid_colors(class_ids, invalid)
            warnings.append(
                f"{name}: repaired {invalid_count} invalid-color pixels from "
                "surrounding fiber/resin/pore colors"
            )

        cleaned_path = clean_dir / f"{name}.png" if clean_dir else mask_path
        if clean_dir:
            write_rgb(cleaned_path, decode_mask(class_ids))
        pairs.append(Pair(name, image_path, cleaned_path))

    return ValidationResult(pairs, errors, warnings)
