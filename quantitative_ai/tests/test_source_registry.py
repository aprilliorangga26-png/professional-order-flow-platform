"""Tests for source metadata and registry behavior."""

import unittest
from datetime import datetime, timezone

from quantitative_ai.quantitative_ai.data.source_metadata import (
    DataProvenance,
    DataSourceSpec,
    build_xauusd_source,
)
from quantitative_ai.quantitative_ai.data.source_registry import (
    get_source,
    list_sources,
    register_source,
)


class SourceMetadataTests(unittest.TestCase):
    def test_normalizes_timeframe_alias_and_instrument(self) -> None:
        source = build_xauusd_source("custom", timeframe="4h", path="bars.csv")
        self.assertEqual(source.instrument, "XAUUSD")
        self.assertEqual(source.timeframe, "H4")

    def test_rejects_unknown_timeframe_instrument_and_timezone(self) -> None:
        with self.assertRaisesRegex(ValueError, "Unsupported timeframe"):
            DataSourceSpec("bad", "XAUUSD", "M90")
        with self.assertRaisesRegex(ValueError, "Unsupported instrument"):
            DataSourceSpec("bad", "EURUSD", "H1")
        with self.assertRaisesRegex(ValueError, "Invalid IANA timezone"):
            DataSourceSpec("bad", "XAUUSD", "H1", timezone="Not/AZone")

    def test_provenance_requires_timezone_aware_retrieval_time(self) -> None:
        with self.assertRaisesRegex(ValueError, "timezone-aware"):
            DataProvenance("vendor", datetime(2025, 1, 1))


class SourceRegistryTests(unittest.TestCase):
    def test_default_sources_include_research_timeframes(self) -> None:
        self.assertEqual(
            list_sources(),
            ["xauusd_d1_csv", "xauusd_h1_csv", "xauusd_h4_csv"],
        )
        self.assertEqual(get_source("xauusd_h4_csv").timeframe, "H4")

    def test_registration_rejects_duplicate_unless_replaced(self) -> None:
        spec = DataSourceSpec("test_registry_source", "XAUUSD", "H1")
        register_source(spec)
        with self.assertRaisesRegex(ValueError, "already registered"):
            register_source(spec)
        register_source(spec, replace=True)


if __name__ == "__main__":
    unittest.main()
