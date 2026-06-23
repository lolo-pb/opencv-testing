import unittest

import numpy as np

from src.labels import CLASS_COLORS_RGB, decode_mask, encode_mask


class LabelTests(unittest.TestCase):
    def test_round_trip_all_classes(self):
        class_ids = np.array([[0, 1], [2, 3]], dtype=np.uint8)
        encoded, invalid = encode_mask(decode_mask(class_ids))
        np.testing.assert_array_equal(encoded, class_ids)
        self.assertFalse(invalid.any())

    def test_invalid_color_becomes_unidentified(self):
        mask = CLASS_COLORS_RGB[[[0, 1], [2, 3]]].copy()
        mask[0, 0] = (12, 34, 56)
        encoded, invalid = encode_mask(mask)
        self.assertEqual(encoded[0, 0], 3)
        self.assertTrue(invalid[0, 0])


if __name__ == "__main__":
    unittest.main()
