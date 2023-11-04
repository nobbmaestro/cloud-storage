"""Test Helper functions."""

from cloud_storage.common import purge_list, validate_password


class TestHelpers:
    """Collection of test suits for all helper functions."""

    _password_len = 10

    def test_validate_password(self):
        """Verifies `validate_password` helper."""
        # Fails on empty string (insufficient length)
        assert not validate_password("")

        # Fails due to missing digit, uppercase and special char
        assert not validate_password("abcdefghij")

        # Fails due to missing uppercase and special char
        assert not validate_password("abcdefghi1")

        # Fails due to missing special char
        assert not validate_password("Abcdefghi1")

        # Passes if length sufficient and digit, uppercase and special char exists
        assert validate_password("Abcdefgh1$")

    def test_purge_list(self):
        """Verifies `purge_list` helper."""
        # Func handles empty lists
        assert purge_list([]) == []

        # Func handles empty strings
        assert purge_list(["", ""]) == []

        # Func purges only empty strings
        assert purge_list(["a", ""]) == ["a"]

        # Func purges non-meaningful strings
        assert purge_list(["", '""']) == []
