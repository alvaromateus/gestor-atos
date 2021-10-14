# Generated by Django 3.2.8 on 2021-10-14 21:29

import ato.models
import ckeditor.fields
import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ato', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='assunto',
            options={'ordering': ['nome'], 'verbose_name': 'Assunto Principal', 'verbose_name_plural': 'Assuntos Principais'},
        ),
        migrations.AlterModelOptions(
            name='setororiginario',
            options={'ordering': ['nome'], 'verbose_name': 'Setor Originário', 'verbose_name_plural': 'Setores Originários'},
        ),
        migrations.AddField(
            model_name='ato',
            name='arquivo02',
            field=models.FileField(blank=True, default=None, null=True, upload_to=ato.models.documento_file_name, verbose_name='PDF Pesquisável'),
        ),
        migrations.AddField(
            model_name='ato',
            name='arquivo03',
            field=models.FileField(blank=True, default=None, null=True, upload_to=ato.models.documento_file_name, verbose_name='Arquivo editável (Word ou similar)'),
        ),
        migrations.AddField(
            model_name='ato',
            name='atos_vinculados',
            field=models.ManyToManyField(blank=True, default=None, null=True, related_name='_ato_ato_atos_vinculados_+', to='ato.Ato', verbose_name='Outros atos relacionados'),
        ),
        migrations.AddField(
            model_name='ato',
            name='data_documento',
            field=models.DateField(default=datetime.date(2021, 10, 14), verbose_name='Data do documento'),
        ),
        migrations.AddField(
            model_name='ato',
            name='data_final',
            field=models.DateField(blank=True, default=None, null=True, verbose_name='Data do final da vigência do ato'),
        ),
        migrations.AddField(
            model_name='ato',
            name='data_inicial',
            field=models.DateField(blank=True, default=None, null=True, verbose_name='Data do início da vigência do ato'),
        ),
        migrations.AddField(
            model_name='ato',
            name='data_suspensao',
            field=models.DateField(blank=True, default=None, null=True, verbose_name='Data da suspensão do ato'),
        ),
        migrations.AddField(
            model_name='ato',
            name='documentos_alterados',
            field=models.ManyToManyField(blank=True, default=None, null=True, related_name='_ato_ato_documentos_alterados_+', to='ato.Ato', verbose_name='Documento(s) alterado(s)'),
        ),
        migrations.AddField(
            model_name='ato',
            name='documentos_revogados',
            field=models.ManyToManyField(blank=True, default=None, null=True, related_name='_ato_ato_documentos_revogados_+', to='ato.Ato', verbose_name='Documento(s) revogado(s)'),
        ),
        migrations.AddField(
            model_name='ato',
            name='eh_alterador',
            field=models.BooleanField(default=False, verbose_name='Este documento altera outro?'),
        ),
        migrations.AddField(
            model_name='ato',
            name='eh_revogador',
            field=models.BooleanField(default=False, verbose_name='Este documento revoga outro?'),
        ),
        migrations.AddField(
            model_name='ato',
            name='tipo_revogacao',
            field=models.PositiveSmallIntegerField(blank=True, choices=[(0, 'Revogado totalmente'), (1, 'Revogado parcialmente')], null=True),
        ),
        migrations.AddField(
            model_name='setororiginario',
            name='sigla',
            field=models.CharField(blank=True, default=None, max_length=5, null=True, verbose_name='sigla'),
        ),
        migrations.AlterField(
            model_name='assunto',
            name='nome',
            field=models.CharField(max_length=200, verbose_name='assunto principal'),
        ),
        migrations.AlterField(
            model_name='ato',
            name='ano',
            field=models.IntegerField(blank=True, null=True, verbose_name='Ano'),
        ),
        migrations.AlterField(
            model_name='ato',
            name='arquivo',
            field=models.FileField(default=None, null=True, upload_to=ato.models.documento_file_name, verbose_name='Extrato Dioe'),
        ),
        migrations.AlterField(
            model_name='ato',
            name='status',
            field=models.PositiveSmallIntegerField(choices=[(0, 'Vigente'), (1, 'Revogado'), (2, 'Revogado parcialmente'), (3, 'Alterado'), (4, 'Sem efeito'), (5, 'Exaurido'), (6, 'Suspenso')], default=0),
        ),
        migrations.AlterField(
            model_name='ato',
            name='texto',
            field=ckeditor.fields.RichTextField(default=None, verbose_name='Texto documento'),
        ),
        migrations.AlterField(
            model_name='setororiginario',
            name='nome',
            field=models.CharField(blank=True, default=None, max_length=40, null=True, verbose_name='nome do setor originário'),
        ),
        migrations.AlterUniqueTogether(
            name='ato',
            unique_together={('ano', 'numero', 'tipo', 'setor_originario', 'status')},
        ),
        migrations.CreateModel(
            name='AssuntoSecundario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=200, verbose_name='assunto secundário')),
                ('assuntos', models.ManyToManyField(blank=True, null=True, to='ato.Assunto')),
            ],
            options={
                'verbose_name': 'Assunto Secundário',
                'verbose_name_plural': 'Assuntos Secundários',
                'ordering': ['nome'],
            },
        ),
        migrations.AddField(
            model_name='ato',
            name='assuntos_secundarios',
            field=models.ManyToManyField(blank=True, null=True, to='ato.AssuntoSecundario'),
        ),
    ]
