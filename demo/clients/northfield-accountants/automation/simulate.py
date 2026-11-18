#!/usr/bin/env python3
"""Sandbox simulator for the Northfield invoice-capture workflow (DEMO).

Runs the same extraction rules as the n8n "Extract invoice fields" Code node
against the test files in ../sandbox/, writes Xero-style DRAFT bills to a JSON
file and sends anything that is not a valid invoice to the error branch
(a notification for operations-support). Python standard library only.
No network calls: Xero and the mailbox are simulated.

Usage: python3 simulate.py [--runs N] [--sandbox DIR] [--out DIR]
"""
import argparse
import datetime as dt
import hashlib
import json
import re
from decimal import Decimal, InvalidOperation
from pathlib import Path

HERE = Path(__file__).resolve().parent
MONTHS = {m: i for i, m in enumerate(
    ["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"], 1)}
AMT = r"([0-9][0-9,]*\.[0-9]{2})"


def money(s):
    try:
        return Decimal(s.replace(",", ""))
    except (InvalidOperation, AttributeError):
        return None


def find_dates(text):
    """Return (position, ISO date) for every full date in the text, in order."""
    out = []
    for m in re.finditer(r"\b(\d{4})-(\d{2})-(\d{2})\b", text):
        out.append((m.start(), m.group(1), m.group(2), m.group(3)))
    for m in re.finditer(r"\b(\d{1,2})/(\d{1,2})/(\d{4})\b", text):  # UK dd/mm/yyyy
        out.append((m.start(), m.group(3), m.group(2), m.group(1)))
    for m in re.finditer(r"\b(\d{1,2})\s+([A-Za-z]{3})[a-z]*\.?\s+(\d{4})\b", text):
        mon = MONTHS.get(m.group(2).lower())
        if mon:
            out.append((m.start(), m.group(3), str(mon), m.group(1)))
    res = []
    for pos, y, mo, d in sorted(out):
        try:
            res.append((pos, dt.date(int(y), int(mo), int(d)).isoformat()))
        except ValueError:
            continue
    return res


def invoice_date(text):
    dates = find_dates(text)
    for pos, iso in dates:  # skip dates labelled as due / pay-by dates
        before = text[max(0, pos - 15):pos].lower()
        if not re.search(r"due|pay by|payable", before):
            return iso
    return None


def supplier(text):
    m = re.search(r"^\s*From:\s*([^,\n]+)", text, re.M | re.I)
    if m:
        return m.group(1).strip()
    m = re.search(r"^\s*(.+?)\s+[—–-]+\s+invoice\b", text, re.M | re.I)
    if m:
        return m.group(1).strip()
    for line in text.splitlines():  # first line that looks like a business name
        line = line.strip()
        if not line or re.search(r"invoice|date|total|vat|\d", line, re.I):
            continue
        return line
    return None


def invoice_number(text):
    for pat in (r"\bNo\.\s*([A-Z0-9][A-Z0-9/\-]*)",
                r"#\s*([A-Z0-9][A-Z0-9/\-]*)",
                r"\binvoice\s+(?:number|no)?\s*:?\s*([A-Z]{1,6}[/\-][A-Z0-9/\-]+)"):
        m = re.search(pat, text, re.I)
        if m and re.search(r"\d", m.group(1)):
            return m.group(1)
    return None


def extract(text):
    """Extraction logic shared with the n8n Code node. Returns (fields, errors)."""
    f = {"supplier": supplier(text), "invoice_no": invoice_number(text),
         "date": invoice_date(text), "currency": "GBP"}
    total = re.search(r"\btotal(?:\s+due)?\b[\s.:]*(?:£|GBP)?\s*" + AMT, text, re.I)
    vat = re.search(r"\bVAT(?:\s*\d{1,2}(?:\.\d+)?%)?[\s.:]*£?\s*" + AMT, text, re.I)
    net = re.search(r"\b(?:net|subtotal)\b[\s.:]*£?\s*" + AMT, text, re.I)
    total = money(total.group(1)) if total else None
    vat = money(vat.group(1)) if vat else None
    net = money(net.group(1)) if net else None
    no_vat = bool(re.search(r"\bno VAT\b|not VAT registered", text, re.I))
    if total is None:  # single-amount invoice, e.g. "£86.00"
        amounts = re.findall(r"£\s*" + AMT, text)
        if len(amounts) == 1:
            total = money(amounts[0])
    if vat is None and no_vat:
        vat = Decimal("0.00")
    if net is None and total is not None and vat is not None:
        net = total - vat
    f.update(net=net, vat=vat, total=total)

    errors = []
    if not re.search(r"\binvoice\b", text, re.I) or re.search(r"\bno invoice\b", text, re.I):
        errors.append("not an invoice (no invoice wording, or says no invoice)")
    for k in ("supplier", "invoice_no", "date", "net", "vat", "total"):
        if f[k] is None:
            errors.append(f"missing {k}")
    if None not in (net, vat, total) and abs(net + vat - total) > Decimal("0.01"):
        errors.append(f"net + VAT ({net + vat}) does not equal total ({total})")
    for k in ("net", "vat", "total"):
        if f[k] is not None:
            f[k] = f"{f[k]:.2f}"
    return f, errors


def to_draft_bill(f, source):
    """Shape of the Xero 'create invoice' call (Type ACCPAY, Status DRAFT)."""
    return {
        "Type": "ACCPAY", "Status": "DRAFT",
        "Contact": {"Name": f["supplier"]},
        "InvoiceNumber": f["invoice_no"], "Date": f["date"],
        "CurrencyCode": f["currency"], "LineAmountTypes": "Exclusive",
        "LineItems": [{"Description": f"Invoice {f['invoice_no']} from {f['supplier']}",
                       "Quantity": 1, "UnitAmount": f["net"],
                       "TaxType": "INPUT2" if Decimal(f["vat"]) > 0 else "NONE",
                       "TaxAmount": f["vat"]}],
        "Total": f["total"], "_source": source,
    }


def run_once(sandbox, files):
    bills, errors = [], []
    for p in files:
        fields, errs = extract(p.read_text(encoding="utf-8"))
        if errs:
            # Error branch: the notification carries file name and reason only,
            # never the message body (no personal data leaves the client's tools).
            errors.append({"to": "operations-support", "workflow": "northfield-invoice-capture",
                           "item": p.name, "reasons": errs,
                           "action": "Check item; re-run per run-book section 4"})
        else:
            bills.append(to_draft_bill(fields, p.name))
    return bills, errors


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--runs", type=int, default=5)
    ap.add_argument("--sandbox", default=str(HERE.parent / "sandbox"))
    ap.add_argument("--out", default=str(HERE / "output"))
    a = ap.parse_args()
    sandbox, out = Path(a.sandbox), Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    files = sorted(sandbox.glob("*.txt"))
    digests, failures = [], 0
    for n in range(1, a.runs + 1):
        try:
            bills, errors = run_once(sandbox, files)
            (out / f"run-{n}-draft-bills.json").write_text(json.dumps(bills, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
            (out / f"run-{n}-ops-notifications.json").write_text(json.dumps(errors, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
            d = hashlib.sha256(json.dumps([bills, errors], sort_keys=True).encode()).hexdigest()[:12]
            digests.append(d)
            print(f"Run {n}: {len(files)} items -> {len(bills)} draft bills, {len(errors)} to error branch; digest {d}; OK")
        except Exception as e:  # a crash counts as a failed run
            failures += 1
            print(f"Run {n}: FAILED with {type(e).__name__}: {e}")
    if digests:
        bills, errors = run_once(sandbox, files)
        print("\nDraft bills (last run):")
        for b in bills:
            li = b["LineItems"][0]
            print(f"  {b['_source']}: {b['Contact']['Name']} | {b['InvoiceNumber']} | {b['Date']} | "
                  f"net {li['UnitAmount']} | VAT {li['TaxAmount']} | total {b['Total']} | {b['Status']}")
        print("Error branch (last run):")
        for e in errors:
            print(f"  {e['item']}: {'; '.join(e['reasons'])} -> {e['to']}")
    same = len(set(digests)) == 1
    print(f"\nSummary: {a.runs} runs, {failures} failed, identical output across runs: {same}")
    return 0 if failures == 0 and same else 1


if __name__ == "__main__":
    raise SystemExit(main())
