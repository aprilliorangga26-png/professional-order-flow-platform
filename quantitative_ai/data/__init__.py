"""Data source metadata for research inputs."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal

SUPPORTED_INSTRUMENTS = {"XAUUSD"}
SUPPORTED_TIMEFRAMES = {"M1", "M5", "M15", "M30", "H1", "H4", "D1", "W1", "MN"}
TIMEFRAME_ALIASES = {
    "1m": "M1",
    "5m": "M5",
    "15m": "M15",
    "30m": "M30",
    "1h": "H1",
    "4h": "H4",
    "1d": "D1",
    "1w": "W1",
    "1mo": "MN",
}


@dataclass(frozen=True, slots=True)
class InstrumentProfile:
    symbol: str
    asset_class: str = "commodity"
    quote_currency: str = "USD"
    pip_size: float = 0.01
    timezone: str = "UTC"

    def __post_init__(self) -> None:
        symbol = self.symbol.upper()
        if symbol not in SUPPORTED_INSTRUMENTS:
            raise ValueError(f"Unsupported instrument {self.symbol!r}; supported instruments: {sorted(SUPPORTED_INSTRUMENTS)}")
        object.__setattr__(self, "symbol", symbol)


@dataclass(frozen=True, slots=True)
class DataSourceSpec:
    name: str
    instrument: str
    timeframe: str
    timezone: str = "UTC"
    source_type: Literal["csv", "api", "database", "manual"] = "csv"
    path: str | None = None
    description: str = ""
    metadata: dict[str, str | float | int | bool] = field(default_factory=dict)

    def __post_init__(self) -> None:
        normalized = self.timeframe.upper()
        if normalized in TIMEFRAME_ALIASES.values():
            object.__setattr__(self, "timeframe", normalized)
        elif self.timeframe.lower() in TIMEFRAME_ALIASES:
            object.__setattr__(self, "timeframe", TIMEFRAME_ALIASES[self.timeframe.lower()])
        else:
            raise ValueError(
                f"Unsupported timeframe {self.timeframe!r}; supported timeframes: {sorted(SUPPORTED_TIMEFRAMES)}"
            )

        symbol = self.instrument.upper()
        if symbol not in SUPPORTED_INSTRUMENTS:
            raise ValueError(f"Unsupported instrument {self.instrument!r}; supported instruments: {sorted(SUPPORTED_INSTRUMENTS)}")
        object.__setattr__(self, "instrument", symbol)

        if not self.name or not self.name.strip():
            raise ValueError("Data source name must be non-empty")


XAUUSD_PROFILE = InstrumentProfile(symbol="XAUUSD", asset_class="commodity", quote_currency="USD", pip_size=0.01, timezone="UTC")


def build_xauusd_source(name: str, *, timeframe: str = "H4", source_type: str = "csv", path: str | None = None) -> DataSourceSpec:
    """Build a source specification for the research instrument.

    This keeps the system explicit: every dataset must declare instrument,
    timeframe, and source metadata. No assumptions are made from file names or
    provider defaults.
    """
    return DataSourceSpec(
        name=name,
        instrument=XAUUSD_PROFILE.symbol,
        timeframe=timeframe,
        timezone=XAUUSD_PROFILE.timezone,
        source_type=source_type,
        path=path,
        description="XAUUSD research data specification for quantitative analysis.",
    )
