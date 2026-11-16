from collective.venue import PACKAGE_NAME
from importlib.util import find_spec


# configure.zcml registers a different default profile when the optional
# geolocation extra is installed.
HAS_GEOLOCATION = find_spec("collective.geolocationbehavior") is not None


class TestSetupInstall:
    def test_addon_installed(self, installer):
        """Test if collective.venue is installed."""
        assert installer.is_product_installed(PACKAGE_NAME) is True

    def test_browserlayer(self, browser_layers):
        """Test that IVenueLayer is registered."""
        from collective.venue.interfaces import IVenueLayer

        assert IVenueLayer in browser_layers

    def test_latest_version(self, profile_last_version):
        """Test latest version of default profile."""
        expected = "2" if HAS_GEOLOCATION else "1"
        assert profile_last_version(f"{PACKAGE_NAME}:default") == expected
