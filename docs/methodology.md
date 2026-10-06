# Methodology

This frozen file was exported from recorded execution-derived one-second candles for BTC Up/Down market 5060604. The metadata includes the market window, source token IDs, source history state, dataset provenance, row count and SHA-256 checksum.

1. Keep market and outcome-token identity separate.
2. Group recorded executions by their UTC execution-event second.
3. Preserve execution ordering for open and close; take the extrema for high and low.
4. Sum shares for volume and execution price × shares for quote volume.
5. Count observed executions using the source semantics recorded in the metadata.
6. Export recorded candles only. Preserve known gaps rather than manufacture candles for absent seconds.

Summing quote volume and dividing by summed shares gives the recorded-volume VWAP. A sampled price-history API does not contain execution sizes and cannot recover traded volume or execution count from prices alone.

## Coverage and revisions

The sample has unverified source completeness and three documented unrepaired connection gaps for the Down token. Up and Down have independent capture histories. The file’s time bounds do not imply continuous collection or complete exchange coverage. No participant identity or wallet attribution is inferred.

The export is immutable for reproducibility. Later collection or canonical corrections can produce a different live chart. If publishing another sample, use a new dated filename and its own metadata and checksum.

See [Omens candle methodology](https://omens.market/learn/how-we-build-polymarket-1s-ohlcv) and [the sample landing page](https://omens.market/polymarket-charts#one-second-sample).
