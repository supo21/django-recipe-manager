# Generated by Django 5.0.4 on 2024-05-23 12:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipe', '0003_recipe_recipe_prep'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='recipe_prep',
            field=models.TextField(),
        ),
    ]
