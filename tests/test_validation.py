import tempfile
import unittest
from pathlib import Path

import numpy as np

from src.labels import decode_mask, encode_mask, read_rgb, write_rgb
from src.validation import validate_dataset


class ValidationTests(unittest.TestCase):
    def test_valid_pair_is_cleaned(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            images = root / "images"
            masks = root / "masks"
            cleaned = root / "cleaned"
            images.mkdir()
            masks.mkdir()

            image = np.full((8, 8, 3), 120, dtype=np.uint8)
            class_ids = np.zeros((8, 8), dtype=np.uint8)
            class_ids[:, 4:] = 1
            mask = decode_mask(class_ids)
            mask[0, 0] = (1, 2, 3)
            write_rgb(images / "sample.jpg", image)
            write_rgb(masks / "sample.png", mask)

            result = validate_dataset(images, masks, cleaned)

            self.assertTrue(result.ok)
            self.assertEqual(len(result.warnings), 1)
            self.assertTrue((cleaned / "sample.png").exists())
            cleaned_ids, invalid = encode_mask(read_rgb(cleaned / "sample.png"))
            self.assertFalse(invalid.any())
            self.assertEqual(cleaned_ids[0, 0], 0)

    def test_missing_mask_fails(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            images = root / "images"
            masks = root / "masks"
            images.mkdir()
            masks.mkdir()
            write_rgb(images / "sample.jpg", np.zeros((8, 8, 3), dtype=np.uint8))

            result = validate_dataset(images, masks)

            self.assertFalse(result.ok)
            self.assertIn("missing PNG mask", result.errors[0])


if __name__ == "__main__":
    unittest.main()
