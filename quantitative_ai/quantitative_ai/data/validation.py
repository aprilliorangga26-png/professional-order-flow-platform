"""Validation for market-bar data, without inferring missing observations."""

import math
from collections.abc import Iterable
from datetime import datetime

from ..models import OHLCVBar


class DataValidationError(ValueError):
    """Raised when input market data violates the documented data contract."""


def validate_bar(bar: OHLCVBar, *, row_number: int | None = None) -> None:
    """Validate one OHLCV bar and raise a descriptive error if invalid."""
    location = f" at row {row_number}" if row_number is not None else ""

    if not isinstance(bar.timestamp, datetime):
        raise DataValidationError(f"timestamp{location} must be a datetime")
    if bar.timestamp.tzinfo is None or bar.timestamp.utcoffset() is None:
        raise DataValidationError(f"timestamp{location} must include a timezone")

    for field in ("open", "high", "low", "close", "volume"):
        value = getattr(bar, field)
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise DataValidationError(f"{field}{location} must be numeric")
        if not math.isfinite(value):
            raise DataValidationError(f"{field}{location} must be finite")

    if any(getattr(bar, field) <= 0 for field in ("open", "high", "low", "close")):
        raise DataValidationError(f"OHLC prices{location} must be greater than zero")
    if bar.volume < 0:
        raise DataValidationError(f"volume{location} must not be negative")
    if bar.high < max(bar.open, bar.close, bar.low):
        raise DataValidationError(f"high{location} must be at least open, close, and low")
    if bar.low > min(bar.open, bar.close, bar.high):
        raise DataValidationError(f"low{location} must be at most open, close, and high")


def validate_bars(bars: Iterable[OHLCVBar]) -> list[OHLCVBar]:
    """Validate bars and require strictly increasing, unique timestamps.

    No timeframe is assumed, so gaps are preserved and are not classified as
    missing data. Returns a materialized list in its original order.
    """
    validated: list[OHLCVBar] = []
    previous: datetime | None = None

    for row_number, bar in enumerate(bars, start=1):
        validate_bar(bar, row_number=row_number)
        if previous is not None:
            try:
                increasing = bar.timestamp > previous
            except (TypeError, OverflowError) as exc:
                raise DataValidationError(
                    f"timestamps are not comparable at row {row_number}"
                ) from exc
            if not increasing:
                if bar.timestamp == previous:
                    raise DataValidationError(
                        f"duplicate timestamp at row {row_number}: {bar.timestamp.isoformat()}"
                    )
                raise DataValidationError(
                    f"timestamps must be strictly increasing at row {row_number}"
                )
        validated.append(bar)
        previous = bar.timestamp

    return validated
