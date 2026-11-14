# Quantitative AI Research System — Foundation

This directory contains phase one of a research-oriented XAUUSD quantitative
system. This phase implements only a provider-neutral OHLCV input contract,
validation, a CSV loader, a small validation CLI, and unit tests. It does not
produce signals, trading advice, backtest results, or performance claims.

## Project layout

```text
quantitative_ai/
├── config/                 # Configuration notes; no strategy parameters yet
├── data/
│   ├── economic/           # Reserved for sourced economic observations
│   ├── historical/         # Place local historical files here (not committed)
│   └── news/               # Reserved for sourced news observations
├── quantitative_ai/
│   ├── data/               # Input contract, validation, and CSV ingestion
│   ├── main.py             # Data-validation CLI
│   └── models.py           # Immutable OHLCV bar model
└── tests/                  # Standard-library unittest suite
```

## Data contract

CSV files must contain these headers: `timestamp,open,high,low,close,volume`.
Timestamps must be ISO-8601 and timezone-aware (for example,
`2025-01-02T00:00:00Z` or `2025-01-02T00:00:00+00:00`). OHLC values must be
finite positive numbers, volume must be finite and non-negative, and each bar
must have internally consistent high and low values. Rows must be ordered by
strictly increasing timestamps; duplicate timestamps are rejected. Extra CSV
columns are ignored.

No timeframe, session calendar, instrument precision, feed convention, or
expected bar interval is assumed. Gaps are preserved rather than silently
filled or labeled missing. This avoids inventing data; a future provider- or
instrument-specific adapter should define those semantics explicitly.

## Run

From the repository root, validate a CSV:

```bash
python -m quantitative_ai.main quantitative_ai/data/historical/example.csv
```

Run the unit tests from the repository root (Python 3.10+):

```bash
python -m unittest discover -s quantitative_ai/tests -v
```

The implementation uses only the Python standard library. No market data is
included. `requirements.txt` is intentionally empty until a dependency is
justified by a later phase.

## Known limitations and open decisions

- This is ingestion validation, not source authentication or data-quality
  certification. Validate vendor provenance separately before research use.
- Float parsing is convenient for ingestion; future calculation modules must
  define precision and rounding rules appropriate to their computations.
- Bar interval and timezone/session conventions are not inferred.
- Fibonacci anchoring/meaning and the definition of OCL remain unspecified;
  they are intentionally not implemented.
- The existing repository is a market/order-flow prototype. This Python
  research foundation is isolated under this directory and does not alter its
  existing frontend or documentation.

## Development boundary

This is the initial phase only. Technical patterns, fundamental analysis,
probability estimation, regimes, execution simulation, risk decisions, and
backtesting require separate specifications and approval before implementation.
