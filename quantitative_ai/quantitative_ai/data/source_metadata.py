"""Explicit metadata and provenance for market-data sources."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Literal
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

SUPPORTED_INSTRUMENTS = frozenset({"XAUUSD"})
SUPPORTED_TIMEFRAMES = frozenset({"M1", "M5", "M15", "M30", "H1", "H4", "D1", "W1", "MN"})
TIMEFRAME_ALIASES = {
    "1m": "M1", "5m": "M5", "15m": "M15", "30m": "M30",
    "1h": "H1", "4h": "H4", "1d": "D1", "1w": "W1", "1mo": "MN",
}
SourceType = Literal["csv", "api", "database", "manual"]


def _validate_timezone(value: str, field: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field} must be a non-empty IANA timezone name")
    try:
        ZoneInfo(value)
    except (ZoneInfoNotFoundError, ValueError) as exc:
        raise ValueError(f"Invalid IANA timezone for {field}: {value!r}") from exc


@dataclass(frozen=True, slots=True)
class InstrumentProfile:
    """Instrument facts that must be explicitly configured, not inferred."""

    symbol: str
    asset_class: str = "commodity"
    quote_currency: str = "USD"
    timezone: str = "UTC"

    def __post_init__(self) -> None:
        symbol = self.symbol.strip().upper()
        if symbol not in SUPPORTED_INSTRUMENTS:
            raise ValueError(f"Unsupported instrument {self.symbol!r}")
        _validate_timezone(self.timezone, "instrument timezone")
        object.__setattr__(self, "symbol", symbol)


@dataclass(frozen=True, slots=True)
class DataProvenance:
    """Traceability details for a dataset, supplied by its owner/provider."""

    provider: str
    retrieved_at: datetime
    source_uri: str | None = None
    dataset_revision: str | None = None
    license: str | None = None

    def __post_init__(self) -> None:
        if not self.provider.strip():
            raise ValueError("Provenance provider must be non-empty")
        if self.retrieved_at.tzinfo is None or self.retrieved_at.utcoffset() is None:
            raise ValueError("Provenance retrieved_at must be timezone-aware")


@dataclass(frozen=True, slots=True)
class DataSourceSpec:
    """Contract describing one dataset; it does not fetch or certify data."""

    name: str
    instrument: str
    timeframe: str
    timezone: str = "UTC"
    source_type: SourceType = "csv"
    path: str | None = None
    description: str = ""
    provenance: DataProvenance | None = None

    def __post_init__(self) -> None:
        if not self.name or not self.name.strip():
            raise ValueError("Data source name must be non-empty")
        symbol = self.instrument.strip().upper()
        if symbol not in SUPPORTED_INSTRUMENTS:
            raise ValueError(f"Unsupported instrument {self.instrument!r}")
        object.__setattr__(self, "instrument", symbol)

        timeframe = self.timeframe.strip()
        normalized = TIMEFRAME_ALIASES.get(timeframe.lower(), timeframe.upper())
        if normalized not in SUPPORTED_TIMEFRAMES:
            raise ValueError(
                f"Unsupported timeframe {self.timeframe!r}; supported: {sorted(SUPPORTED_TIMEFRAMES)}"
            )
        object.__setattr__(self, "timeframe", normalized)
        _validate_timezone(self.timezone, "source timezone")
        if self.source_type not in ("csv", "api", "database", "manual"):
            raise ValueError(f"Unsupported source type: {self.source_type!r}")
        if self.path is not None and not self.path.strip():
            raise ValueError("Source path must be omitted or non-empty")


XAUUSD_PROFILE = InstrumentProfile(symbol="XAUUSD")


def build_xauusd_source(
    name: str,
    *,
    timeframe: str = "H4",
    source_type: SourceType = "csv",
    path: str | None = None,
    timezone: str = "UTC",
    provenance: DataProvenance | None = None,
) -> DataSourceSpec:
    """Create an explicit XAUUSD dataset specification; no source is assumed."""
    return DataSourceSpec(
        name=name,
        instrument=XAUUSD_PROFILE.symbol,
        timeframe=timeframe,
        timezone=timezone,
        source_type=source_type,
        path=path,
        description="XAUUSD research dataset; source details are owner-supplied.",
        provenance=provenance,
    )
