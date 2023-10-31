"""Test Jinja filters."""

from cloud_storage.common import format_file_size


class TestFilters:
    """Collection of test suits for all Jinja filters."""

    def test_format_file_size(self):
        """Verifies `format_file_size` filter."""
        assert format_file_size("0") == "-"
        assert format_file_size("12") == "12.0 B"
        assert format_file_size("123") == "123.0 B"
        assert format_file_size("1234") == "1.2 kB"
        assert format_file_size("123456789") == "123.5 MB"
