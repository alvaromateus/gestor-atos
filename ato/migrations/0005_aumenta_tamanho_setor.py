# Generated by Django 3.2 on 2021-10-20 22:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ato', '0004_alter_assunto'),
    ]

    operations = [
        migrations.AlterField(
            model_name='setororiginario',
            name='nome',
            field=models.CharField(blank=True, default=None, max_length=60, null=True, verbose_name='nome do setor originário'),
        ),
    ]