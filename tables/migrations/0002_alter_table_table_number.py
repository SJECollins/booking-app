# Generated by Django 4.2.7 on 2023-11-23 15:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tables', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='table',
            name='table_number',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]
