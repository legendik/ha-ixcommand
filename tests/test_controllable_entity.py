"""Tests for controllable entity."""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))


class TestControllableEntityLogic:
    """Test cases for controllable entity logic (without full HA mocking)."""

    def test_control_update_delay_constant(self):
        """Test that control update delay is defined."""
        from custom_components.ixcommand.controllable_entity import CONTROL_UPDATE_DELAY
        assert CONTROL_UPDATE_DELAY == 2

    def test_property_key_constants(self):
        """Test property key constants are defined."""
        from custom_components.ixcommand.const import (
            PROP_CHARGING_ENABLE,
            PROP_TARGET_CURRENT,
            PROP_SINGLE_PHASE,
            PROP_MAXIMUM_CURRENT,
            PROP_BOOST_CURRENT,
            PROP_BOOST_TIME,
        )
        # These should be strings
        assert isinstance(PROP_CHARGING_ENABLE, str)
        assert isinstance(PROP_TARGET_CURRENT, str)
        assert isinstance(PROP_SINGLE_PHASE, str)


if __name__ == "__main__":
    import pytest
    pytest.main([__file__, "-v"])
