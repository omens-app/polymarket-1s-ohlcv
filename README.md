# Polymarket 1s OHLCV Dataset & Python Examples

[![Validate OHLCV sample](https://github.com/omens-app/polymarket-1s-ohlcv/actions/workflows/validate-sample.yml/badge.svg)](https://github.com/omens-app/polymarket-1s-ohlcv/actions/workflows/validate-sample.yml)

A reproducible sample of trade-derived **1-second Polymarket OHLCV candles**, provided by [Omens](https://omens.market/polymarket-charts). Explore [live Polymarket 1s OHLCV charts](https://omens.market/polymarket-charts) and the methodology behind them.

The sample covers BTC Up/Down market **5060604**, September 29, 2026, **01:55–02:00 UTC**. It contains **366 candles**, with Up and Down kept as separate outcome tokens. No account, API key or Python package installation is needed to inspect it.

## Run the example

```sh
git clone https://github.com/omens-app/polymarket-1s-ohlcv.git
cd polymarket-1s-ohlcv
python3 examples/load_ohlcv.py
```

The loader verifies the CSV checksum, row count, market identity, timestamp alignment, OHLC bounds and share/traded-value consistency. It reports each outcome’s recorded volume, execution count and VWAP using Python Decimal arithmetic.

- [CSV sample](sample/btc-5m-1s-20260929.csv)
- [Provenance, source semantics and collection gaps](sample/btc-5m-1s-20260929.metadata.json)
- [Field schema](docs/schema.md)
- [Methodology and limitations](docs/methodology.md)
- [Python example](examples/load_ohlcv.py)

## What the data means

Prices use the **0–1 scale**. `volume` is shares; `quote_volume` is recorded execution price multiplied by shares, in source collateral units. `trade_count` counts observed executions in this sample, not unique traders or orders. The CSV `time` field is the UTC timestamp at the start of each second; `bucket_ms` is the same timestamp in Unix milliseconds.

**This sample is incomplete market history.** Its metadata records three unrepaired Down-token connection gaps. Missing seconds are omitted, and do not establish that no trading occurred. Source completeness is unverified. This is a frozen export; later corrections may change the current chart.

## Charts and research

[Omens charts](https://omens.market/polymarket-charts) support 1s, 1m, 5m, 15m, 30m, 1h, 4h and 1d intervals where recorded data is available. The file here contains only real recorded 1s candles. It does not invent higher-resolution data from price-history observations, nor synthesize missing trades.

Read [How we build 1-second OHLCV from Polymarket trades](https://omens.market/learn/how-we-build-polymarket-1s-ohlcv). This repository provides a static research sample and working code, not a hosted API or a complete historical feed.

Omens is independent of Polymarket. Source provenance and rights to third-party market data are separate from the example code.
