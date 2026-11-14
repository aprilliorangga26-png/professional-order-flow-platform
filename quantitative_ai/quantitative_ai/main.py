"""Command-line entry point for validating historical OHLCV CSV files."""

import argparse
import sys

from .data.csv_loader import load_ohlcv_csv
from .data.validation import DataValidationError


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate OHLCV CSV market data")
    parser.add_argument("csv_path", help="CSV with timezone-aware OHLCV columns")
    args = parser.parse_args()

    try:
        bars = load_ohlcv_csv(args.csv_path)
    except DataValidationError as exc:
        print(f"Invalid market data: {exc}", file=sys.stderr)
        return 2

    print(f"Valid OHLCV data: {len(bars)} bars")
    if bars:
        print(
            f"Time range: {bars[0].timestamp.isoformat()} to "
            f"{bars[-1].timestamp.isoformat()}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
