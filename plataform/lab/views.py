from django.contrib.auth.models import User
from django.shortcuts import render
from django.utils import timezone
from .models import Post, Profile_user
from .forms import PostForm, Profile_user_form
from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect
import requests
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from google.cloud import storage
import os, itertools
import qrcode
from PIL import Image  
import random

from os import makedirs
from ip2geotools.databases.noncommercial import DbIpCity
from requests import get
import folium
from folium.plugins import HeatMap, MarkerCluster
from branca.element import Figure

from folium import plugins

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "./pythondbtest-a8bdf-firebase-adminsdk-daafs-7052e44485.json"

db = firestore.client() # Database
client = storage.Client() # Storage
bucket = client.get_bucket('pythondbtest-a8bdf.appspot.com')

def button(request):
    return render(request,'lab/base.html')

def output(request,pk):
    post=Post.objects.get(id=pk)
    try:
        users_ref = db.collection(u'Exame')
        docs = users_ref.stream()
        for doc in docs:
            CPF_ID_result = str(post.Cpf_paciente)#+("_")+str(post.pk)

            exp = doc.to_dict()
            data = exp.get(CPF_ID_result+("_result"))

        if data != None:
            Exame_result = data[0]
            Paciente = data[1]
            Executor = data[2]
         #   paciente_sus = data[3]
            paciente_sexo = data[4]
            paciente_nascimento = data[5]
            medico_nome = data[6]
            medico_email = data[7]
            medico_crm = data[8]
            medico_estadocrm = data[9]
            executor_id = data[10]
            unidade_saude = data[11]

        return render(request,'lab/result.html',{'data':data,'exame':Exame_result,'paciente':Paciente,'executor':Executor,
            'paciente_sexo':paciente_sexo,'paciente_nascimento':paciente_nascimento,
            'medico_nome':medico_nome,'medico_email':medico_email,'medico_crm':medico_crm,
            'medico_estadocrm':medico_estadocrm,'executor_id':executor_id,'unidade_saude':unidade_saude})
    except:
        return render(request, 'lab/result.html')

def post_new(request):
    try:
        if request.method == "POST":
            form = PostForm(request.POST)
            form_update = Profile_user.objects.get(autor=request.user)
            if form.is_valid():
                post = form.save(commit=False)
                post.author = request.user
                post.published_date = timezone.now()
                post.four_digit_code = random.randint(1000,9999)
                post.save()
                # Salvando dados na nuvem
                nome_medico = str(request.user.first_name)+" "+str(request.user.last_name)
                    
                dicionario_estados = {'A': 'Acre (AC)',
                                        'B': 'Alagoas (AL)',
                                        'C': 'Amapá (AP)',
                                        'D': 'Amazonas (AM)',
                                        'E': 'Bahia (BA',
                                        'F': 'Ceará (CE)',
                                        'G': 'Distrito Federal (DF)',
                                        'H': 'Espírito Santo (ES)',
                                        'I': 'Goiás (GO)',
                                        'J': 'Maranhão (MA)',
                                        'K': 'Mato Grosso (MT)',
                                        'L': 'Mato Grosso do Sul (MS)',
                                        'M': 'Minas Gerais (MG)',
                                        'N': 'Pará (PA)',
                                        'O': 'Paraíba (PB)',
                                        'P': 'Paraná (PR)',
                                        'Q': 'Pernambuco (PE)',
                                        'R': 'Piauí (PI)',
                                        'S': 'Rio de Janeiro (RJ)',
                                        'T': 'Rio Grande do Norte (RN)',
                                        'U': 'Rio Grande do Sul (RS)',
                                        'V': 'Rondônia (RO)',
                                        'X': 'Roraima (RR)',
                                        'Y': 'Santa Catarina (SC)',
                                        'Z': 'São Paulo (SP)',
                                        'W': 'Sergipe (SE)',
                                        'Ç': 'Tocantin (TO)'
                                        }

                Equipamento = 'Pegasus' 
                #CPF = str(post.Cpf_paciente)#+("_")+str(post.pk)
                doc_ref = db.collection(Equipamento).document(u'Exame')
                doc_ref.set({
                    str(post.four_digit_code):[str(post.Exame),
                    str(post.Nome_do_paciente),
                    str(post.Sexo),
                    str(post.Data_de_nascimento),
                    str(nome_medico),
                    str(form_update.CRM),
                    str(dicionario_estados[form_update.Estado_CRM]),
                    str(request.user.email),
                    str(post.Cpf_paciente)]

                },merge=True)
                # Gerando Qr code
                #qr = qrcode.QRCode(
                #    version=1,
                #    error_correction=qrcode.constants.ERROR_CORRECT_L,
                #    box_size=10,
                #    border=4,
                #)
                #qr.add_data(str(post.Cpf_paciente)+("_")+str(post.pk))
                #qr.make(fit=True)
                #img = qr.make_image(fill_color="black", back_color="white")
                #im1 = img.save("lab/static/qrcodes/"+str(post.Cpf_paciente)+("_")+str(post.pk)+".png") 
                return redirect('post_detail', pk=post.pk)
        else:
            form = PostForm()
        return render(request, 'lab/post_edit.html', {'form': form}) 
    except:
        return redirect( 'edit_profile') 
    
def post_edit(request, pk):
     post = get_object_or_404(Post, pk=pk)
     if request.method == "POST":
         form_update = Profile_user.objects.get(autor=request.user)
         form = PostForm(request.POST, instance=post)
         if form.is_valid():
             post = form.save(commit=False)
             post.published_date = timezone.now()
             post.save()
             nome_medico = str(request.user.first_name)+" "+str(request.user.last_name)
             dicionario_estados = {'A': 'Acre (AC)',
                    'B': 'Alagoas (AL)',
                    'C': 'Amapá (AP)',
                    'D': 'Amazonas (AM)',
                    'E': 'Bahia (BA',
                    'F': 'Ceará (CE)',
                    'G': 'Distrito Federal (DF)',
                    'H': 'Espírito Santo (ES)',
                    'I': 'Goiás (GO)',
                    'J': 'Maranhão (MA)',
                    'K': 'Mato Grosso (MT)',
                    'L': 'Mato Grosso do Sul (MS)',
                    'M': 'Minas Gerais (MG)',
                    'N': 'Pará (PA)',
                    'O': 'Paraíba (PB)',
                    'P': 'Paraná (PR)',
                    'Q': 'Pernambuco (PE)',
                    'R': 'Piauí (PI)',
                    'S': 'Rio de Janeiro (RJ)',
                    'T': 'Rio Grande do Norte (RN)',
                    'U': 'Rio Grande do Sul (RS)',
                    'V': 'Rondônia (RO)',
                    'X': 'Roraima (RR)',
                    'Y': 'Santa Catarina (SC)',
                    'Z': 'São Paulo (SP)',
                    'W': 'Sergipe (SE)',
                    'Ç': 'Tocantin (TO)'
                    }

             Equipamento = 'Pegasus' 
             #CPF = str(post.Cpf_paciente)#+("_")+str(post.pk)
             doc_ref = db.collection(Equipamento).document(u'Exame')#.document(CPF+' '+date_time_txt)
             doc_ref.set({
                 str(post.four_digit_code):[str(post.Exame),
                 str(post.Nome_do_paciente),
                 str(post.Sexo),
                 str(post.Data_de_nascimento),
                 str(nome_medico),
                 str(form_update.CRM),
                 str(dicionario_estados[form_update.Estado_CRM]),
                 str(request.user.email),
                 str(post.Cpf_paciente)]

             },merge=True)
             return redirect('post_detail', pk=post.pk)
     else:
         form = PostForm(instance=post)
     return render(request, 'lab/post_edit.html', {'form': form})

def delete_post(request,pk):
    
    post=Post.objects.get(id=pk)
    Equipamento = 'Pegasus' 
    try:
        os.remove("lab/static/laudos/"+str(post.four_digit_code)+str(post.four_digit_code)+".pdf")
        #os.remove("lab/static/laudos/"+str(post.Cpf_paciente)+".png")#+("_")+str(post.pk)+".png")
    except:
        pass
    CPF = str(post.Cpf_paciente)#+("_")+str(post.pk)
    print(str(post.Cpf_paciente))
    doc_ref = db.collection(Equipamento).document(u'Exame')
    doc_ref.update({str(post.four_digit_code):firestore.DELETE_FIELD})

    post.delete()
    return redirect('/')

def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request,'lab/post_list.html',{'posts':posts})
    #return render(request,'lab/mapa.html')

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    try:
        pasta_nova = "lab/static/laudos/"+str(post.four_digit_code)
        try:
            os.mkdir(pasta_nova)
        except: 
            pass
        test = pasta_nova+"/"+str(post.four_digit_code)+".pdf"
        test1 = str(post.four_digit_code)+"/"+"Laudo"
        caminho_laudo = "laudos/"+str(post.four_digit_code)+"/"+str(post.four_digit_code)+".pdf"
        bucket.blob(test1).download_to_filename(test)
        
        return render(request, 'lab/post_detail.html', {'post': post,"caminho_laudo":caminho_laudo})
    except: 
        return render(request, 'lab/post_detail.html', {'post': post})

def register(response):
    return render()
    
def profile_user_edit(request):
     form = Profile_user_form(request.POST)
     try:
        form_update = Profile_user.objects.get(autor=request.user)
        if request.method == "POST":
            form = Profile_user_form(request.POST)
            if form.is_valid():
                post = form.save(commit=False)
                post.autor = request.user
                form_update.CRM = post.CRM
                form_update.Estado_CRM = post.Estado_CRM
                form_update.save()
                return redirect('/')
        else:
            form = Profile_user_form()
     except:
        if request.method == "POST":
            form = Profile_user_form(request.POST)
            if form.is_valid():
                post = form.save(commit=False)
                post.autor = request.user
                post.save()
                form_update = Profile_user.objects.get(autor=request.user)
                form_update.CRM = post.CRM
                form_update.Estado_CRM = post.Estado_CRM
                form_update.save()
                return redirect('/')
        else:
            form = Profile_user_form()
     return render(request, 'lab/edit_profile.html', {'form': form})

def gerar_mapa(request):
    
    ip = get('https://api.ipify.org').text
    response1 = DbIpCity.get(ip, api_key='free')
    m = folium.Map([response1.latitude, response1.longitude],tiles= 'cartodbpositron', zoom_start= 3, prefer_canvas=True,max_bounds=True,
        min_lat=-84, max_lat=84, min_lon=-220, max_lon=220)
    folium.Map()
    # Minimapa
    #minimap = plugins.MiniMap(toggle_display=True)
    #m.add_child(minimap)

    # add full screen button to map
    plugins.Fullscreen(position='topright').add_to(m)

    # Declaring points of latitude and longitude
    #my_locations = [(response1.latitude, response1.longitude),(-25.45,-49.34),(-25.45,-49.34)]
    doc_ref = db.collection('Pegasus').document(u'Exame')
    
    docs = doc_ref.get()
    exp = docs.to_dict()
    my_locations = []
    for exame_firebase in exp:
        try:
            print(exp[exame_firebase][12])
            my_locations.append((float(exp[exame_firebase][12]),float(exp[exame_firebase][13])))
        except:
            pass
    print(my_locations)

    #for i in range(0,len(exp['Geopoints']),2):
    #    my_locations.append((exp['Geopoints'][i],exp['Geopoints'][i+1]))
    marker_cluster = MarkerCluster(locations = my_locations)
        
    marker_cluster.add_to(m)    

    m.save ('lab/templates/lab/mapa.html')
    
    table_file = open('lab/templates/lab/mapa.html')
    map_lines = table_file.readlines()
    table_file.close()
    
    table_file = open('lab/templates/lab/mapa.html','w+')
    first_lines = ["{% extends 'lab/base.html' %}\n",
                        #"{% load static %} \n",
                        "{% block content %} \n",
                        "{% if user.is_authenticated %} \n"]
    end_lines = ["\n{% endif %}\n","{% endblock %}"]
    table_file.writelines(first_lines)
    table_file.writelines(map_lines)
    table_file.close()
 
    table_file = open('lab/templates/lab/mapa.html','a+')
    table_file.writelines(end_lines)
    table_file.close()

    return render(request, 'lab/mapa.html')
