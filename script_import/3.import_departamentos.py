#!/usr/bin/env python3
import argparse
import csv
import re
import sys
import time
import unicodedata
import xmlrpc.client
from pathlib import Path


def clean(value):
    if value is None:
        return False
    s = str(value).strip()
    return s if s else False


def to_int(value, default=None):
    s = clean(value)
    if not s:
        return default
    try:
        return int(float(s))
    except ValueError:
        return default


def slugify(value):
    s = clean(value)
    if not s:
        return "department"
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode("ascii")
    s = re.sub(r"[^a-zA-Z0-9]+", "_", s).strip("_").lower()
    return s or "department"


def find_employee(models, db, uid, password, name):
    raw = clean(name)
    if not raw:
        return False

    ids = models.execute_kw(
        db, uid, password,
        "hr.employee", "search",
        [[["name", "=", raw]]],
        {"limit": 1}
    )
    if ids:
        return ids[0]

    ids = models.execute_kw(
        db, uid, password,
        "hr.employee", "search",
        [[["name", "ilike", raw]]],
        {"limit": 1}
    )
    return ids[0] if ids else False


def find_department_by_name(models, db, uid, password, name):
    raw = clean(name)
    if not raw:
        return False

    ids = models.execute_kw(
        db, uid, password,
        "hr.department", "search",
        [[["name", "=", raw]]],
        {"limit": 1}
    )
    if ids:
        return ids[0]

    ids = models.execute_kw(
        db, uid, password,
        "hr.department", "search",
        [[["name", "ilike", raw]]],
        {"limit": 1}
    )
    return ids[0] if ids else False


def find_xmlid(models, db, uid, password, module, name):
    xmlid_ids = models.execute_kw(
        db, uid, password,
        "ir.model.data", "search",
        [[
            ["module", "=", module],
            ["name", "=", name],
        ]],
        {"limit": 1}
    )
    if not xmlid_ids:
        return False

    xmlid = models.execute_kw(
        db, uid, password,
        "ir.model.data", "read",
        [xmlid_ids],
        {"fields": ["res_id", "model"]}
    )[0]

    if xmlid["model"] != "hr.department":
        return False

    return xmlid["res_id"]


def main():
    parser = argparse.ArgumentParser(description="Import departments into Odoo from CSV.")
    parser.add_argument("--url", required=True, help="Odoo URL, e.g. http://odoo:8069 or http://localhost:8070")
    parser.add_argument("--db", required=True, help="Database name")
    parser.add_argument("--username", required=True, help="Odoo username")
    parser.add_argument("--password", required=True, help="Odoo password or API key")
    parser.add_argument("--csv", required=True, help="CSV path")
    parser.add_argument("--module", default="csv_departments", help="Module namespace for external ids")
    parser.add_argument("--retry-seconds", type=int, default=5, help="Retry delay if Odoo is not ready")
    parser.add_argument("--max-retries", type=int, default=60, help="Max connection retries")
    args = parser.parse_args()

    csv_path = Path(args.csv)
    if not csv_path.exists():
        print(f"CSV not found: {csv_path}", file=sys.stderr)
        sys.exit(1)

    common = xmlrpc.client.ServerProxy(f"{args.url}/xmlrpc/2/common")
    uid = None
    for _ in range(args.max_retries):
        try:
            uid = common.authenticate(args.db, args.username, args.password, {})
            if uid:
                break
        except Exception:
            pass
        time.sleep(args.retry_seconds)

    if not uid:
        print("Authentication failed or Odoo is not ready.", file=sys.stderr)
        sys.exit(1)

    models = xmlrpc.client.ServerProxy(f"{args.url}/xmlrpc/2/object")

    with csv_path.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames or []
        expected = {"Name", "Manager", "Parent Department", "Color"}
        missing = expected - set(fieldnames)
        if missing:
            print(f"Missing columns in CSV: {', '.join(sorted(missing))}", file=sys.stderr)
            sys.exit(1)
        rows = list(reader)

    created = 0
    updated = 0
    skipped = 0
    errors = 0

    # First pass: create/update departments by name/color only
    name_to_external = {}
    ordered_rows = []

    for row in rows:
        name = clean(row.get("Name"))
        if not name:
            skipped += 1
            continue

        ext_name = slugify(name)
        name_to_external[name] = ext_name
        ordered_rows.append(row)

        vals = {
            "name": name,
        }

        color = to_int(row.get("Color"), default=None)
        if color is not None:
            vals["color"] = color

        vals = {k: v for k, v in vals.items() if v not in (False, None, "")}

        try:
            dept_id = find_xmlid(models, args.db, uid, args.password, args.module, ext_name)

            if dept_id:
                models.execute_kw(
                    args.db, uid, args.password,
                    "hr.department", "write",
                    [[dept_id], vals]
                )
                updated += 1
            else:
                dept_id = models.execute_kw(
                    args.db, uid, args.password,
                    "hr.department", "create",
                    [vals]
                )
                models.execute_kw(
                    args.db, uid, args.password,
                    "ir.model.data", "create",
                    [{
                        "module": args.module,
                        "name": ext_name,
                        "model": "hr.department",
                        "res_id": dept_id,
                        "noupdate": False,
                    }]
                )
                created += 1
        except Exception:
            errors += 1

    # Second pass: set manager and parent department, but don't count as updates
    for row in ordered_rows:
        try:
            name = clean(row.get("Name"))
            if not name:
                continue

            dept_id = find_xmlid(models, args.db, uid, args.password, args.module, slugify(name))
            if not dept_id:
                continue

            vals = {}

            manager_name = clean(row.get("Manager"))
            if manager_name:
                manager_id = find_employee(models, args.db, uid, args.password, manager_name)
                if manager_id:
                    vals["manager_id"] = manager_id
                else:
                    vals["manager_id"] = False

            parent_name = clean(row.get("Parent Department"))
            if parent_name:
                parent_id = find_department_by_name(models, args.db, uid, args.password, parent_name)
                if not parent_id:
                    parent_id = find_xmlid(models, args.db, uid, args.password, args.module, slugify(parent_name))
                if parent_id:
                    vals["parent_id"] = parent_id
                else:
                    vals["parent_id"] = False

            if vals:
                models.execute_kw(
                    args.db, uid, args.password,
                    "hr.department", "write",
                    [[dept_id], vals]
                )
        except Exception:
            errors += 1

    print("\n================================")
    print("Departments import finished")
    print("================================")
    print(f"Created : {created}")
    print(f"Updated : {updated}")
    print(f"Skipped : {skipped}")
    print(f"Errors  : {errors}")
    print("================================")


if __name__ == "__main__":
    main()
