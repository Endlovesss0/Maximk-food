# Generated by Django 4.0.5 on 2022-06-28 09:24

import ckeditor_uploader.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_recipe_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='content',
            field=ckeditor_uploader.fields.RichTextUploadingField(blank=True, null=True, verbose_name='Рецепт'),
        ),
    ]
