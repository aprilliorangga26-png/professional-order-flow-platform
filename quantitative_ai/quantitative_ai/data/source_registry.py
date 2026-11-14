"""Named registry for explicitly configured XAUUSD datasets."""

from __future__ import annotations

from .source_metadata import DataSourceSpec

DEFAULT_XAUUSD_SOURCES: dict[str, DataSourceSpec] = {
    "xauusd_h1_csv": DataSourceSpec("xauusd_h1_csv", "XAUUSD", "H1"),
    "xauusd_h4_csv": DataSourceSpec("xauusd_h4_csv", "XAUUSD", "H4"),
    "xauusd_d1_csv": DataSourceSpec("xauusd_d1_csv", "XAUUSD", "D1"),
}


def get_source(name: str) -> DataSourceSpec:
    """Return a configured source spec or explain the available names."""
    try:
        return DEFAULT_XAUUSD_SOURCES[name]
    except KeyError as exc:
        raise KeyError(
            f"Unknown source {name!r}; registered sources: {sorted(DEFAULT_XAUUSD_SOURCES)}"
        ) from exc


def register_source(spec: DataSourceSpec, *, replace: bool = False) -> None:
    """Register a source spec; duplicates are rejected unless explicitly replaced."""
    if spec.name in DEFAULT_XAUUSD_SOURCES and not replace:
        raise ValueError(f"Source {spec.name!r} is already registered")
    DEFAULT_XAUUSD_SOURCES[spec.name] = spec


def list_sources() -> list[str]:
    return sorted(DEFAULT_XAUUSD_SOURCES)
