import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from google.cloud import storage
import os, itertools
from typing import Optional
from datetime import datetime
from initialise_firebase_admin import app
from firebase_admin import auth
from firebase_admin.auth import UserRecord
import json
import os
import requests
import pprint

FIREBASE_WEB_API_KEY = 'AIzaSyDuYp1S1udPe47Idq2zM9FCAg-X3QDUgpw'
rest_api_url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword"
rest_api_url_email = "https://identitytoolkit.googleapis.com/v1/accounts:sendOobCode"

db = firestore.client() # Database
client = storage.Client() # Storage
bucket = client.get_bucket('pythondbtest-a8bdf.appspot.com') # Caminho do Storage - Fixo

# ---------------------------- [STORAGE] --------------------------------------------------------------

#---- Upload -----
'''
ImagePath = ('tom.jpeg')
ImageBlob = bucket.blob('Pasta/Tom2') # Caminho e nome do arquivo, só o nome -> cria na raiz
ImageBlob.upload_from_filename(ImagePath)
'''
def upload_laudo(path_on_cloud, path_local):
    bucket.blob(path_on_cloud).upload_from_filename(path_local) # Caminho e nome do arquivo, só o nome -> cria na raiz
    get_file_name = bucket.get_blob(path_on_cloud)
    get_file_name.metadata = {'firebaseStorageDownloadTokens': 'Pegasus :D'}
    get_file_name.patch()
#upload_exame('Laudo', "/home/pi/Desktop/Lamp Chip/Main_lamp/Laudo/43214913808/Laudo.pdf")

#---- Download ----
#def download_laudo():
#    bucket.blob('1230/Resultado.pdf').download_to_filename('Resultado.pdf')

#download_laudo()


# Listar os objetos do Storage
'''blobs = client.list_blobs('pythondbtest-a8bdf.appspot.com') 
#for blob in blobs:
    print(blob.name)
'''

# ---------------------------- [DATABASE] -------------------------------------------------------------

#Cria coleção e documento caso não exista e adiciona os dados
#Coleção ->  Documento -> Dados 
'''doc_ref = db.collection(u'users').document(u'FioCruz')
doc_ref.set({
    u'Nome': u'Geovani',
    u'Sobrenome': u'Mendonça',
    u'Nascimento': 11121996,
    u'CPF':43214913808,
    u'Sexo':u'Masculino'
})
'''

# Se referenciar o mesmo local da informação, ele substitui
'''CPF = 43214913808
doc_ref = db.collection(u'users').document(str(CPF))
doc_ref.set({
    u'first': u'Geovani',
    u'middle': u'Torezin',
    u'last': u'Mendonça',
    u'Nascimento': 11121996
})
'''

'''cpf_referencia = db.collection(u'users')
query_ref = cpf_referencia.where(u'first',u'==',u'43214913808')
print(query_ref)
'''

# Deletar documentos
#db.collection(u'users').document(str(CPF)).delete()

# Excluir campos
'''referencia = db.collection(u'users').document(str(CPF))
referencia.update({
    u'Nascimento':firestore.DELETE_FIELD
    })
'''

# Excluir coleção
'''for x in range (1,11):
    y=('Enfermeiro','Médico','Pacientes')
    for yy in y:
        users_ref = db.collection(u'Equipamento '+str(x)).document(u'Usuarios').collection(str(yy))
        docs = users_ref.stream()
        for doc in docs:
            doc.reference.delete()
'''

# Puxa todos os dados do banco de dados e printa na tela
def load_data(Db_collection, Db_document, campo):
    print("Loading data...")
    try:
        users_ref = db.collection(Db_collection).document(Db_document)
        docs = users_ref.get()
        exp = docs.to_dict()
        print(exp[campo])
        return exp[campo]
    except:
        return("Erro")
        
#load_data('Pegasus', 'Exame', '4115')
#load_data('Pegasus','Exame','CPF paciente')


def upload_exame(ID,VAR1,VAR2,VAR3,VAR4,VAR5,VAR6,VAR7,VAR8,VAR9,VAR10,VAR11,VAR12,VAR13,VAR14,VAR15,VAR16):
    print("Uploading exame info")
    Equipamento = 'Pegasus'
    date_time = datetime.now()
    date_time_txt = date_time.strftime('%d/%m/%Y %H:%M')
    doc_ref = db.collection(Equipamento).document(u'Exame')
    doc_ref.set({
       ID:[VAR1,VAR2,VAR3,VAR4,VAR5,VAR6,VAR7,VAR8,VAR9,VAR10,VAR11,VAR12,VAR13,VAR14,VAR15,VAR16,date_time_txt]
    },merge=True)
    

                                        
def upload_user(nome,email,senha):
    print("Uploading user info")
    Equipamento = 'Equipamento'
    date_time = datetime.now()
    date_time_txt = date_time.strftime('%d/%m/%Y %H:%M')
    doc_ref = db.collection(Equipamento).document(u'Users')
    doc_ref.set({
       nome:[nome,email,senha,date_time_txt]
    }, merge  = True)

def update_email(user_id: str, email: str) -> UserRecord:
    return auth.update_user(user_id, email=email)

def update_mobile(user_id: str, mobile_no: str) -> UserRecord:
    return auth.update_user(user_id, phone_number=mobile_no)

def update_display_name(user_id: str, display_name: str) -> UserRecord:
    return auth.update_user(user_id, display_name=display_name)

def set_password(user_id: str, password: str) -> UserRecord:
    return auth.update_user(user_id, password=password)

def email_verification_link(id_token: str):
    payload = json.dumps({
        "requestType": "VERIFY_EMAIL",
        "idToken": id_token
    })

    r = requests.post(rest_api_url_email,
                      params={"key": FIREBASE_WEB_API_KEY},
                      data=payload)

    return r.json()

def create_user(email: str) -> UserRecord:  
    return auth.create_user(email=email, email_verified=0)

def delete_user(user_id: str):
    return auth.delete_user(user_id)

def user_uid(email: str) -> UserRecord:
    result = auth.get_users([auth.EmailIdentifier(email)])
    for user in result.users:
        uid = user.uid
    return  uid

def get_user_uid(user_email: str) -> UserRecord:
    result = auth.get_user_by_email(user_email).uid
    return result

def get_user_verify(user_email: str) -> UserRecord:
    result = auth.get_user_by_email(user_email).email_verified
    return result

def sign_in(email: str, password: str, return_secure_token: bool = True):
    payload = json.dumps({
        "email": email,
        "password": password,
        "returnSecureToken": return_secure_token
        
    })

    r = requests.post(rest_api_url,
                      params={"key": FIREBASE_WEB_API_KEY},
                      data=payload)
    return r.json()
