# Generated by Django 2.2.16 on 2022-04-17 16:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0004_auto_20220417_1930'),
    ]

    operations = [
        migrations.AlterField(
            model_name='titles',
            name='genre',
            field=models.ManyToManyField(blank=True, related_name='genre', to='reviews.Genres'),
        ),
    ]
