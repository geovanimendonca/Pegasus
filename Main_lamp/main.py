from kivy.config import Config
Config.set('input', 'mouse', 'mouse,multitouch_on_demand')
from kivy.uix.screenmanager import Screen
from kivymd.app import MDApp
from kivymd.uix.button import MDRectangleFlatButton
from kivy.app import App
from kivy.uix.progressbar import ProgressBar
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty,StringProperty,NumericProperty, BooleanProperty, ListProperty
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.garden.graph import Graph, MeshLinePlot
from kivy.config import Config
from kivy.clock import Clock
from kivy.factory import Factory
from kivy.uix.image import Image
from kivy.animation import Animation
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics.texture import Texture
from kivy.core.window import Window
from functools import partial
from random import randint
from math import sin
from pyzbar import pyzbar
import threading, serial, sys, time, cv2, Laudo, ident, os, shutil
from datetime import datetime
import qrcode
import numpy as np
from numpy import random
from datetime import datetime, timedelta
import pynput       
import makegif
from pynput.keyboard import Key, Controller
from ip2geotools.databases.noncommercial import DbIpCity
from requests import get

keyboard = Controller()

try: # Firebase
    import firebase
except:
    print("Sem internet")

class CreateAccountWindow(Screen):
    namee = ObjectProperty(None)
    email = ObjectProperty(None)
    password = ObjectProperty(None)
    def close_app(self):
        close_application()
    def submit(self):
        try:
            firebase.create_user(self.email.text)
            print("Create OK")
            uid_user = firebase.get_user_uid(self.email.text)
            print("UID OK")
            firebase.set_password(uid_user, self.password.text)
            print("password OK")
            firebase.update_display_name(uid_user, self.namee.text)
            print("name OK")
            token = firebase.sign_in(self.email.text,self.password.text)
            print("sign OK")
            a = firebase.email_verification_link(token['idToken'])
            print("Criado com sucesso")
            sm.current= "login"
        except:
            invalidForm()
            self.email.text = ""
            self.password.text = ""
            self.namee.text = ""

    def login(self):
        self.reset()
        sm.current = "login"

    def reset(self):
        self.email.text = ""
        self.password.text = ""
        self.namee.text = ""

class LoginWindow(Screen):
    email = ObjectProperty(None)
    password = ObjectProperty(None)
    
    def close_app(self):
        close_application()
    def loginBtn(self):
        global executor_nome
        try:
            executor_nome = self.email.text
            info_usuario = firebase.sign_in(self.email.text,self.password.text)
            if info_usuario['registered']:
                usuario_cadastrado = True
            else:
                usuario_cadastrado = False
        except:
            usuario_cadastrado= False
            invalidLogin()
            self.reset()
            
        if usuario_cadastrado:
            try:
                usuario_verificado = firebase.get_user_verify(self.email.text)
            except:
                usuario_verificado = False
                print("usuario não verificado")
                invalidLogin()
                self.reset()

        if usuario_cadastrado and usuario_verificado:
            self.reset()
            sm.current = "main"
        else:
            invalidLogin()

    def createBtn(self):
        self.reset()
        sm.current = "create"
    
    def reset(self):
        self.email.text = ""
        self.password.text = ""
    
class MainWindow(Screen):
    def voltar(slf):
        sm.current="login"
    def tipoexame(self):
        sm.current="qrcode"
    def close_app(self):
        close_application()
                   
class TipoExame(Screen):
    def voltar(self):
        sm.current="qrcode"
    def close_app(self):
        close_application()
    def leishmania(self):
        global temperatura_exame, ser
        temperatura_exame = 65
        ser.write(b'x'+str(temperatura_exame).encode('ascii'))
        sm.current="qrcode"
        
    def covid(self):
        global temperatura_exame, ser
        temperatura_exame = 65
        ser.write(b'x'+str(temperatura_exame).encode('ascii'))
        sm.current="play"
    
class Play(Screen):
    pb = ProgressBar(max=100)
    relogio = ObjectProperty(None)
    temperatura = ObjectProperty(None)
    play_habilitado=True
    enable_export=True
    ciclo_1 = False
    foto = 10
    info_arduino=''
    minuto_1=0
    
    def on_enter(self):
        global texture1
        
        global iniciar_threads, texture1
        self.ids.imagem_camera.texture = texture1
        if iniciar_threads:
            def serial_aquisition():
                global ser, leitura_serial, button_start_efeito
                while True:
                    try:
                        read_info_arduino = ser.readline()
                        leitura_serial = read_info_arduino
                        
                        if button_start_efeito == 1:
                            self.ids.start_button.background_color = [0,10,0,1]
                        elif button_start_efeito == 0:
                            self.ids.start_button.background_color = [0,1,0,1]

                        if button_stop_efeito  == 1:
                            self.ids.stop_button.background_color = [10,0,0,1]
                        elif button_start_efeito:
                            self.ids.stop_button.background_color = [1,0,0,1]
                        
                        try:
                            self.info_arduino = ''
                            self.info_arduino = str(chr(read_info_arduino[0]))+str(chr(read_info_arduino[1]))+str(chr(read_info_arduino[3]))+str(chr(read_info_arduino[4]))
                            self.info_arduino = float(self.info_arduino)/100
                            self.temperatura.text="Temperatura atual: "+str(self.info_arduino)+"ºC"
                        except:
                            self.info_arduino=[]
                    except:
                        pass
                        
            def time_run():
                global tempo_exame_segundos, habilita_passar_tempo, habilita_timer, tempo_exame, stop_geral, pre_aquecer
                while True:
                    try:
                        if habilita_passar_tempo:
                            tempo_exame_segundos = datetime.now()
                            new_final = tempo_exame_segundos + timedelta(seconds=tempo_exame*60)
                            time_final = timedelta(seconds= 1)
                            time_export_image = timedelta(seconds = tempo_exame*60)
                            habilita_passar_tempo = False
                        if habilita_timer:
                            now1 = datetime.now()
                            if(str(tempo_exame_segundos) != '0:00:00'):
                                tempo_exame_segundos = datetime.now()
                                tempo_exame_segundos_1 = new_final - tempo_exame_segundos
                                if tempo_exame_segundos_1 <= time_export_image:
                                    self.export()
                                    time_export_image = time_export_image - timedelta(seconds = 30)
                                string_time = str(tempo_exame_segundos_1).split(".")[0]
                                self.relogio.text = "Tempo decorrido: " + str(string_time)
                            if(tempo_exame_segundos_1 <= time_final):
                                habilita_timer = False
                        if stop_geral and not pre_aquecer:
                            self.relogio.text = "Esfriando"
                    except:
                        pass

            def update_camera_test(dt):
                global capture, texture1
                ret, frame = capture.read()
                buf1 = cv2.flip(frame, 0)
                buf = buf1.tostring()
                texture1.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')

            #Initiate camera
            Clock.schedule_interval(update_camera_test, 1.0/60.0)
            
            #Initiate parallel timer                
            self.time_parallel_process = threading.Thread(target=time_run)
            self.time_parallel_process.start()
            
            #Initiate a parallel process to recieve arduino information
            self.serial_parallel_process = threading.Thread(target=serial_aquisition)
            self.serial_parallel_process.start()
            iniciar_threads = False
        
    def voltar(self):
        sm.current="tipoexame"

    def preaquecer(self):
        
        global pre_aquecer
        global ser, read_img, setpoint, leitura_serial, setpoint_spin, time_spin, habilita_passar_tempo, habilita_timer, condicao_cooling, stop_geral
        setpoint = setpoint_spin
        ser.write(b'x'+str(setpoint).encode('ascii'))
        self.ids.setpointlabel.text="Setpoint atual: 65.0" + "ºC"
        self.relogio.text = "Pre aquecendo"
        pre_aquecer = True
    
    def close_app(self):
        close_application()
        
    def export(self,*args):
        global diretorio, image_counter, capture, texture1
        ret, frame = capture.read()
        now = datetime.now()
        path = '/home/pi/Desktop/Lamp Chip/Main_lamp/'+ diretorio
        image_name = str(image_counter)+".png"
        cv2.imwrite(os.path.join(path, image_name),frame)
        image_counter += 1
        
    def identify_image(self):
        global diretorio, capture
        ret, frame = capture.read()
        path = '/home/pi/Desktop/Lamp Chip/Main_lamp/Resultado'
        image_name = "resultado.png"
        cv2.imwrite(os.path.join(path, image_name),frame)
        
    def update(self,*args):
        global tempo_exame, ser, read_img, setpoint, leitura_serial, setpoint_spin, time_spin, habilita_passar_tempo, habilita_timer, condicao_cooling, stop_geral
        stop_geral  = False
        try:
            read_info_arduino = float(leitura_serial)
        except:
            pass
        # Foto a cada minuto
        if habilita_timer:
            condicao_cooling = True
                
        # Esfriar
        elif(habilita_timer == False and (read_info_arduino>=30) and condicao_cooling):
            self.ciclo_1=False
            ser.write(b'x250')
            self.ids.relogio.text ="Esfriando"
            
        # Fim de exame    
        else:
            self.reset()
            ser.write(b'x250')
            sm.current="resultado"
            condicao_cooling = False
            self.identify_image()
    
    def reset(self):
        global ser,sm, button_start_efeito, button_stop_efeito, habilita_passar_tempo, habilita_timer,tempo_exame_segundos, stop_geral, pre_aquecer
        try:
            ser.write(b'x250')
            stop_geral  = True
            Clock.unschedule(self.event)
        except:
            pass
        self.ids.preheat.opacity = 1
        self.ids.preheat.disabled = False
        habilita_passar_tempo = False
        pre_aquecer = False
        habilita_timer = False
        button_start_efeito = 0
        button_stop_efeito = 1
        self.segundo_1 = 0
        self.minuto_1 = 0
        self.time_end_1 = 0
        self.enable_export = True
        self.play_habilitado=True
        self.ids.setpointlabel.text="Setpoint atual: 25.0ºC"

    def call(self,*args):
        global setpoint, tempo_exame, diretorio, button_start_efeito, button_stop_efeito, setpoint_spin, time_spin, habilita_passar_tempo, habilita_timer, image_counter, pre_aquecer
        button_start_efeito = 1
        button_stop_efeito = 0
        
        try:
            setpoint = setpoint_spin
            tempo_exame = time_spin
            if self.play_habilitado==True:
                image_counter = 0
                habilita_passar_tempo = True
                self.ids.preheat.opacity = 0
                self.ids.preheat.disabled = True
                habilita_timer = True
                pre_aquecer = False
                now1 = datetime.now()
                now = now1.strftime("%d-%m-%Y-%H-%M")
                diretorio = "Fotos_processo/"+now
                os.mkdir(diretorio)
                self.export()
                self.ids.setpointlabel.text="Setpoint atual: "+str(setpoint/10) + "ºC"
                ser.write(b'x'+str(setpoint).encode('ascii'))
                ser.reset_output_buffer()
                ser.reset_input_buffer()
                self.event=Clock.schedule_interval(partial(self.update),0.95)
                self.play_habilitado=False
                
        except:
            self.ids.relogio.text ="Error 1"
            
    def increase_setpoint_spin(self,dt):
        global setpoint_spin
        if (setpoint_spin <= 740):
            setpoint_spin += 1
            self.ids.setpoint.text = str(setpoint_spin/10)
     
    def decrease_setpoint_spin(self,dt):
        global setpoint_spin
        if (setpoint_spin >= 100):
            setpoint_spin -= 1
            self.ids.setpoint.text = str(setpoint_spin/10)
     
    def increase_time_spin(self,dt):
        global time_spin
        if (time_spin <= 58):
            time_spin += 1
            self.ids.tempo.text = str(time_spin)
     
    def decrease_time_spin(self,dt):
        global time_spin
        if (time_spin >= 2):
            time_spin -= 1
            self.ids.tempo.text = str(time_spin)
    
    def start_increase_setpoint_spin (self):
        Clock.schedule_interval(self.increase_setpoint_spin, 0.01)
    def stop_increase_setpoint_spin (self):
        Clock.unschedule(self.increase_setpoint_spin)

    def start_decrease_setpoint_spin (self):
        Clock.schedule_interval(self.decrease_setpoint_spin, 0.01)
    def stop_decrease_setpoint_spin (self):
        Clock.unschedule(self.decrease_setpoint_spin)

    def start_increase_time_spin (self):
        Clock.schedule_interval(self.increase_time_spin, 0.01)
    def stop_increase_time_spin (self):
        Clock.unschedule(self.increase_time_spin)

    def start_decrease_time_spin (self):
        Clock.schedule_interval(self.decrease_time_spin, 0.01)
    def stop_decrease_time_spin (self):
        Clock.unschedule(self.decrease_time_spin)
        
class Resultado(Screen):
    
    def close_app(self):
        close_application()
        
    def on_enter(self):
        global exame,paciente_sexo, paciente_nascimento, paciente_nome
        global medico_nome, medico_email, medico_crm, medico_estadocrm
        global executor_nome, executor_id, unidade_saude, four_digit_code, local_ip,cpf_paciente
        #                     nome imagem    pasta    nome imagem identificada
        resultado_identificacao = ident.image_function('/home/pi/Desktop/Lamp Chip/Main_lamp/Resultado/resultado.png',"Resultado","resultado_ident")
        resultado_amostra_valida = resultado_identificacao[0]
        resultado_amostra_1 = resultado_identificacao[1]
        resultado_amostra_2 = resultado_identificacao[2]

        ip = get('https://api.ipify.org').text
        response = DbIpCity.get(ip, api_key='free')
        local_ip = response.city+" "+response.region+" "+response.country
        firebase.upload_exame(four_digit_code,
                                        exame,
                                        paciente_nome,
                                        paciente_sexo,
                                        paciente_nascimento,
                                        medico_nome,
                                        medico_crm,
                                        medico_estadocrm,
                                        medico_email,
                                        cpf_paciente,
                                        resultado_amostra_valida,
                                        executor_nome,
                                        local_ip,
                                        response.latitude,
                                        response.longitude,
                                        resultado_amostra_1,
                                        resultado_amostra_2)
                                         
        try:
            if four_digit_code != "none":
                Laudo.main(four_digit_code,
                            paciente_nome,
                            paciente_sexo,
                            'Informação excluida',
                            paciente_nascimento,
                            medico_nome,
                            medico_crm,
                            medico_email,
                            medico_estadocrm,
                            resultado_amostra_1,
                            resultado_amostra_2,
                            'LAMP',
                            'Extração',
                            exame,
                            four_digit_code,
                            executor_nome,
                            local_ip
                            )
                
                horario = datetime.now()
                string_time_1 = str(horario).split(":")[0] + ":" + str(horario).split(":")[1]
                firebase.upload_laudo(str(four_digit_code)+'/Laudo','Laudo/'+str(four_digit_code)+"/Laudo.pdf")
                firebase.upload_laudo(str(four_digit_code)+"/Resultado",'Resultado/resultado_ident.png')
                self.ids.label_salvo.color = (0,0,0)
                self.ids.label_salvo.text = 'Exame salvo com sucesso!'
                
            else:
                self.ids.label_salvo.text = 'Exame não salvo - Código inválido'
                self.ids.label_salvo.color = (1,0,0)
                print("entrou no else")
                print(four_digit_code)
        except:
            
            self.ids.label_salvo.text = 'Exame não salvo - Sem conexão'
            self.ids.label_salvo.color = (1,0,0)
            print("entrou no except")
        
    def finalizar(self):
        sm.current= "qrcode"
        
class Qrcode(Screen):

    
    def close_app(self):
        close_application()
    
    def voltar(self):
        sm.current="main"
        
    def start(self):
        sm.current="play"
        
    def pop_up(self,qrcode_data):
        
        def avancar(self):
            global exame, paciente_sexo, paciente_nascimento, paciente_nome
            global     medico_nome, medico_email, medico_crm, medico_estadocrm
            global     executor_nome, executor_id, unidade_saude, cpf_paciente, four_digit_code

            exame = qrcode_data[0]
            paciente_nome = qrcode_data[1]
            paciente_sexo = qrcode_data[2]
            paciente_nascimento = qrcode_data[3]
            medico_nome = qrcode_data[4]
            medico_crm = qrcode_data[5]
            medico_estadocrm = qrcode_data[6]
            medico_email = qrcode_data[7]
            cpf_paciente = qrcode_data[8]

            pop.dismiss()
            sm.current="play"
    
        def pop_close(self):
            pop.dismiss()   
            
        box = BoxLayout(orientation='vertical')    
        box1 = BoxLayout(orientation='horizontal')
        box2 = BoxLayout(orientation='horizontal')
        box3 = BoxLayout(orientation='horizontal')
        botoes = BoxLayout()
        
        sim = Button(text='Confirmar',on_release=avancar)
        nao = Button(text='Cancelar',on_release=pop_close)
        
        botoes.add_widget(sim)
        botoes.add_widget(nao)
        
        box1.add_widget(Label(text='Exame:')) #Exame - label
        box1.add_widget(Label(text=str(qrcode_data[0]))) #Exame
        box2.add_widget(Label(text='Paciente:')) #Nome do paciente - label
        box2.add_widget(Label(text=str(qrcode_data[1]))) #Nome do paciente
        box3.add_widget(Label(text='CPF:')) #Cpf do paciente - label
        box3.add_widget(Label(text=str(qrcode_data[8]))) #Cpf do paciente
        
        box.add_widget(box1)
        box.add_widget(box2)
        box.add_widget(box3)
        box.add_widget(botoes)
        
        pop = Popup(title='Informações do Exame',
                    content=box, auto_dismiss=False, 
                    size_hint=(None, None), size=(400, 300))
        pop.open()

    def pop_up_erro(self):

        def pop_close(self):
            pop.dismiss()  
        
        box = BoxLayout(orientation='vertical')
        botoes = BoxLayout()
        sim = Button(text='Ok',on_release=pop_close)
        
        box1 = BoxLayout(orientation='horizontal')
    
        box1.add_widget(Label(text='Exame não encontrado'))

        box.add_widget(box1)
        box.add_widget(botoes)
        
        pop = Popup(title='Erro',
                    content=box, auto_dismiss=True, 
                    size_hint=(None, None), size=(200, 150))
        pop.open()
        
    def update(self):
        global four_digit_code
        four_digit_code = str(self.ids.exam_code.text)
  
        info_base = firebase.load_data('Pegasus', 'Exame', four_digit_code)
        if (info_base == 'Erro'):
            self.pop_up_erro()
        else:
            self.pop_up(info_base)
    
    def number_0(self):
        self.ids.exam_code.text = self.ids.exam_code.text+'0'
        
    def number_1(self):
        self.ids.exam_code.text = self.ids.exam_code.text+'1'
        
    def number_2(self):
        self.ids.exam_code.text = self.ids.exam_code.text+'2'
        
    def number_3(self):
        self.ids.exam_code.text = self.ids.exam_code.text+'3'
        
    def number_4(self):
        self.ids.exam_code.text = self.ids.exam_code.text+'4'
        
    def number_5(self):
        self.ids.exam_code.text = self.ids.exam_code.text+'5'
        
    def number_6(self):
        self.ids.exam_code.text = self.ids.exam_code.text+'6'
        
    def number_7(self):
        self.ids.exam_code.text = self.ids.exam_code.text+'7'
        
    def number_8(self):
        self.ids.exam_code.text = self.ids.exam_code.text+'8'
        
    def number_9(self):
        self.ids.exam_code.text = self.ids.exam_code.text+'9'

    def delete_info(self):
        self.ids.exam_code.text = ''
        
     
def invalidLogin():
    pop = Popup(title='Login inválido',
                  content=Label(text='Usuário ou senha inválidos'),
                  size_hint=(None, None), size=(250, 250))
    pop.open()

def invalidForm():
    pop = Popup(title='Formulário inválido',
                  content=Label(text='Dados inválidos, tente novamente'),
                  size_hint=(None, None), size=(250, 250))

    pop.open()

def close_application():
        App.get_running_app().stop()
        Window.close()
        exit()

kv = Builder.load_file("my.kv")

class WindowManager(ScreenManager):
    pass
    
sm = WindowManager()

screens = [LoginWindow(name="login"), CreateAccountWindow(name="create"),
           MainWindow(name="main"),Qrcode(name="qrcode"),TipoExame(name="tipoexame"),
           Play(name="play"),Resultado(name="resultado")]

for screen in screens:
    sm.add_widget(screen)
    
    
sm.current = "main" # Tela em que inicia

#-------------------------------------------------------
#                    Global

try:
    ser = serial.Serial("/dev/ttyUSB0", 9600)
except:
    try:
        ser = serial.Serial("/dev/ttyUSB1", 9600)
    except:
        print("Arduino desconectado")
        
tempo_exame = 1
setpoint = 20
leitura_serial = 0
button_start_efeito = 0
button_stop_efeito = 0
setpoint_spin = 650
time_spin = 30
image_counter = 0
habilita_passar_tempo = False
tempo_exame_segundos = timedelta(seconds=10)
habilita_timer = False
iniciar_threads = True
condicao_cooling = False
stop_geral= False
pre_aquecer = False

exame = "none"
paciente_nome = "none"
paciente_sus = "none"
paciente_sexo = "none"
paciente_nascimento = "none"
medico_nome = "none"
medico_email = "none"
medico_crm = "none"
medico_estadocrm = "none"
executor_nome = "none"
unidade_saude = "none"
four_digit_code = "none"


#Initiate camera as global
capture = cv2.VideoCapture(0)
#Create global texture to save camera frame
texture1 = Texture.create(size=(640,480) , colorfmt='rgba')

#-------------------------------------------------------
    
class MyMainApp(App):   
    title = "LAB on a chip"
    def build(self):
        return sm
        
if __name__ == "__main__":
    Window.size=(640,480)
    Window.fullscreen = True
    MyMainApp().run()
    
