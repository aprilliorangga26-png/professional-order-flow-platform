"""Tests for source metadata and registry validation."""

import unittest

from quantitative_ai.data.source_metadata import DataSourceSpec, build_xauusd_source
from quantitative_ai.data.source_registry import get_source, list_sources


class SourceMetadataTests(unittest.TestCase):
    def test_build_xauusd_source_uses_supported_timeframe(self) -> None:
        source = build_xauusd_source("xauusd_h4", timeframe="4h")
        self.assertEqual(source.instrument, "XAUUSD")
        self.assertEqual(source.timeframe, "H4")
        self.assertEqual(source.timezone, "UTC")

    def test_invalid_timeframe_is_rejected(self) -> None:
        with self.assertRaisesRegex(ValueError, "Unsupported timeframe"):
            DataSourceSpec(name="bad", instrument="XAUUSD", timeframe="M90")

    def test_invalid_instrument_is_rejected(self) -> None:
        with self.assertRaisesRegex(ValueError, "Unsupported instrument"):
            DataSourceSpec(name="bad", instrument="EURUSD", timeframe="H1")


class SourceRegistryTests(unittest.TestCase):
    def test_known_source_is_available(self) -> None:
        source = get_source("xauusd_h4_csv")
        self.assertEqual(source.name, "xauusd_h4_csv")
        self.assertEqual(source.timeframe, "H4")

    def test_list_sources_is_sorted(self) -> None:
        self.assertEqual(list_sources(), ["xauusd_d1_csv", "xauusd_h1_csv", "xauusd_h4_csv"])


if __name__ == "__main__":
    unittest.main()
