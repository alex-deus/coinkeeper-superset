import csv
from datetime import datetime
from decimal import Decimal

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction as db_transaction

from apps.core.models import Account, Category, Tag, Transaction


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("-f", "--file", default="rows.csv", type=str)

    def handle(self, *args, **options):
        try:
            file = open(options["file"], newline="", encoding="utf-8")
        except OSError as e:
            raise CommandError(f"Cannot open file: {e}")

        reader = csv.DictReader(file)

        required_columns = {
            "Date",
            "Type",
            "From",
            "To",
            "Tags",
            "Amount",
            "Currency",
            "Amount converted",
            "Currency of conversion",
            "Recurrence",
            "Note",
        }

        if not required_columns.issubset(reader.fieldnames):
            missing = required_columns - set(reader.fieldnames or [])
            raise CommandError(f"Missing columns: {', '.join(missing)}")

        created_count = 0

        with db_transaction.atomic():
            for row_num, row in enumerate(reader, start=2):
                try:
                    tx_date = datetime.strptime(row["Date"], "%d.%m.%Y").date()

                    tx_type = row["Type"].strip()

                    if tx_type != Transaction.TransactionType.EXPENSE:
                        continue

                    if tx_type not in Transaction.TransactionType.values:
                        raise ValueError(f"Invalid transaction type: {tx_type}")

                    account_name = row["From"].strip()
                    category_name = row["To"].strip()

                    recurrence = row["Recurrence"].strip().lower() == "true"

                    note = (row.get("Note") or "").strip() or None

                    currency_from = row["Currency"].strip()
                    if currency_from == "EUR":
                        amount_converted = Decimal(row["Amount"])
                    else:
                        amount_converted = Decimal(row["Amount converted"])

                    currency_to = row["Currency of conversion"].strip()

                    amount = Decimal(row["Amount"])

                except Exception as e:
                    raise CommandError(f"Row {row_num}: parsing error: {e}")

                account, _ = Account.objects.get_or_create(name=account_name)
                category, _ = Category.objects.get_or_create(name=category_name)
                tx = Transaction.objects.create(
                    type=tx_type,
                    account=account,
                    category=category,
                    currency_from=currency_from,
                    currency_to=currency_to,
                    amount=amount,
                    amount_converted=amount_converted,
                    is_recurrence=recurrence,
                    note=note,
                    created=tx_date,
                )

                tags_raw = (row.get("Tags") or "").strip()
                if tags_raw:
                    tag_names = [t.strip() for t in tags_raw.split(",") if t.strip()]
                    for tag_name in tag_names:
                        tag, _ = Tag.objects.get_or_create(name=tag_name)
                        tx.tags.add(tag)

                created_count += 1

        self.stdout.write(self.style.SUCCESS(f"Imported {created_count} transactions"))
