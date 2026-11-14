# Quantitative AI Research System — Data Foundation

This phase adds an explicit XAUUSD data-source contract and CSV adapter on top
of the initial OHLCV validator. It remains a research data foundation only: no
signals, recommendations, strategy logic, backtests, or performance claims.

## Layout

```text
quantitative_ai/
├── data/                         # Local data directories (no market data committed)
├── quantitative_ai/
│   ├── data/
│   │   ├── csv_loader.py         # Generic OHLCV CSV parser and validation
│   │   ├── csv_source.py         # Provenance- and metadata-aware CSV adapter
│   │   ├── source_metadata.py    # Instrument/source/provenance dataclasses
│   │   └── source_registry.py    # Named XAUUSD source specifications
│   ├── models.py                 # Immutable OHLCV bar
│   └── main.py                  # CSV validation CLI
└── tests/                        # Standard-library unittest suite
```

## CSV contract

CSV headers must include `timestamp,open,high,low,close,volume`. Timestamps are
ISO-8601 with an explicit UTC offset. Prices must be finite and positive;
volume finite and non-negative; highs/lows internally consistent; timestamps
strictly increasing and unique. Rows are never sorted, filled, or silently
repaired. Gaps are preserved because no vendor calendar or expected interval
has been specified.

## Source metadata and provenance

`DataSourceSpec` requires a supported instrument and timeframe, declares a
valid IANA timezone and source type, and can identify a local CSV path.
`DataProvenance` records a provider/source label and timezone-aware retrieval
timestamp, with optional URI, dataset revision, and license details. The CSV
adapter requires provenance by default. This is traceability metadata supplied
by the caller; it does not verify provider identity, licensing, or file
integrity.

A small default registry lists H1, H4, and D1 XAUUSD dataset *specifications*.
They do not point to actual data files and are not evidence that market data is
available. Register a real source only after providing its actual provenance.

## Run tests

From the repository root (Python 3.10+):

```bash
python -m unittest discover -s quantitative_ai/tests -v
```

The project uses only the Python standard library. No market data or external
provider credentials are included.

## Limitations and unresolved specifications

- Timeframe labels are metadata only; this phase does not verify candle spacing,
  trading sessions, or bar close conventions.
- A timezone offset in a timestamp cannot prove the true vendor/session
  convention. The adapter checks offset compatibility with the declared zone,
  not provenance authenticity.
- XAUUSD pip/tick size is deliberately not hard-coded; conventions vary by
  provider and account.
- Fibonacci anchoring and the meaning of OCL remain unspecified and are not
  implemented.
- Source-specific schema changes, revisions, and corporate-action-like data
  correction policies need provider documentation before implementation.
