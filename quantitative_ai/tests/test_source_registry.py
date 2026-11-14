"""Registry helpers for supported market-data sources."""

from __future__ import annotations

from .source_metadata import DataSourceSpec, build_xauusd_source

DEFAULT_XAUUSD_SOURCES = {
    "xauusd_h4_csv": build_xauusd_source("xauusd_h4_csv", timeframe="H4", source_type="csv"),
    "xauusd_h1_csv": build_xauusd_source("xauusd_h1_csv", timeframe="H1", source_type="csv"),
    "xauusd_d1_csv": build_xauusd_source("xauusd_d1_csv", timeframe="D1", source_type="csv"),
}


def get_source(name: str) -> DataSourceSpec:
    """Return a registered source specification by name."""
    try:
        return DEFAULT_XAUUSD_SOURCES[name]
    except KeyError as exc:
        raise KeyError(f"Unknown source {name!r}; registered sources: {sorted(DEFAULT_XAUUSD_SOURCES)}") from exc


def list_sources() -> list[str]:
    """Return the names of the registered XAUUSD sources."""
    return sorted(DEFAULT_XAUUSD_SOURCES)
