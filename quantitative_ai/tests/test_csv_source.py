"""Tests for CSV source adapter provenance and timezone checks."""

import io
import unittest
from datetime import datetime, timezone

from quantitative_ai.quantitative_ai.data.csv_source import load_source_csv
from quantitative_ai.quantitative_ai.data.source_metadata import DataProvenance, DataSourceSpec
from quantitative_ai.quantitative_ai.data.validation import DataValidationError


CSV = (
    "timestamp,open,high,low,close,volume\n"
    "2025-01-01T00:00:00Z,2000,2020,1990,2010,5\n"
    "2025-01-02T00:00:00Z,2010,2030,2000,2025,6\n"
)
PROVENANCE = DataProvenance(
    provider="owner-supplied test fixture",
    retrieved_at=datetime(2025, 1, 3, tzinfo=timezone.utc),
    dataset_revision="test-v1",
)


class CsvSourceTests(unittest.TestCase):
    def test_loads_csv_with_provenance(self) -> None:
        spec = DataSourceSpec("fixture", "XAUUSD", "H1", provenance=PROVENANCE)
        self.assertEqual(len(load_source_csv(spec, io.StringIO(CSV))), 2)

    def test_requires_provenance_by_default(self) -> None:
        spec = DataSourceSpec("fixture", "XAUUSD", "H1")
        with self.assertRaisesRegex(DataValidationError, "missing provenance"):
            load_source_csv(spec, io.StringIO(CSV))

    def test_can_disable_provenance_requirement_explicitly(self) -> None:
        spec = DataSourceSpec("fixture", "XAUUSD", "H1")
        self.assertEqual(
            len(load_source_csv(spec, io.StringIO(CSV), require_provenance=False)), 2
        )

    def test_rejects_non_csv_source(self) -> None:
        spec = DataSourceSpec(
            "fixture", "XAUUSD", "H1", source_type="api", provenance=PROVENANCE
        )
        with self.assertRaisesRegex(DataValidationError, "not 'csv'"):
            load_source_csv(spec, io.StringIO(CSV))

    def test_rejects_timestamp_not_matching_declared_zone(self) -> None:
        spec = DataSourceSpec(
            "fixture", "XAUUSD", "H1", timezone="America/New_York", provenance=PROVENANCE
        )
        with self.assertRaisesRegex(DataValidationError, "does not match source timezone"):
            load_source_csv(spec, io.StringIO(CSV))


if __name__ == "__main__":
    unittest.main()
