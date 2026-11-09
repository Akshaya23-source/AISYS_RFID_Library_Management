import unittest

from app.services.rfid_mock import (
    read_rfid_tag,
    check_rfid_connection
)


class TestRFIDMock(unittest.TestCase):

    def test_read_rfid_tag(self):
        result = read_rfid_tag("rfid001")
        self.assertEqual(result, "RFID001")

    def test_remove_extra_spaces(self):
        result = read_rfid_tag("  rfid002  ")
        self.assertEqual(result, "RFID002")

    def test_empty_rfid_tag(self):
        with self.assertRaises(ValueError):
            read_rfid_tag("")

    def test_rfid_connection(self):
        result = check_rfid_connection()
        self.assertTrue(result["connected"])
        self.assertEqual(
            result["reader_type"],
            "Mock RFID Reader"
        )


if __name__ == "__main__":
    unittest.main()