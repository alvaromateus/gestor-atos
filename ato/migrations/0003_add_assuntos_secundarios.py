# Generated by Django 3.2.8 on 2021-10-08 19:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ato', '0002_add_fields'),
    ]

    operations = [
        migrations.CreateModel(
            name='AssuntoSecundario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=200)),
            ],
            options={
                'verbose_name': 'Assunto Secundário',
                'verbose_name_plural': 'Assuntos Secundários',
                'ordering': ['nome'],
            },
        ),
        migrations.AlterModelOptions(
            name='setororiginario',
            options={'ordering': ['nome'], 'verbose_name': 'Setor Originário', 'verbose_name_plural': 'Setores Originários'},
        ),
        migrations.AlterField(
            model_name='ato',
            name='data_final',
            field=models.DateField(blank=True, default=None, null=True, verbose_name='Data do final da vigência do ato'),
        ),
        migrations.AlterField(
            model_name='ato',
            name='data_inicial',
            field=models.DateField(blank=True, default=None, null=True, verbose_name='Data do início da vigência do ato'),
        ),
        migrations.AlterField(
            model_name='setororiginario',
            name='nome',
            field=models.CharField(blank=True, default=None, max_length=40, null=True, verbose_name='nome do setor originário'),
        ),
        migrations.AddField(
            model_name='assunto',
            name='assuntos_secundarios',
            field=models.ManyToManyField(blank=True, null=True, to='ato.AssuntoSecundario'),
        ),
        migrations.AddField(
            model_name='ato',
            name='assuntos_secundarios',
            field=models.ManyToManyField(blank=True, null=True, to='ato.AssuntoSecundario'),
        ),
    ]
