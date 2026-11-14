"""Tests for the explicit multi-timeframe bundle contract."""

import unittest

from quantitative_ai.quantitative_ai.data.dataset_bundle import build_default_research_bundle
from quantitative_ai.quantitative_ai.data.source_metadata import DataSourceSpec


class DatasetBundleTests(unittest.TestCase):
    def test_bundle_requires_declared_sources(self) -> None:
        with self.assertRaisesRegex(ValueError, "at least one source spec"):
            build_default_research_bundle(source_specs=())

    def test_bundle_accepts_research_timeframes(self) -> None:
        sources = (
            DataSourceSpec("xauusd_h4", "XAUUSD", "H4"),
            DataSourceSpec("xauusd_h1", "XAUUSD", "H1"),
            DataSourceSpec("xauusd_d1", "XAUUSD", "D1"),
        )
        bundle = build_default_research_bundle(name="gold_bundle", source_specs=sources)
        self.assertEqual(bundle.primary_timeframe, "H4")
        self.assertEqual(bundle.confirmation_timeframes, ("H1", "D1"))
        self.assertTrue(bundle.contains_timeframe("4h"))
        self.assertEqual(len(bundle.sources_for_timeframe("D1")), 1)

    def test_bundle_rejects_duplicate_source_names(self) -> None:
        sources = (
            DataSourceSpec("dup", "XAUUSD", "H4"),
            DataSourceSpec("dup", "XAUUSD", "H1"),
        )
        with self.assertRaisesRegex(ValueError, "Duplicate source name"):
            build_default_research_bundle(source_specs=sources)


if __name__ == "__main__":
    unittest.main()
