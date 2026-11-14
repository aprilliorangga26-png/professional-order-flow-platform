"""CSV adapter that binds OHLCV rows to explicit source metadata."""

from __future__ import annotations

from pathlib import Path
from typing import TextIO
from zoneinfo import ZoneInfo

from ..models import OHLCVBar
from .csv_loader import load_ohlcv_csv
from .source_metadata import DataSourceSpec
from .validation import DataValidationError


def load_source_csv(
    source: DataSourceSpec,
    csv_input: str | Path | TextIO | None = None,
    *,
    require_provenance: bool = True,
) -> list[OHLCVBar]:
    """Load CSV data while checking its declared source contract.

    ``csv_input`` may override the spec path for controlled testing or explicit
    invocation. A source must be of type CSV and, by default, include provenance
    metadata. Timestamp values must represent the timezone declared by the spec;
    they are not silently converted or reinterpreted. No bar interval or gaps
    are inferred because vendor/session conventions are not yet specified.
    """
    if source.source_type != "csv":
        raise DataValidationError(
            f"Source {source.name!r} has type {source.source_type!r}, not 'csv'"
        )
    if require_provenance and source.provenance is None:
        raise DataValidationError(
            f"Source {source.name!r} is missing provenance metadata"
        )
    selected_input = csv_input if csv_input is not None else source.path
    if selected_input is None:
        raise DataValidationError(
            f"Source {source.name!r} has no CSV path; pass csv_input or configure path"
        )

    bars = load_ohlcv_csv(selected_input)
    declared_zone = ZoneInfo(source.timezone)
    for index, bar in enumerate(bars, start=1):
        if bar.timestamp.utcoffset() != bar.timestamp.astimezone(declared_zone).utcoffset():
            raise DataValidationError(
                f"timestamp offset at data row {index} does not match source timezone "
                f"{source.timezone!r}"
            )
    return bars
