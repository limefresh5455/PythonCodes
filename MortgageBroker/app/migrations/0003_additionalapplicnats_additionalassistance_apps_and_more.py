# Generated by Django 4.2.2 on 2023-06-21 05:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("app", "0002_remove_ticket_is_resolved"),
    ]

    operations = [
        migrations.CreateModel(
            name="AdditionalApplicnats",
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
                (
                    "applicant_form",
                    models.CharField(
                        choices=[("Yes", "Yes"), ("No", "No")], max_length=50
                    ),
                ),
                ("checkbox", models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name="AdditionalAssistance",
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
                ("assistance", models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name="Apps",
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
                ("apps", models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name="Country",
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
                ("country_name", models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name="Loans",
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
                (
                    "school_fees",
                    models.CharField(
                        choices=[("Yes", "Yes"), ("No", "No")], max_length=50
                    ),
                ),
                (
                    "maintenance",
                    models.CharField(
                        choices=[("Yes", "Yes"), ("No", "No")], max_length=50
                    ),
                ),
                (
                    "credit_card",
                    models.CharField(
                        choices=[("Yes", "Yes"), ("No", "No")], max_length=50
                    ),
                ),
                (
                    "other_loans",
                    models.CharField(
                        choices=[("Yes", "Yes"), ("No", "No")], max_length=50
                    ),
                ),
                ("checkbox", models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name="Property",
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
                ("property", models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name="PropertyType",
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
                ("type", models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name="SituationExisting",
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
                ("existing", models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name="SituationSearch",
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
                ("search", models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name="SourceOfFunds",
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
                ("source_of_funds", models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name="Status",
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
                ("status", models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name="MortgageRequirements",
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
                ("purchase_price", models.IntegerField()),
                ("currency", models.CharField(max_length=50)),
                ("loan_required", models.IntegerField()),
                ("years", models.IntegerField()),
                (
                    "savings_resources",
                    models.CharField(
                        choices=[("Yes", "Yes"), ("No", "No")], max_length=50
                    ),
                ),
                (
                    "rent_new_property",
                    models.CharField(
                        blank=True,
                        choices=[("Yes", "Yes"), ("No", "No")],
                        max_length=50,
                        null=True,
                    ),
                ),
                (
                    "improvements_in_property",
                    models.CharField(
                        blank=True,
                        choices=[("Yes", "Yes"), ("No", "No")],
                        max_length=50,
                        null=True,
                    ),
                ),
                ("checkbox", models.BooleanField(default=False)),
                (
                    "source",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="app.sourceoffunds",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Employment",
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
                ("employer_name", models.CharField(max_length=50)),
                ("employer_email", models.CharField(max_length=50, unique=True)),
                ("occupation", models.CharField(max_length=50)),
                ("shareholding_percent", models.IntegerField()),
                (
                    "employed_current_company",
                    models.IntegerField(blank=True, null=True),
                ),
                ("gross_income", models.IntegerField(blank=True, null=True)),
                ("income_after_tax", models.IntegerField(blank=True, null=True)),
                (
                    "income_after_tax_and_pension_ANNUM",
                    models.IntegerField(blank=True, null=True),
                ),
                (
                    "income_after_tax_and_pension_MONTH",
                    models.IntegerField(blank=True, null=True),
                ),
                ("bonus", models.IntegerField(blank=True, null=True)),
                ("checkbox", models.BooleanField(default=False)),
                (
                    "status",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="app.status"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="CurrentCircumstances",
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
                (
                    "hear_my_services",
                    models.CharField(blank=True, max_length=100, null=True),
                ),
                ("location_town", models.CharField(max_length=50)),
                ("postal_address", models.TextField(blank=True, null=True)),
                ("web_link", models.CharField(blank=True, max_length=50, null=True)),
                ("checkbox", models.BooleanField(default=False)),
                (
                    "location_country",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="app.country"
                    ),
                ),
                (
                    "property",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="app.property"
                    ),
                ),
                (
                    "property_type",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="app.propertytype",
                    ),
                ),
                (
                    "situation_regarding_existing",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="app.situationexisting",
                    ),
                ),
                (
                    "situation_regarding_search",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="app.situationsearch",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Assets",
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
                ("existing_property", models.TextField(blank=True, null=True)),
                ("other_savings", models.TextField(blank=True, null=True)),
                (
                    "bad_debts",
                    models.CharField(
                        blank=True,
                        choices=[("Yes", "Yes"), ("No", "No")],
                        max_length=50,
                        null=True,
                    ),
                ),
                ("checkbox", models.BooleanField(default=False)),
                (
                    "assistance",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="app.additionalassistance",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Applicant",
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
                (
                    "title",
                    models.CharField(
                        choices=[
                            ("Mr", "Mr"),
                            ("Mrs", "Mrs"),
                            ("Miss", "Miss"),
                            ("Mx", "Mx"),
                            ("Dr", "Dr"),
                            ("Ms", "Ms"),
                            ("Ind.", "Ind."),
                            ("Msr", "Msr"),
                            ("Mre", "Mre"),
                            ("M", "M"),
                            ("Pr", "Pr"),
                        ],
                        max_length=50,
                    ),
                ),
                ("first_name", models.CharField(max_length=50)),
                ("last_name", models.CharField(max_length=50)),
                ("dob", models.DateField(max_length=20)),
                ("marital_status", models.CharField(max_length=50)),
                ("nationality", models.CharField(max_length=50)),
                (
                    "current_residence",
                    models.CharField(blank=True, max_length=50, null=True),
                ),
                ("three_years_address_history_including_dates", models.TextField()),
                ("portfolio_details", models.TextField(blank=True, null=True)),
                ("day_telephone", models.TextField(unique=True)),
                ("home_telephone", models.IntegerField(blank=True, null=True)),
                ("mobile_telephone", models.IntegerField(blank=True, null=True)),
                ("whatsapp_telephone", models.IntegerField(blank=True, null=True)),
                ("email_address", models.CharField(max_length=50, unique=True)),
                (
                    "skype_address",
                    models.CharField(blank=True, max_length=50, null=True),
                ),
                ("checkbox", models.BooleanField(default=False)),
                (
                    "apps",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="app.apps"
                    ),
                ),
            ],
        ),
    ]
