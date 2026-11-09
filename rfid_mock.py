"""
Mock RFID middleware.
This simulates RFID tag input without physical hardware.
"""


def read_rfid_tag(tag_value):
    """Read and validate a simulated RFID tag."""

    if not tag_value:
        raise ValueError("RFID tag cannot be empty.")

    tag_value = str(tag_value).strip().upper()

    if not tag_value:
        raise ValueError("RFID tag cannot be empty.")

    return tag_value


def write_rfid_tag(tag_value):
    """Prepare an RFID tag value for registration."""
    return read_rfid_tag(tag_value)


def check_rfid_connection():
    """Return the status of the mock RFID reader."""
    return {
        "connected": True,
        "reader_type": "Mock RFID Reader",
        "message": "RFID mock service is running."
    }