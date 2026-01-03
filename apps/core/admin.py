from datetime import timedelta

from admin_auto_filters.filters import AutocompleteFilterFactory
from rangefilter.filters import DateRangeFilterBuilder, NumericRangeFilterBuilder

from django.contrib import admin
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from . import models


@admin.register(models.Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ["name", "id"]
    search_fields = ["name"]


@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "id"]
    search_fields = ["name"]


@admin.register(models.Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ["name", "id"]
    search_fields = ["name"]


@admin.register(models.Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ["id", "type", "account", "category", "amount_converted", "currency_to", "created", "get_tags"]
    list_filter = [
        (
            "created",
            DateRangeFilterBuilder(
                title=_("Created"), default_start=timezone.now() - timedelta(days=7), default_end=timezone.now()
            ),
        ),
        AutocompleteFilterFactory(_("Account"), "account", use_pk_exact=True),
        ("amount", NumericRangeFilterBuilder(title=_("Amount"))),
        "currency_from",
        AutocompleteFilterFactory(_("Category"), "category", use_pk_exact=True),
        ("amount_converted", NumericRangeFilterBuilder(title=_("Amount converted"))),
        "currency_to",
        AutocompleteFilterFactory(_("Tags"), "tags", use_pk_exact=True),
    ]
    filter_horizontal = ["tags"]
    search_fields = ["account__name", "category__name", "tags__name", "note"]
    fieldsets = (
        (_("Main"), {"fields": ("type", "created")}),
        (_("From"), {"fields": ("account", ("amount", "currency_from"))}),
        (_("To"), {"fields": ("category", ("amount_converted", "currency_to"))}),
        (_("Description"), {"fields": ("tags", "note")}),
        (_("Service"), {"classes": ["collapse"], "fields": ("is_recurrence",)}),
    )

    @admin.display(description=_("Tags"))
    def get_tags(self, obj: models.Transaction) -> str:
        return ", ".join(obj.tags.values_list("name", flat=True))
