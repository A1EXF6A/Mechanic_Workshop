#!/usr/bin/env python3

import argparse
import csv
import sys
import xmlrpc.client
from pathlib import Path


def to_float(value):
    if value is None:
        return False

    s = str(value).strip()

    if not s:
        return False

    return float(s.replace(",", "."))


def clean_str(value):
    if value is None:
        return False

    s = str(value).strip()

    return s if s else False


def main():
    parser = argparse.ArgumentParser(
        description="Import products into Odoo from CSV"
    )

    parser.add_argument(
        "--url",
        required=True,
        help="Odoo URL (example: http://localhost:8069)"
    )

    parser.add_argument(
        "--db",
        required=True,
        help="Database name"
    )

    parser.add_argument(
        "--username",
        required=True,
        help="Odoo username"
    )

    parser.add_argument(
        "--password",
        required=True,
        help="Odoo password"
    )

    parser.add_argument(
        "--csv",
        required=True,
        help="CSV path"
    )

    parser.add_argument(
        "--module",
        default="csv_products",
        help="Module namespace for external ids"
    )

    args = parser.parse_args()

    csv_path = Path(args.csv)

    if not csv_path.exists():
        print(f"CSV not found: {csv_path}")
        sys.exit(1)

    # -----------------------------
    # AUTH
    # -----------------------------

    common = xmlrpc.client.ServerProxy(
        f"{args.url}/xmlrpc/2/common"
    )

    uid = common.authenticate(
        args.db,
        args.username,
        args.password,
        {}
    )

    if not uid:
        print("Authentication failed")
        sys.exit(1)

    models = xmlrpc.client.ServerProxy(
        f"{args.url}/xmlrpc/2/object"
    )

    # -----------------------------
    # CSV IMPORT
    # -----------------------------

    created = 0
    updated = 0
    skipped = 0
    errors = 0

    with csv_path.open(
        "r",
        encoding="utf-8-sig",
        newline=""
    ) as f:

        reader = csv.DictReader(
            f,
            delimiter=";"
        )

        for row in reader:

            try:
                external_id = clean_str(
                    row.get("External ID")
                )

                if not external_id:
                    skipped += 1
                    continue

                vals = {
                    "name": clean_str(
                        row.get("Name")
                    ),

                    "default_code": clean_str(
                        row.get("Internal Reference")
                    ),

                    "barcode": clean_str(
                        row.get("Barcode")
                    ),

                    "list_price": to_float(
                        row.get("Sales Price")
                    ) or 0.0,

                    "standard_price": to_float(
                        row.get("Cost")
                    ) or 0.0,

                    "description_sale": clean_str(
                        row.get("Sales Description")
                    ),
                }

                weight = to_float(
                    row.get("Weight")
                )

                if weight is not False:
                    vals["weight"] = weight

                # remove empty values
                vals = {
                    k: v
                    for k, v in vals.items()
                    if v not in (False, None, "")
                }

                # -----------------------------
                # SEARCH EXISTING XML ID
                # -----------------------------

                xmlid_ids = models.execute_kw(
                    args.db,
                    uid,
                    args.password,
                    "ir.model.data",
                    "search",
                    [[
                        ["module", "=", args.module],
                        ["name", "=", external_id],
                    ]],
                    {"limit": 1}
                )

                # -----------------------------
                # UPDATE
                # -----------------------------

                if xmlid_ids:

                    xmlid = models.execute_kw(
                        args.db,
                        uid,
                        args.password,
                        "ir.model.data",
                        "read",
                        [xmlid_ids],
                        {"fields": ["res_id", "model"]}
                    )[0]

                    models.execute_kw(
                        args.db,
                        uid,
                        args.password,
                        "product.template",
                        "write",
                        [[xmlid["res_id"]], vals]
                    )

                    updated += 1

                # -----------------------------
                # CREATE
                # -----------------------------

                else:

                    record_id = models.execute_kw(
                        args.db,
                        uid,
                        args.password,
                        "product.template",
                        "create",
                        [vals]
                    )

                    models.execute_kw(
                        args.db,
                        uid,
                        args.password,
                        "ir.model.data",
                        "create",
                        [{
                            "module": args.module,
                            "name": external_id,
                            "model": "product.template",
                            "res_id": record_id,
                            "noupdate": False,
                        }]
                    )

                    created += 1

            except Exception:
                errors += 1

    # -----------------------------
    # SUMMARY
    # -----------------------------

    print("\n================================")
    print("Products import finished")
    print("================================")
    print(f"Created : {created}")
    print(f"Updated : {updated}")
    print(f"Skipped : {skipped}")
    print(f"Errors  : {errors}")
    print("================================")


if __name__ == "__main__":
    main()
