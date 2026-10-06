#!/usr/bin/env python3
"""Inspect the frozen Omens Polymarket 1s OHLCV sample with Python 3.

Clone this repository, then:
    python3 examples/load_ohlcv.py
Or provide both file paths:
    python3 examples/load_ohlcv.py candles.csv candles.metadata.json

Documentation: https://omens.market/polymarket-charts#one-second-sample
No network requests, external packages, or filling of missing seconds.
"""
import argparse
import csv
import hashlib
import io
import json
from datetime import datetime, timezone
from decimal import Decimal
from pathlib import Path


def summarize(csv_path, metadata_path):
    raw = Path(csv_path).read_bytes()
    metadata = json.loads(Path(metadata_path).read_text())
    if hashlib.sha256(raw).hexdigest() != metadata["sha256"]:
        raise ValueError("CSV checksum differs from the frozen sample metadata")
    rows = list(csv.DictReader(io.StringIO(raw.decode("utf-8"))))
    if len(rows) != metadata["rows"]:
        raise ValueError("CSV row count differs from metadata")
    start = datetime.fromisoformat(metadata["opens_at"].replace("Z", "+00:00"))
    end = datetime.fromisoformat(metadata["closes_at"].replace("Z", "+00:00"))
    sources = {source["outcome"]: source for source in metadata["sources"]}
    totals, seen = {}, set()
    for row in rows:
        outcome = row["outcome"]
        if row["market_id"] != metadata["market_id"] or outcome not in sources:
            raise ValueError("Unexpected market or outcome identity")
        bucket = int(row["bucket_ms"])
        time = datetime.fromisoformat(row["time"].replace("Z", "+00:00"))
        if bucket % 1000 or time != datetime.fromtimestamp(bucket // 1000, timezone.utc):
            raise ValueError("Time does not match the UTC one-second bucket")
        if not start <= time < end:
            raise ValueError("Candle is outside the half-open round window")
        key = (row["market_id"], outcome, bucket)
        if key in seen:
            raise ValueError("Duplicate candle for the same market, outcome and second")
        seen.add(key)
        prices = [Decimal(row[field]) for field in ("open", "high", "low", "close")]
        volume, quote = Decimal(row["volume"]), Decimal(row["quote_volume"])
        if not all(value.is_finite() for value in [*prices, volume, quote]):
            raise ValueError("Non-finite price or volume")
        opening, high, low, close = prices
        if not (0 <= low <= opening <= high <= 1 and low <= close <= high):
            raise ValueError("Invalid OHLC bounds")
        count = int(row["trade_count"])
        if volume <= 0 or quote < 0 or count <= 0 or row["synthetic"] != "False":
            raise ValueError("Expected positive-volume, non-synthetic recorded candles")
        if not low * volume <= quote <= high * volume:
            raise ValueError("Traded value is outside candle price × share bounds")
        total = totals.setdefault(outcome, {"candles": 0, "shares": Decimal(0),
                                           "traded_value": Decimal(0), "trade_count": 0})
        total["candles"] += 1
        total["shares"] += volume
        total["traded_value"] += quote
        total["trade_count"] += count
    for outcome, total in totals.items():
        source = sources[outcome]
        total["vwap"] = str(total["traded_value"] / total["shares"])
        total["shares"] = str(total["shares"])
        total["traded_value"] = str(total["traded_value"])
        total["volume_unit"] = source["volume_unit"]
        total["quote_unit"] = source["quote_unit"]
        total["trade_count_semantics"] = source["trade_count_semantics"]
        total["source_completeness"] = source["history"]["source_completeness"]
        total["documented_gaps"] = len(source["gaps"])
    return {"market_id": metadata["market_id"], "rows": len(rows),
            "checksum_verified": True, "limitations": metadata["definition"],
            "outcomes": totals}


def main():
    directory = Path(__file__).resolve().parents[1] / "sample"
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("csv", nargs="?", type=Path,
                        default=directory / "btc-5m-1s-20260929.csv")
    parser.add_argument("metadata", nargs="?", type=Path,
                        default=directory / "btc-5m-1s-20260929.metadata.json")
    args = parser.parse_args()
    try:
        print(json.dumps(summarize(args.csv, args.metadata), indent=2))
    except (ValueError, KeyError, OSError) as error:
        parser.exit(1, f"Sample check failed: {error}\n")


if __name__ == "__main__":
    main()
