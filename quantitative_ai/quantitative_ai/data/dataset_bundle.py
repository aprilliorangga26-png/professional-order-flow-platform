"""Explicit data-bundle definitions for multi-timeframe research layouts."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterable

from .source_metadata import DataSourceSpec
from .timeframe import normalize_timeframe


@dataclass(frozen=True, slots=True)
class DatasetBundle:
    """A bundle of explicitly configured source specs for one research workflow.

    The design intentionally avoids inferring missing datasets. For XAUUSD daily to
    swing research, a valid bundle must declare which timeframes it uses.
    """

    name: str
    primary_timeframe: str
    confirmation_timeframes: tuple[str, ...] = ()
    source_specs: tuple[DataSourceSpec, ...] = ()

    def __post_init__(self) -> None:
        if not self.name.strip():
            raise ValueError("Bundle name must be non-empty")
        object.__setattr__(self, "primary_timeframe", normalize_timeframe(self.primary_timeframe))
        normalized_confirmations = tuple(normalize_timeframe(tf) for tf in self.confirmation_timeframes)
        object.__setattr__(self, "confirmation_timeframes", normalized_confirmations)

        names: set[str] = set()
        for source in self.source_specs:
            if source.name in names:
                raise ValueError(f"Duplicate source name in bundle: {source.name!r}")
            names.add(source.name)

    def contains_timeframe(self, timeframe: str) -> bool:
        target = normalize_timeframe(timeframe)
        return target == self.primary_timeframe or target in self.confirmation_timeframes

    def sources_for_timeframe(self, timeframe: str) -> tuple[DataSourceSpec, ...]:
        target = normalize_timeframe(timeframe)
        return tuple(source for source in self.source_specs if source.timeframe == target)


def build_default_research_bundle(
    *,
    name: str = "xauusd_research_bundle",
    primary_timeframe: str = "H4",
    confirmation_timeframes: Iterable[str] = ("H1", "D1"),
    source_specs: Iterable[DataSourceSpec] = (),
) -> DatasetBundle:
    """Create an explicit multi-timeframe bundle for daily-to-swing research.

    This function does not create data files or claim a valid setup. It only
    asserts that the bundle declares the research layout and all included sources.
    """
    normalized_sources = tuple(source_specs)
    if not normalized_sources:
        raise ValueError("A research bundle must declare at least one source spec")
    return DatasetBundle(
        name=name,
        primary_timeframe=primary_timeframe,
        confirmation_timeframes=tuple(confirmation_timeframes),
        source_specs=normalized_sources,
    )
