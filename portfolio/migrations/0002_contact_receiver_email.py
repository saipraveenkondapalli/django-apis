# Generated by Django 5.0.1 on 2024-06-08 10:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='contact',
            name='receiver_email',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
    ]
