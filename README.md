# buildcores-open-db-cn

China-oriented PC components product facts repository.

This repository keeps two product-fact sources side by side:

1. `open-db-upstream/open-db/` - upstream BuildCores OpenDB (nested submodule)
2. `open-db-cn/` - China market incremental product facts (reviewed additions)

The union of these two directories is the effective CN product-facts view.

## Repository Layout

- `open-db-upstream/` - nested git submodule tracking `buildcores/buildcores-open-db`
- `open-db-cn/` - CN incremental facts (same category-style layout)
- `schemas/` - schema definitions
- `tools/build_product_facts.py` - builds combined index from upstream + CN layers
- `viewer/` - static viewer for generated index

## Key Rules

- No retail prices, promotions, or inventory in product facts.
- Every real product must map to one stable `product_id` in downstream identity mapping.
- CN incremental facts must keep source evidence and pass review before promotion.

## Upstream Update Strategy (Changed)

This repo no longer merges upstream directly into `main`.

Use nested submodule updates instead:

```bash
./scripts/sync_upstream.sh
```

This updates the pointer of `open-db-upstream` to latest upstream commit.

## Build Product Facts Index

```bash
python tools/build_product_facts.py
```

Output:

- `dist/product_facts/index.json`
- `dist/product_facts/index.csv`
- `dist/product_facts/stats.json`

## Viewer

```bash
python -m http.server 8000
# open http://localhost:8000/viewer/
```
