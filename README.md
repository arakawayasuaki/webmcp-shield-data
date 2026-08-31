# WebMCP Shield — public data

Daily snapshots of how WebMCP is actually deployed across the web, and what
servers in the official MCP registry advertise.

Live site and methodology: **https://webmcpshield.com**

This repository is a mirror. The files here are byte-identical to the ones
served at `https://webmcpshield.com/data/`, which remains the canonical source.

## What is measured

We crawl a list built from the Tranco popularity ranking plus a daily feed of
newly registered domains, and re-visit each domain on a tiered schedule. We read
what sites and servers declare.

**We never invoke a tool.**

## The two adoption numbers

Reporting WebMCP adoption as one number is misleading, so we report two.

| | what it is |
|---|---|
| **Vendor-distributed** | Sites carrying a tool set their platform ships them — Shopify storefronts, Cloudflare at the edge. Documented platform features, not vulnerabilities. This is the large number. |
| **Independent** | Sites that wrote their own implementation. This is the small number, and the one that reflects a decision made by the site itself. |

If you quote a single total without this split, you will misstate what we found.

## Using the data

```
data/index.json          every sealed snapshot, with sha256 and errata
data/YYYY-MM-DD.json     one sealed day — immutable, never rewritten
```

- **Cite a dated file, not the live endpoints.** `latest.json` and
  `/v1/public-status` on the site are rewritten continuously.
- Every dated file is listed in `index.json` with a **sha256**, so a number you
  cite stays verifiable.
- Corrections are appended to `errata` in the index. **The dated file itself is
  never edited.**
- Series baseline is **2026-08-16**. The 2026-08-15 file was written while the
  methodology was still changing; it is kept unmodified but excluded from
  comparisons.

### Cite as

```
WebMCP Shield, "WebMCP Exposure Census", YYYY-MM-DD.
https://webmcpshield.com/data/YYYY-MM-DD.json
```

### Verify a file

```
shasum -a 256 data/2026-08-30.json
```

Compare against the `sha256` for that date in `data/index.json`.

## Limitations we ask you to carry with the numbers

- Capability is inferred from tool names and descriptions. **We have not yet
  published an accuracy measurement for that inference.** These are measured
  indicators, not audits.
- A server advertising a state-changing tool is **not** evidence that the tool
  can be executed anonymously. Many ask for an API key in their own description.
- `domains_monitored` is the size of our crawl list. `domains_crawled` is what
  we have actually fetched. Statements about what we have looked at use the
  second one.
- The newly-registered-domain feed is a capped sample, not a census.
- We honour `robots.txt`. Sites that disallow us are excluded and counted
  separately.

## License

Data is published under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).
Attribute to WebMCP Shield with a link to the dated file you used.

## Not in this repository

The crawler itself. This repository contains published aggregate data only.

## How this mirror stays current

A scheduled GitHub Action fetches `index.json` from the canonical source once a
day, downloads any sealed file this repository does not have, and **verifies the
sha256 against the index before saving it**. If the mirror is offline for a few
days, the next run backfills every missing day.

It pulls; the production server pushes nothing here and holds no credentials for
this repository.
