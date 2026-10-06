# Sample schema

Each row identifies one market, outcome token and UTC one-second bucket. The metadata maps outcome labels to source token IDs.

| Field | Meaning |
|---|---|
| market_id | Source market identifier, stored as text |
| outcome | Up or Down; do not merge the two tokens |
| time | UTC bucket-opening timestamp, ISO 8601 |
| bucket_ms | UTC bucket-opening Unix timestamp in milliseconds |
| open | First recorded execution price |
| high / low | Highest / lowest recorded execution price |
| close | Last recorded execution price |
| volume | Sum of recorded execution shares |
| quote_volume | Sum of recorded execution price × shares |
| trade_count | Observed execution count for this sample |
| synthetic | False in every supplied row |

OHLC uses the 0–1 price scale. Keep decimals as decimal values, not binary floats, when aggregating volume. Outcome-token prices are different from Bitcoin’s dollar price. Consult the metadata for source collateral units, revisions, coverage intervals and trade-count semantics.

The CSV is sparse: absent seconds are not zero-volume evidence. A five-minute market round and a one-second candle are different time windows.
