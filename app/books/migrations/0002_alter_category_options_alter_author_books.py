# Generated by Django 4.1.5 on 2023-02-01 13:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("books", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="category",
            options={"verbose_name_plural": "Categories"},
        ),
        migrations.AlterField(
            model_name="author",
            name="books",
            field=models.ManyToManyField(
                blank=True, null=True, related_name="books", to="books.book"
            ),
        ),
    ]
