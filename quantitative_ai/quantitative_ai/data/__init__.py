"""Core market-data models, source metadata, and CSV ingestion."""

from .csv_source import load_source_csv
from .source_metadata import DataProvenance, DataSourceSpec, InstrumentProfile, XAUUSD_PROFILE
from .source_registry import get_source, list_sources, register_source

__all__ = [
    "DataProvenance",
    "DataSourceSpec",
    "InstrumentProfile",
    "XAUUSD_PROFILE",
    "get_source",
    "list_sources",
    "load_source_csv",
    "register_source",
]
