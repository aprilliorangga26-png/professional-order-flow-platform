"""Unit tests for OHLCV validation and CSV ingestion."""

import io
import math
import unittest
from datetime import datetime, timezone

from quantitative_ai.data.csv_loader import load_ohlcv_csv
from quantitative_ai.data.validation import (
    DataValidationError,
    validate_bar,
    validate_bars,
)
from quantitative_ai.models import OHLCVBar


def bar(timestamp: datetime | None = None, **overrides: float) -> OHLCVBar:
    values = {"open": 2000.0, "high": 2020.0, "low": 1990.0, "close": 2010.0, "volume": 10.0}
    values.update(overrides)
    return OHLCVBar(timestamp or datetime(2025, 1, 1, tzinfo=timezone.utc), **values)


class ValidateBarTests(unittest.TestCase):
    def test_accepts_valid_bar_and_zero_volume(self) -> None:
        validate_bar(bar(volume=0.0))

    def test_rejects_naive_timestamp(self) -> None:
        with self.assertRaisesRegex(DataValidationError, "timezone"):
            validate_bar(bar(datetime(2025, 1, 1)))

    def test_rejects_non_finite_price(self) -> None:
        with self.assertRaisesRegex(DataValidationError, "finite"):
            validate_bar(bar(close=math.nan))

    def test_rejects_non_positive_price(self) -> None:
        with self.assertRaisesRegex(DataValidationError, "greater than zero"):
            validate_bar(bar(open=0.0))

    def test_rejects_negative_volume(self) -> None:
        with self.assertRaisesRegex(DataValidationError, "negative"):
            validate_bar(bar(volume=-1.0))

    def test_rejects_inconsistent_high(self) -> None:
        with self.assertRaisesRegex(DataValidationError, "high"):
            validate_bar(bar(high=2005.0))

    def test_rejects_boolean_as_numeric(self) -> None:
        with self.assertRaisesRegex(DataValidationError, "numeric"):
            validate_bar(bar(volume=True))  # type: ignore[arg-type]


class ValidateBarsTests(unittest.TestCase):
    def test_requires_strictly_increasing_timestamps(self) -> None:
        first = bar()
        later = bar(datetime(2025, 1, 2, tzinfo=timezone.utc))
        self.assertEqual(validate_bars([first, later]), [first, later])

    def test_rejects_duplicate_timestamps(self) -> None:
        with self.assertRaisesRegex(DataValidationError, "duplicate timestamp"):
            validate_bars([bar(), bar()])

    def test_rejects_out_of_order_timestamps(self) -> None:
        with self.assertRaisesRegex(DataValidationError, "strictly increasing"):
            validate_bars([
                bar(datetime(2025, 1, 2, tzinfo=timezone.utc)),
                bar(datetime(2025, 1, 1, tzinfo=timezone.utc)),
            ])

    def test_does_not_infer_missing_interval(self) -> None:
        bars = [
            bar(datetime(2025, 1, 1, tzinfo=timezone.utc)),
            bar(datetime(2025, 1, 5, tzinfo=timezone.utc)),
        ]
        self.assertEqual(validate_bars(bars), bars)


class CsvLoaderTests(unittest.TestCase):
    def test_loads_valid_csv_with_zulu_timestamps(self) -> None:
        text = (
            "timestamp,open,high,low,close,volume\n"
            "2025-01-01T00:00:00Z,2000,2020,1990,2010,5\n"
            "2025-01-02T00:00:00Z,2010,2030,2000,2025,6\n"
        )
        loaded = load_ohlcv_csv(io.StringIO(text))
        self.assertEqual(len(loaded), 2)
        self.assertEqual(loaded[0].timestamp.utcoffset().total_seconds(), 0)

    def test_rejects_missing_required_header(self) -> None:
        with self.assertRaisesRegex(DataValidationError, "missing required columns"):
            load_ohlcv_csv(io.StringIO("timestamp,open,high,low,close\n"))

    def test_rejects_timestamp_without_timezone(self) -> None:
        text = "timestamp,open,high,low,close,volume\n2025-01-01,2000,2020,1990,2010,5\n"
        with self.assertRaisesRegex(DataValidationError, "timezone"):
            load_ohlcv_csv(io.StringIO(text))

    def test_rejects_invalid_numeric_value_with_line_number(self) -> None:
        text = "timestamp,open,high,low,close,volume\n2025-01-01T00:00:00Z,nope,2020,1990,2010,5\n"
        with self.assertRaisesRegex(DataValidationError, "row 2"):
            load_ohlcv_csv(io.StringIO(text))

    def test_empty_headerless_csv_is_rejected(self) -> None:
        with self.assertRaisesRegex(DataValidationError, "missing a header"):
            load_ohlcv_csv(io.StringIO(""))


if __name__ == "__main__":
    unittest.main()
