# Generated by Django 5.1.2 on 2024-10-30 19:31

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="User",
            fields=[
                ("user_id", models.AutoField(primary_key=True, serialize=False)),
                ("username", models.CharField(max_length=255)),
                ("email", models.EmailField(max_length=254)),
            ],
        ),
    ]
