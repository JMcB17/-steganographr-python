import unittest

import steganographr


class TestSteganographr(unittest.TestCase):
    def test_wrap(self):
        original = "test"
        wrapped = steganographr.wrap(original)

        self.assertEqual(wrapped.split("\uFEFF"), ["", "test", ""])

        unwrapped = steganographr.unwrap(wrapped)
        self.assertEqual(original, unwrapped)

    def test_encode(self):
        public = "hello world"
        private = "never gonna give you up"
        encoded = steganographr.encode(public, private)
        decoded = steganographr.decode(encoded)

        self.assertEqual(private, decoded)


if __name__ == "__main__":
    unittest.main()
