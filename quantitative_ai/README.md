# Quantitative AI Research System — Multi-Timeframe Data Layout

This phase introduces an explicit multi-timeframe dataset bundle for XAUUSD.
It is still a data and structure foundation only. No technical signal, trading
recommendation, or backtest logic is added.

## Purpose

The system is designed around daily-to-swing research with primary H4 context
and H1/D1 confirmation. This module makes that requirement explicit instead of
assuming the system will magically align timeframes or discover data files.

## Included components

- `timeframe.py` — canonical timeframe normalization and duration definition
- `dataset_bundle.py` — bundle validation for primary/confirmation timeframes
- tests in `tests/test_dataset_bundle.py` — validates the declared bundle layout

## Rules enforced

- timeframes are normalized to canonical values such as `H1`, `H4`, and `D1`
- a bundle must declare at least one source spec
- duplicate source names are rejected
- timeframe alias values such as `4h` and `1d` are accepted and normalized
- research bundles are explicit; no missing dataset is inferred silently

## Limitations

- this does not resample, merge, or backfill data
- it does not certify that the source files exist or are correct
- it does not infer the trading calendar or session shifts
- future modules will still need provider-specific semantics for historical
  corrections and symbol conventions
