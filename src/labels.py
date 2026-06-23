from pathlib import Path

import cv2
import numpy as np


CLASS_NAMES = ("fiber", "resin", "pore", "unidentified")
CLASS_COLORS_RGB = np.array(
    [
        (255, 0, 0),
        (0, 255, 0),
        (0, 0, 255),
        (0, 0, 0),
    ],
    dtype=np.uint8,
)
UNIDENTIFIED_ID = 3


def read_rgb(path: Path | str) -> np.ndarray:
    image = cv2.imread(str(path), cv2.IMREAD_COLOR)
    if image is None:
        raise ValueError(f"Could not read image: {path}")
    return cv2.cvtColor(image, cv2.COLOR_BGR2RGB)


def write_rgb(path: Path | str, image: np.ndarray) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    cv2.imwrite(str(path), cv2.cvtColor(image, cv2.COLOR_RGB2BGR))


def encode_mask(mask_rgb: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    matches = np.all(
        mask_rgb[:, :, None, :] == CLASS_COLORS_RGB[None, None, :, :],
        axis=3,
    )
    valid = np.any(matches, axis=2)
    class_ids = np.argmax(matches, axis=2).astype(np.uint8)
    class_ids[~valid] = UNIDENTIFIED_ID
    return class_ids, ~valid


def decode_mask(class_ids: np.ndarray) -> np.ndarray:
    return CLASS_COLORS_RGB[class_ids]
