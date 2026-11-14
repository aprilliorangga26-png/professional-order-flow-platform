"""Small, dependency-free OHLCV data contract."""

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True, slots=True)
class OHLCVBar:
    """One OHLCV candle with a timezone-aware timestamp.

    Prices and volume are represented as floats at this ingestion boundary.
    Financial calculations should document their precision and rounding policy.
    """

    timestamp: datetime
    open: float
    high: float
    low: float
    close: float
    volume: float
