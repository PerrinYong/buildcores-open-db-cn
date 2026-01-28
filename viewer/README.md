# OpenDB Product Facts Viewer

A simple, searchable web interface for browsing the BuildCores OpenDB product catalog.

## Quick Start

### 1. Build the Index

```bash
cd buildcores-open-db-cn
python tools/build_product_facts.py
```

This scans all `open-db/*/*.json` files and generates:
- `dist/product_facts/index.json` (13MB) - Full product index
- `dist/product_facts/index.csv` (8.6MB) - CSV export
- `dist/product_facts/stats.json` (14KB) - Category/manufacturer statistics

**Processing time:** ~4-5 minutes for 42,000+ products

### 2. Launch the Viewer

```bash
# Start HTTP server
python -m http.server 8000

# Open in browser
http://localhost:8000/viewer/
```

## Features

### Search & Filter
- **Search bar**: Filter by name, manufacturer, OpenDB ID, or category
- **Category dropdown**: Filter by component type (CPU, GPU, RAM, etc.)
- **Live results**: Updates as you type

### Data Displayed
- **Category**: Component type (CPU, GPU, RAM, Motherboard, etc.)
- **Name**: Full product name from metadata
- **Manufacturer**: Brand name (e.g., Intel, AMD, Corsair, ASUS)
- **OpenDB ID**: Unique identifier (UUID v4)
- **File**: Path to source JSON file (clickable link to GitHub)

### Current Stats (as of last build)
- **Total products**: 42,312
- **Categories**: 23 (RAM, GPU, PCCase, Keyboard, Motherboard, Storage, Monitor, etc.)
- **Top manufacturers**: 
  - Corsair (1,949 products)
  - MSI (1,924)
  - Gigabyte (1,581)
  - ASUS/Asus (2,393 combined)

## Technical Details

### Performance Optimizations
- **Lazy loading**: Displays max 2,000 rows at once
- **Client-side filtering**: No backend required
- **Minified JSON**: Compact format (~13MB for 42K records)

### Data Structure
Each record contains:
```json
{
  "opendb_id": "e0230286-0549-4da9-8115-9d1fbdcc2979",
  "category": "CPU",
  "name": "Intel Core i9-13900K",
  "manufacturer": "Intel",
  "series": "Core i9",
  "variant": "13900K",
  "part_numbers": ["BX8071513900K"],
  "path": "open-db/CPU/e0230286-0549-4da9-8115-9d1fbdcc2979.json"
}
```

## Updating Data

### Rebuild Index After Changes
```bash
# Pull latest from upstream
git fetch upstream
git merge upstream/main

# Rebuild
python tools/build_product_facts.py

# Refresh browser (Ctrl+R)
```

### Auto-sync Workflow
A GitHub Actions workflow (`.github/workflows/sync-upstream.yml`) automatically:
- Runs daily at 00:00 UTC
- Merges changes from upstream (`buildcores/buildcores-open-db`)
- Can be manually triggered via `gh workflow run sync-upstream.yml`

## Use Cases

1. **Component Research**: Browse all CPUs, GPUs, or other categories
2. **Manufacturer Analysis**: See all products from a specific brand
3. **Data Validation**: Quickly check if products are in the database
4. **Integration Testing**: Verify OpenDB IDs before linking market data

## Integration with Market Facts (Future)

This viewer shows the **Product Facts Layer** (M0 milestone). Future enhancements:

- **Price overlay**: Show typical market price ranges (from e-commerce APIs)
- **Availability indicator**: Green/yellow/red based on stock signals
- **Regional variants**: Highlight CN-specific products vs. global catalog
- **Clickable filters**: Jump to manufacturer/category combinations

## Files

- `index.html` - Main viewer UI
- `app.js` - Search/filter logic, table rendering
- `style.css` - Styling (responsive, clean layout)
- `README.md` - This file

## Limitations

- **Display cap**: Shows max 2,000 filtered results (refine search for more)
- **Schema variance**: Different categories have different fields (CPU vs GPU)
  - Viewer shows only common metadata fields
  - Full schemas available in `schemas/*.schema.json`
- **No write access**: Read-only viewer (edit via GitHub PR workflow)

## Browser Compatibility

Tested on:
- Chrome/Edge 90+
- Firefox 88+
- Safari 14+

Requires JavaScript enabled (uses Fetch API, ES6 features).

---

**Related Documentation:**
- Main project: `../README.md`
- System design: `../../docs/02-optimized-framework.md`
- Execution plan: `../../docs/03-execution-plan.md`
