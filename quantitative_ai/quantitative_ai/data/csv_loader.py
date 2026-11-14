"""CSV ingestion for the documented OHLCV contract."""

import csv
from datetime import datetime
from pathlib import Path
from typing import TextIO

from ..models import OHLCVBar
from .validation import DataValidationError, validate_bars

REQUIRED_COLUMNS = ("timestamp", "open", "high", "low", "close", "volume")


def _parse_timestamp(value: str, *, row_number: int) -> datetime:
    normalized = value.strip()
    if normalized.endswith("Z"):
        normalized = normalized[:-1] + "+00:00"
    try:
        timestamp = datetime.fromisoformat(normalized)
    except ValueError as exc:
        raise DataValidationError(
            f"invalid ISO-8601 timestamp at row {row_number}: {value!r}"
        ) from exc
    if timestamp.tzinfo is None or timestamp.utcoffset() is None:
        raise DataValidationError(
            f"timestamp at row {row_number} must include a timezone offset"
        )
    return timestamp


def load_ohlcv_csv(source: str | Path | TextIO) -> list[OHLCVBar]:
    """Load and validate CSV bars.

    Required headers: timestamp,open,high,low,close,volume. Timestamps must
    be ISO-8601 with a timezone, for example ``2025-01-02T00:00:00Z``.
    Extra columns are ignored. Rows are not sorted or repaired silently.
    """
    if hasattr(source, "read"):
        return _load_stream(source)  # type: ignore[arg-type]
    path = Path(source)
    try:
        with path.open("r", encoding="utf-8-sig", newline="") as handle:
            return _load_stream(handle)
    except OSError as exc:
        raise DataValidationError(f"could not read CSV file {path}: {exc}") from exc


def _load_stream(handle: TextIO) -> list[OHLCVBar]:
    reader = csv.DictReader(handle)
    if reader.fieldnames is None:
        raise DataValidationError("CSV is empty or missing a header row")

    missing = [column for column in REQUIRED_COLUMNS if column not in reader.fieldnames]
    if missing:
        raise DataValidationError(f"CSV missing required columns: {', '.join(missing)}")

    bars: list[OHLCVBar] = []
    for row_number, row in enumerate(reader, start=2):
        try:
            timestamp_value = row["timestamp"]
            if timestamp_value is None or not timestamp_value.strip():
                raise DataValidationError(f"missing timestamp at row {row_number}")
            values = {}
            for field in ("open", "high", "low", "close", "volume"):
                raw_value = row[field]
                if raw_value is None or not raw_value.strip():
                    raise DataValidationError(f"missing {field} at row {row_number}")
                try:
                    values[field] = float(raw_value)
                except ValueError as exc:
                    raise DataValidationError(
                        f"invalid {field} at row {row_number}: {raw_value!r}"
                    ) from exc
            bars.append(
                OHLCVBar(
                    timestamp=_parse_timestamp(timestamp_value, row_number=row_number),
                    **values,
                )
            )
        except KeyError as exc:
            raise DataValidationError(f"malformed CSV row {row_number}") from exc

    return validate_bars(bars)
