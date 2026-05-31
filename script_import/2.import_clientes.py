#!/usr/bin/env python3
import argparse
import csv
import sys
import time
import xmlrpc.client
from pathlib import Path


def clean(value):
    if value is None:
        return False
    s = str(value).strip()
    return s if s else False


def to_bool(value):
    s = str(value).strip().lower()
    return s in {"1", "true", "t", "yes", "y", "si", "sí"}


def resolve_country(models, db, uid, password, raw_value):
    raw = clean(raw_value)
    if not raw:
        return False

    ids = models.execute_kw(
        db, uid, password,
        "res.country", "search",
        [[["code", "=", raw.upper()]]],
        {"limit": 1}
    )
    if ids:
        return ids[0]

    ids = models.execute_kw(
        db, uid, password,
        "res.country", "search",
        [[["name", "ilike", raw]]],
        {"limit": 1}
    )
    return ids[0] if ids else False


def resolve_state(models, db, uid, password, raw_value, country_id=False):
    raw = clean(raw_value)
    if not raw:
        return False

    domain = [["name", "ilike", raw]]
    if country_id:
        domain.append(["country_id", "=", country_id])

    ids = models.execute_kw(
        db, uid, password,
        "res.country.state", "search",
        [domain],
        {"limit": 1}
    )
    return ids[0] if ids else False


def find_partner(models, db, uid, password, vat, email, name):
    if vat:
        ids = models.execute_kw(
            db, uid, password,
            "res.partner", "search",
            [[["vat", "=", vat]]],
            {"limit": 1}
        )
        if ids:
            return ids[0]

    if email:
        ids = models.execute_kw(
            db, uid, password,
            "res.partner", "search",
            [[["email", "=", email]]],
            {"limit": 1}
        )
        if ids:
            return ids[0]

    if name:
        ids = models.execute_kw(
            db, uid, password,
            "res.partner", "search",
            [[["name", "=", name]]],
            {"limit": 1}
        )
        if ids:
            return ids[0]

    return False


def find_or_create_bank(models, db, uid, password, bank_name):
    name = clean(bank_name)
    if not name:
        return False

    ids = models.execute_kw(
        db, uid, password,
        "res.bank", "search",
        [[["name", "=", name]]],
        {"limit": 1}
    )
    if ids:
        return ids[0]

    ids = models.execute_kw(
        db, uid, password,
        "res.bank", "search",
        [[["name", "ilike", name]]],
        {"limit": 1}
    )
    if ids:
        return ids[0]

    return models.execute_kw(
        db, uid, password,
        "res.bank", "create",
        [{"name": name}]
    )


def upsert_partner_bank(models, db, uid, password, partner_id, bank_name, acc_number):
    acc_number = clean(acc_number)
    if not acc_number:
        return None

    bank_id = find_or_create_bank(models, db, uid, password, bank_name)

    existing = models.execute_kw(
        db, uid, password,
        "res.partner.bank", "search",
        [[
            ["partner_id", "=", partner_id],
            ["acc_number", "=", acc_number],
        ]],
        {"limit": 1}
    )

    vals = {
        "partner_id": partner_id,
        "acc_number": acc_number,
    }
    if bank_id:
        vals["bank_id"] = bank_id

    if existing:
        models.execute_kw(
            db, uid, password,
            "res.partner.bank", "write",
            [existing, vals]
        )
        return existing[0]

    return models.execute_kw(
        db, uid, password,
        "res.partner.bank", "create",
        [vals]
    )


def main():
    parser = argparse.ArgumentParser(description="Import clientes into Odoo from CSV.")
    parser.add_argument("--url", required=True, help="Odoo URL, e.g. http://odoo:8069 or http://localhost:8070")
    parser.add_argument("--db", required=True, help="Database name")
    parser.add_argument("--username", required=True, help="Odoo username")
    parser.add_argument("--password", required=True, help="Odoo password or API key")
    parser.add_argument("--csv", required=True, help="CSV path")
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

    created = 0
    updated = 0
    skipped = 0
    errors = 0

    with csv_path.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f, delimiter=";")
        required = {
            "name", "is_company", "country_id", "state_id", "zip", "city",
            "street", "phone", "mobile", "email", "vat",
            "bank_ids/bank", "bank_ids/acc_number"
        }
        missing = required - set(reader.fieldnames or [])
        if missing:
            print(f"Missing columns in CSV: {', '.join(sorted(missing))}", file=sys.stderr)
            sys.exit(1)

        for row in reader:
            try:
                name = clean(row.get("name"))
                vat = clean(row.get("vat"))
                email = clean(row.get("email"))

                if not any([name, vat, email]):
                    skipped += 1
                    continue

                country_id = resolve_country(
                    models, args.db, uid, args.password, row.get("country_id")
                )
                state_id = resolve_state(
                    models, args.db, uid, args.password, row.get("state_id"), country_id
                )

                vals = {
                    "name": name,
                    "is_company": to_bool(row.get("is_company")),
                    "company_name": clean(row.get("company_name")),
                    "country_id": country_id,
                    "state_id": state_id,
                    "zip": clean(row.get("zip")),
                    "city": clean(row.get("city")),
                    "street": clean(row.get("street")),
                    "street2": clean(row.get("street2")),
                    "phone": clean(row.get("phone")),
                    "mobile": clean(row.get("mobile")),
                    "email": email,
                    "vat": vat,
                }

                vals = {
                    k: v
                    for k, v in vals.items()
                    if v not in (False, None, "")
                }

                partner_id = find_partner(
                    models, args.db, uid, args.password, vat, email, name
                )

                if partner_id:
                    models.execute_kw(
                        args.db, uid, args.password,
                        "res.partner", "write",
                        [[partner_id], vals]
                    )
                    updated += 1
                else:
                    partner_id = models.execute_kw(
                        args.db, uid, args.password,
                        "res.partner", "create",
                        [vals]
                    )
                    created += 1

                bank_account = clean(row.get("bank_ids/acc_number"))
                bank_name = clean(row.get("bank_ids/bank"))
                if bank_account:
                    upsert_partner_bank(
                        models, args.db, uid, args.password,
                        partner_id, bank_name, bank_account
                    )

            except Exception:
                errors += 1

    print("\n================================")
    print("Clients import finished")
    print("================================")
    print(f"Created : {created}")
    print(f"Updated : {updated}")
    print(f"Skipped : {skipped}")
    print(f"Errors  : {errors}")
    print("================================")


if __name__ == "__main__":
    main()
