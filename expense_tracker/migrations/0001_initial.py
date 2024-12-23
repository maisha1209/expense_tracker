# Generated by Django 4.2 on 2024-11-08 20:55

from django.conf import settings
import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Account",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                (
                    "plaid_account_id",
                    models.CharField(max_length=200, null=True, unique=True),
                ),
                ("balances", models.JSONField(null=True)),
                ("mask", models.CharField(max_length=200, null=True)),
                ("name", models.CharField(max_length=200, null=True)),
                ("official_name", models.CharField(max_length=200, null=True)),
                ("subtype", models.CharField(max_length=200, null=True)),
                ("account_type", models.CharField(max_length=200, null=True)),
            ],
        ),
        migrations.CreateModel(
            name="Budget",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("date", models.DateField()),
                (
                    "user",
                    models.ForeignKey(
                        default=None,
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Category",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("description", models.CharField(max_length=200, unique=True)),
                ("custom", models.BooleanField(default=False)),
                (
                    "parent_category",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="expense_tracker.category",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        blank=True,
                        default=None,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Transaction",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("account_owner", models.CharField(max_length=200, null=True)),
                (
                    "amount",
                    models.DecimalField(decimal_places=2, max_digits=12, null=True),
                ),
                ("authorized_date", models.CharField(max_length=200, null=True)),
                (
                    "category",
                    django.contrib.postgres.fields.ArrayField(
                        base_field=models.CharField(max_length=200),
                        null=True,
                        size=None,
                    ),
                ),
                ("category_id", models.CharField(max_length=200, null=True)),
                ("date", models.DateField(default=django.utils.timezone.now)),
                ("iso_currency_code", models.CharField(max_length=200, null=True)),
                ("location", models.JSONField(null=True)),
                ("merchant_name", models.CharField(max_length=200, null=True)),
                ("name", models.CharField(max_length=200, null=True)),
                ("payment_meta", models.JSONField(null=True)),
                ("payment_channel", models.CharField(max_length=200, null=True)),
                ("pending", models.BooleanField(null=True)),
                ("pending_transaction_id", models.CharField(max_length=200, null=True)),
                ("transaction_code", models.CharField(max_length=200, null=True)),
                (
                    "transaction_id",
                    models.CharField(max_length=200, null=True, unique=True),
                ),
                ("transaction_type", models.CharField(max_length=200, null=True)),
                (
                    "unofficial_currency_code",
                    models.CharField(max_length=200, null=True),
                ),
                (
                    "account",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="expense_tracker.account",
                    ),
                ),
                (
                    "builtin_category",
                    models.ForeignKey(
                        blank=True,
                        default=260,
                        null=True,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        to="expense_tracker.category",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        default=None,
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="PlaidItem",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("access_token", models.CharField(max_length=200, unique=True)),
                ("item_id", models.CharField(max_length=200, unique=True)),
                (
                    "user",
                    models.ForeignKey(
                        default=None,
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="BudgetCategoryAmount",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("amount", models.DecimalField(decimal_places=2, max_digits=12)),
                (
                    "budget",
                    models.ForeignKey(
                        default=0,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="expense_tracker.budget",
                    ),
                ),
                (
                    "category",
                    models.ForeignKey(
                        default=0,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="expense_tracker.category",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="account",
            name="item",
            field=models.ForeignKey(
                blank=True,
                default=None,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="expense_tracker.plaiditem",
            ),
        ),
        migrations.AddField(
            model_name="account",
            name="user",
            field=models.ForeignKey(
                default=None,
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddConstraint(
            model_name="budgetcategoryamount",
            constraint=models.UniqueConstraint(
                fields=("budget", "category"), name="unique_budget_category"
            ),
        ),
    ]
