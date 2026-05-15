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
    # DEBUG FIELDS
    # -----------------------------

    product_fields = models.execute_kw(
        args.db,
        uid,
        args.password,
        "product.template",
        "fields_get",
        [],
        {}
    )

    print("Available fields:")
    print(product_fields.keys())

    # -----------------------------
    # CSV
    # -----------------------------

    with csv_path.open(
        "r",
        encoding="utf-8-sig",
        newline=""
    ) as f:

        reader = csv.DictReader(
            f,
            delimiter=";"
        )

        print("\nCSV columns:")
        print(reader.fieldnames)

        created = 0
        updated = 0

        for row in reader:

            external_id = clean_str(
                row.get("External ID")
            )

            if not external_id:
                print("Skipping row without External ID")
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

            print("\n--------------------------------")
            print("Processing:", external_id)
            print(vals)

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

                print("Updating existing product")

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

                print("Creating new product")

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

        print("\n================================")
        print(f"Created: {created}")
        print(f"Updated: {updated}")
        print("Done")


if __name__ == "__main__":
    main()
