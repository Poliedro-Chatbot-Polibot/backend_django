# Generated by Django 5.2.1 on 2025-05-18 03:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0018_rename_fluxo_chatfluxoopcao_etapa_fluxo"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="chatfluxo",
            name="titulo",
        ),
    ]
