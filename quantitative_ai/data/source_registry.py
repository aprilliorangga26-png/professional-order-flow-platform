"""Source registry and metadata for structured market-data inputs."""

from .source_metadata import (
    DataSourceSpec,
    InstrumentProfile,
    XAUUSD_PROFILE,
    build_xauusd_source,
)

__all__ = [
    "DataSourceSpec",
    "InstrumentProfile",
    "XAUUSD_PROFILE",
    "build_xauusd_source",
]
