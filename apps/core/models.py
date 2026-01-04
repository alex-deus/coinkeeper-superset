from django.db import models
from django.template.defaultfilters import truncatechars

__all__ = ["Account", "Category", "Tag", "Transaction"]


class Account(models.Model):
    name = models.CharField(max_length=128, unique=True)

    def __str__(self):
        return truncatechars(self.name, 32)

    class Meta:
        app_label = "core"
        ordering = ["name"]


class Category(models.Model):
    name = models.CharField(max_length=128, unique=True)

    def __str__(self):
        return truncatechars(self.name, 32)

    class Meta:
        app_label = "core"
        ordering = ["name"]
        verbose_name_plural = "Categories"


class Tag(models.Model):
    name = models.CharField(max_length=128, unique=True)

    def __str__(self):
        return truncatechars(self.name, 32)

    class Meta:
        app_label = "core"
        ordering = ["name"]


class Transaction(models.Model):
    class TransactionType(models.TextChoices):
        EXPENSE = "expense", "Expense"
        INCOME = "income", "Income"
        TRANSFER = "transfer", "Transfer"
        CORRECTION = "correction", "Correction"

    type = models.CharField(max_length=16, choices=TransactionType.choices, db_index=True)
    account = models.ForeignKey(Account, on_delete=models.PROTECT, related_name="account")
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="category")
    tags = models.ManyToManyField(Tag, related_name="tags", blank=True)

    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency_from = models.CharField(max_length=8)

    amount_converted = models.DecimalField(max_digits=10, decimal_places=2)
    currency_to = models.CharField(max_length=8)

    is_recurrence = models.BooleanField(default=False)

    note = models.TextField(blank=True, null=True)

    created = models.DateField(db_index=True)

    def __str__(self):
        return str(self.pk)

    class Meta:
        app_label = "core"
        ordering = ["-created"]
