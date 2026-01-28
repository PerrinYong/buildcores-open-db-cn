#!/usr/bin/env python3
import csv
import json
import os
from pathlib import Path
from typing import Any, Dict, List, Tuple


REPO_ROOT = Path(__file__).resolve().parents[1]
OPEN_DB_DIR = REPO_ROOT / "open-db"
OUT_DIR = REPO_ROOT / "dist" / "product_facts"


def _safe_str(v: Any) -> str:
    if v is None:
        return ""
    if isinstance(v, (str, int, float, bool)):
        return str(v)
    return json.dumps(v, ensure_ascii=True, separators=(",", ":"), sort_keys=True)


def _extract_record(category: str, file_path: Path, data: Dict[str, Any]) -> Dict[str, Any]:
    metadata = data.get("metadata") or {}
    opendb_id = data.get("opendb_id") or metadata.get("opendb_id")
    name = metadata.get("name")
    manufacturer = metadata.get("manufacturer")
    series = metadata.get("series")
    variant = metadata.get("variant")
    part_numbers = metadata.get("part_numbers")

    rel_path = file_path.relative_to(REPO_ROOT).as_posix()

    return {
        "opendb_id": opendb_id,
        "category": category,
        "name": name,
        "manufacturer": manufacturer,
        "series": series,
        "variant": variant,
        "part_numbers": part_numbers,
        "path": rel_path,
    }


def build_index() -> Tuple[List[Dict[str, Any]], Dict[str, Any]]:
    if not OPEN_DB_DIR.exists():
        raise RuntimeError(f"Missing open-db directory: {OPEN_DB_DIR}")

    records: List[Dict[str, Any]] = []
    by_category: Dict[str, int] = {}
    by_manufacturer: Dict[str, int] = {}
    invalid: List[Dict[str, str]] = []

    processed = 0
    for category_dir in sorted([p for p in OPEN_DB_DIR.iterdir() if p.is_dir()]):
        category = category_dir.name
        print(f"Processing category: {category}")
        for json_file in category_dir.glob("*.json"):
            try:
                with json_file.open("r", encoding="utf-8") as f:
                    data = json.load(f)
            except Exception as e:
                invalid.append({"path": str(json_file), "error": str(e)})
                continue

            rec = _extract_record(category, json_file, data)
            if not rec.get("opendb_id"):
                invalid.append({"path": str(json_file), "error": "missing opendb_id"})
                continue

            records.append(rec)
            by_category[category] = by_category.get(category, 0) + 1
            m = rec.get("manufacturer") or ""
            if m:
                by_manufacturer[m] = by_manufacturer.get(m, 0) + 1
            
            processed += 1
            if processed % 5000 == 0:
                print(f"  Processed {processed} files...")

    stats = {
        "total": len(records),
        "by_category": dict(sorted(by_category.items(), key=lambda kv: (-kv[1], kv[0]))),
        "by_manufacturer_top": [
            {"manufacturer": k, "count": v}
            for k, v in sorted(by_manufacturer.items(), key=lambda kv: (-kv[1], kv[0]))[:200]
        ],
        "invalid": invalid[:2000],
        "invalid_count": len(invalid),
    }

    return records, stats


def write_outputs(records: List[Dict[str, Any]], stats: Dict[str, Any]) -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    index_json = OUT_DIR / "index.json"
    stats_json = OUT_DIR / "stats.json"
    index_csv = OUT_DIR / "index.csv"

    with index_json.open("w", encoding="utf-8") as f:
        json.dump(records, f, ensure_ascii=False, separators=(",", ":"))

    with stats_json.open("w", encoding="utf-8") as f:
        json.dump(stats, f, ensure_ascii=False, indent=2)

    fields = ["opendb_id", "category", "name", "manufacturer", "series", "variant", "part_numbers", "path"]
    with index_csv.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for r in records:
            row = dict(r)
            row["part_numbers"] = ";".join(row.get("part_numbers") or [])
            w.writerow({k: _safe_str(row.get(k)) for k in fields})


def main() -> int:
    records, stats = build_index()
    write_outputs(records, stats)
    print(f"Wrote: {OUT_DIR}")
    print(f"Total records: {stats['total']}")
    if stats.get("invalid_count"):
        print(f"Invalid files: {stats['invalid_count']} (see stats.json)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
