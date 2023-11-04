"""Test Jinja filters."""

from cloud_storage.common import pretty_file_size_format


class TestFilters:
    """Collection of test suits for all Jinja filters."""

    def test_format_file_size(self):
        """Verifies `format_file_size` filter."""
        assert pretty_file_size_format("0") == "-"
        assert pretty_file_size_format("12") == "12.0 B"
        assert pretty_file_size_format("123") == "123.0 B"
        assert pretty_file_size_format("1234") == "1.2 kB"
        assert pretty_file_size_format("123456789") == "123.5 MB"
