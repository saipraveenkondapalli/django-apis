# Generated by Django 5.0.1 on 2024-06-11 05:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0006_jobapplication'),
    ]

    operations = [
        migrations.AddField(
            model_name='jobapplication',
            name='last_visit',
            field=models.DateTimeField(auto_now=True),
        ),
    ]