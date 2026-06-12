# infraatlas-mcp

MCP server **and CLI** for [Infra Atlas](https://infraatlas.dev) — query live
multi-cloud compute catalogues, cross-cloud SKU equivalence, regions and
egress cost math from Claude, Cursor, any MCP client, or straight from the
terminal.

LLMs answer infrastructure questions with stale training data. Infra Atlas has
structured, daily-refreshed JSON for AWS, Azure, GCP, OCI and OVHcloud — this
server puts it one tool call away. No API key: the data is public (CC BY 4.0)
and the server runs locally over stdio, fetching the same CORS-enabled
`data.json` endpoints the site itself renders from.

## Tools

| Tool | What it answers |
|---|---|
| `infraatlas_get_compute_instances` | "Cheapest arm64 with 16 GB on AWS available in eu-west-1?" — filter one cloud's catalogue by region, arch, vCPU, memory, price, category |
| `infraatlas_find_equivalent_sku` | "What is the Azure equivalent of m5.xlarge?" — same transparent scoring as the [Equivalent-SKU Finder](https://infraatlas.dev/equivalent-sku/), with list price and region count per match |
| `infraatlas_get_egress_cost` | "What does 50 TB/month of internet egress cost on the big three?" — walks the tier ladder from the [Egress Cost Map](https://infraatlas.dev/egress/) |
| `infraatlas_get_regions` | "Which GCP regions are in Europe?" — all GA regions with city, country and coordinates |
| `infraatlas_whats_changed` | "Any new instance families this month?" — the daily-refresh change feed |

All prices are hourly on-demand **list** prices (Linux; USD, except OVHcloud
which publishes EUR) — never spot, reserved, savings-plan or invoiced prices.
Every response carries its source endpoint and upstream refresh timestamp.

## Install

Straight from the repository with [uv](https://docs.astral.sh/uv/) (no PyPI
needed):

```sh
uvx --from "git+https://github.com/ineslino/infra-atlas#subdirectory=mcp" infraatlas-mcp
```

### Claude Code

```sh
claude mcp add infraatlas -- uvx --from "git+https://github.com/ineslino/infra-atlas#subdirectory=mcp" infraatlas-mcp
```

### Claude Desktop / other MCP clients

```json
{
  "mcpServers": {
    "infraatlas": {
      "command": "uvx",
      "args": [
        "--from",
        "git+https://github.com/ineslino/infra-atlas#subdirectory=mcp",
        "infraatlas-mcp"
      ]
    }
  }
}
```

### From a local checkout

```sh
cd mcp
uv run infraatlas-mcp        # or: pip install -e . && infraatlas-mcp
```

## Try it

> *"Using infraatlas, find the cheapest arm64 instance with at least 16 GB on
> AWS and GCP, and tell me what 5 TB of internet egress would add per month."*

## Development

```sh
cd mcp
python3 tests/test_logic.py   # offline tests: scoring, tier ladder, band parser
npx @modelcontextprotocol/inspector uv run infraatlas-mcp   # poke the tools
```

The scoring constants mirror `equivalent-sku/index.html` (vCPU 50 / memory 38 /
category 12, ×0.55 cross-architecture) and the egress walk mirrors
`tools/egress-cost/`. If those change, change this server with them — the
offline tests pin the known-good numbers.

## The CLI

The same package ships an `infraatlas` terminal client over the same logic —
the public data API without the browser, with a ~1h on-disk cache
(`~/.cache/infraatlas`, `--fresh` bypasses) so repeat queries answer
instantly. Every command takes `--json` for piping into `jq`.

```sh
uvx --from "git+https://github.com/ineslino/infra-atlas#subdirectory=mcp" infraatlas --help

infraatlas ec2 --region eu-west-1 --arch arm64 --min-memory 16
infraatlas equivalent m5.xlarge
infraatlas egress aws azure --gb 500
infraatlas regions gcp --area Europe
infraatlas changes --days 7 --instrument aws
```

`ec2`, `azure`, `gcp`, `oci` and `ovh` are shorthands for `compute <cloud>`;
`changes --instrument` reads the per-instrument feeds
(`/ec2/feed.json`, …). Same price note as the tools: hourly on-demand list
prices, never spot/reserved/invoiced.

## Data & license

Data: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/), curated and
refreshed by [infraatlas.dev](https://infraatlas.dev) from public vendor
sources ([methodology](https://infraatlas.dev/about/)). Endpoint list:
[infraatlas.dev/api](https://infraatlas.dev/api/). Code: MIT.
