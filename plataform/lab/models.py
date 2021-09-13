from random import choices
from django.conf import settings
from django.db import models
from django.forms import widgets
from django.forms.models import ALL_FIELDS
from django.forms.widgets import Widget
from django.utils import timezone
from django.contrib.auth.models import User
from cpf_field.models import CPFField
from django import forms
from tempus_dominus.widgets import DatePicker
from django.core.validators import MaxValueValidator

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    
    Exames = (
        ('Covid-19', 'Covid-19'),
        ('Leishmaniose', 'Leishmaniose')
    )
    sexo_escolha = ( 
        ('Masculino', 'Masculino'),
        ('Feminino', 'Feminino'),
        ('Outros', 'Outros'),
    )

    Exame = models.CharField(max_length=20, choices = Exames)
    Nome_do_paciente = models.CharField(max_length=50)
    Cpf_paciente = CPFField('cpf')
    Sexo = models.CharField(max_length=20, choices = sexo_escolha)
    Data_de_nascimento = models.DateField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank = True, null=True)
    four_digit_code = models.IntegerField(blank = False, null = True)
    author = models.TextField()
    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.Exame
  
class Profile_user(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    autor = models.CharField(max_length = 50, blank = False)
    CRM = models.IntegerField(blank = False)
    ESTADOS = (
        ('A', 'Acre (AC)'),
        ('B', 'Alagoas (AL)'),
        ('C', 'Amapá (AP)'),
        ('D', 'Amazonas (AM)'),
        ('E', 'Bahia (BA'),
        ('F', 'Ceará (CE)'),
        ('G', 'Distrito Federal (DF)'),
        ('H', 'Espírito Santo (ES)'),
        ('I', 'Goiás (GO)'),
        ('J', 'Maranhão (MA)'),
        ('K', 'Mato Grosso (MT)'),
        ('L', 'Mato Grosso do Sul (MS)'),
        ('M', 'Minas Gerais (MG)'),
        ('N', 'Pará (PA)'),
        ('O', 'Paraíba (PB)'),
        ('P', 'Paraná (PR)'),
        ('Q', 'Pernambuco (PE)'),
        ('R', 'Piauí (PI)'),
        ('S', 'Rio de Janeiro (RJ)'),
        ('T', 'Rio Grande do Norte (RN)'),
        ('U', 'Rio Grande do Sul (RS)'),
        ('V', 'Rondônia (RO)'),
        ('X', 'Roraima (RR)'),
        ('Y', 'Santa Catarina (SC)'),
        ('Z', 'São Paulo (SP)'),
        ('W', 'Sergipe (SE)'),
        ('Ç', 'Tocantin (TO)')
    )
    Estado_CRM = models.CharField(max_length =1, choices = ESTADOS)
    def publish(self):
        self.save()

    def __str__(self):
        return self.CRM
        