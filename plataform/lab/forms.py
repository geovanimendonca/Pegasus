from django import forms
from django.forms import widgets
from tempus_dominus.widgets import DatePicker
from .models import Post
from .models import Profile_user


class DateInput(forms.DateInput):
    input_type = 'date'

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('Exame',
                    'Nome_do_paciente',
                    'Cpf_paciente',
                    'Sexo',
                    'Data_de_nascimento')
        widgets = {'Data_de_nascimento': DateInput()}
        
        
class Profile_user_form(forms.ModelForm):
    class Meta:
        model = Profile_user
        fields = ('CRM',
                    'Estado_CRM'
            )
            