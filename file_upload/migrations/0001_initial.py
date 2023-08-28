# Generated by Django 4.2.4 on 2023-08-20 13:15

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Visitor",
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
                ("UID", models.CharField(max_length=200)),
                ("사용일", models.DateField()),
                ("구분", models.CharField(blank=True, max_length=100, null=True)),
            ],
            options={
                "unique_together": {("UID", "사용일")},
            },
        ),
    ]