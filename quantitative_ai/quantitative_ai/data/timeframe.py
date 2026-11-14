"""Timeframe utilities for explicit market-data contracts."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import timedelta

SUPPORTED_TIMEFRAMES = frozenset({"M1", "M5", "M15", "M30", "H1", "H4", "D1", "W1", "MN"})
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
TIMEFRAME_TO_DURATION = {
    "M1": timedelta(minutes=1),
    "M5": timedelta(minutes=5),
    "M15": timedelta(minutes=15),
    "M30": timedelta(minutes=30),
    "H1": timedelta(hours=1),
    "H4": timedelta(hours=4),
    "D1": timedelta(days=1),
    "W1": timedelta(weeks=1),
    "MN": timedelta(days=30),
}


def normalize_timeframe(value: str) -> str:
    """Normalize a timeframe alias into the canonical research code."""
    text = value.strip()
    if not text:
        raise ValueError("Timeframe cannot be empty")
    normalized = TIMEFRAME_ALIASES.get(text.lower(), text.upper())
    if normalized not in SUPPORTED_TIMEFRAMES:
        raise ValueError(f"Unsupported timeframe {value!r}")
    return normalized


@dataclass(frozen=True, slots=True)
class TimeframeSpec:
    """A canonical timeframe definition with an explicit duration."""

    code: str
    duration: timedelta

    def __post_init__(self) -> None:
        code = normalize_timeframe(self.code)
        if code not in TIMEFRAME_TO_DURATION:
            raise ValueError(f"Unsupported timeframe {self.code!r}")
        object.__setattr__(self, "code", code)
        object.__setattr__(self, "duration", TIMEFRAME_TO_DURATION[code])


M1 = TimeframeSpec("M1", TIMEFRAME_TO_DURATION["M1"])
M5 = TimeframeSpec("M5", TIMEFRAME_TO_DURATION["M5"])
M15 = TimeframeSpec("M15", TIMEFRAME_TO_DURATION["M15"])
M30 = TimeframeSpec("M30", TIMEFRAME_TO_DURATION["M30"])
H1 = TimeframeSpec("H1", TIMEFRAME_TO_DURATION["H1"])
H4 = TimeframeSpec("H4", TIMEFRAME_TO_DURATION["H4"])
D1 = TimeframeSpec("D1", TIMEFRAME_TO_DURATION["D1"])
W1 = TimeframeSpec("W1", TIMEFRAME_TO_DURATION["W1"])
MN = TimeframeSpec("MN", TIMEFRAME_TO_DURATION["MN"])


def timeframe_duration(value: str) -> timedelta:
    """Return the canonical duration for a timeframe alias."""
    return TimeframeSpec(normalize_timeframe(value), TIMEFRAME_TO_DURATION[normalize_timeframe(value)]).duration


def is_higher_resolution(candidate: str, reference: str) -> bool:
    """Return True when candidate is a finer-grained timeframe than reference."""
    normalized_candidate = normalize_timeframe(candidate)
    normalized_reference = normalize_timeframe(reference)
    return TIMEFRAME_TO_DURATION[normalized_candidate] < TIMEFRAME_TO_DURATION[normalized_reference]
