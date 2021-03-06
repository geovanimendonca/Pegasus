# Generated by Django 2.2.24 on 2021-07-09 13:08

import cpf_field.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile_user',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('autor', models.CharField(max_length=50)),
                ('CRM', models.IntegerField()),
                ('Estado_CRM', models.CharField(choices=[('A', 'Acre (AC)'), ('B', 'Alagoas (AL)'), ('C', 'Amapá (AP)'), ('D', 'Amazonas (AM)'), ('E', 'Bahia (BA'), ('F', 'Ceará (CE)'), ('G', 'Distrito Federal (DF)'), ('H', 'Espírito Santo (ES)'), ('I', 'Goiás (GO)'), ('J', 'Maranhão (MA)'), ('K', 'Mato Grosso (MT)'), ('L', 'Mato Grosso do Sul (MS)'), ('M', 'Minas Gerais (MG)'), ('N', 'Pará (PA)'), ('O', 'Paraíba (PB)'), ('P', 'Paraná (PR)'), ('Q', 'Pernambuco (PE)'), ('R', 'Piauí (PI)'), ('S', 'Rio de Janeiro (RJ)'), ('T', 'Rio Grande do Norte (RN)'), ('U', 'Rio Grande do Sul (RS)'), ('V', 'Rondônia (RO)'), ('X', 'Roraima (RR)'), ('Y', 'Santa Catarina (SC)'), ('Z', 'São Paulo (SP)'), ('W', 'Sergipe (SE)'), ('Ç', 'Tocantin (TO)')], max_length=1)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Exame', models.CharField(choices=[('Covid-19', 'Covid-19'), ('Leishmaniose', 'Leishmaniose')], max_length=20)),
                ('Nome_do_paciente', models.CharField(max_length=50)),
                ('Cpf_paciente', cpf_field.models.CPFField(max_length=14, verbose_name='cpf')),
                ('Sexo', models.CharField(max_length=10)),
                ('Data_de_nascimento', models.DateField()),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('published_date', models.DateTimeField(blank=True, null=True)),
                ('four_digit_code', models.IntegerField(null=True)),
                ('author', models.TextField()),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
