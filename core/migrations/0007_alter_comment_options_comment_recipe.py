# Generated by Django 4.0.5 on 2022-07-10 09:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_comment'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comment',
            options={'verbose_name': 'Коментар рецепту', 'verbose_name_plural': 'Коментарі рецептів'},
        ),
        migrations.AddField(
            model_name='comment',
            name='recipe',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='core.recipe', verbose_name='Рецепт'),
            preserve_default=False,
        ),
    ]
