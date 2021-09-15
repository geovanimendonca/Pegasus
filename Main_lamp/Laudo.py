from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
import os, shutil
from datetime import datetime

def main(four_digit_code,
            paciente_nome,
            paciente_sexo,
            paciente_codigo_sus,
            paciente_nascimento,
            medico_nome,
            medico_crm,
            medico_email,
            medico_estado_crm,
            resultado_amostra_1,
            resultado_amostra_2,
            metodo,
            amostra,
            doenca_testada,
            info_id,
            info_nome_executor,
            info_unidade_saude,
            ):
                
    horario = datetime.now()
    string_time = str(horario).split(":")[0] + ":" + str(horario).split(":")[1]
    data_hora_exame = (str(horario).split("-")[2].split(" ")[0]+"/"
                        +str(horario).split("-")[1].split("-")[0]+"/"
                        +str(horario).split("-")[0]+" - "
                        +str(horario).split("-")[2].split(" ")[1].split(":")[0]+":"
                        +str(horario).split("-")[2].split(" ")[1].split(":")[1])
    
    
    c = canvas.Canvas("Laudo.pdf",pagesize=A4,bottomup=0)
    width, height = A4
    c.translate(50,10)
    # Inverting the scale for getting mirror Image of logo
    c.scale(1,-1)
    # Inserting Logo into the Canvas at required position
    try:
        c.drawImage("Wallpaper/logo_fiocruz.png",(132+50)*2,-50,width = 132,height = 40)
        c.drawImage("/home/pi/Desktop/Lamp Chip/Main_lamp/Resultado/resultado_ident.png",(132+50)*1.5,-770,width = 211.2,height = 281.6)
    except:
        print("Não foi possivel carregar a imagem")
    # Again Inverting Scale For strings insertion
    c.scale(1,-1)
    
    # Cabeçalho
    c.translate(-50,35)
    c.setFont("Helvetica-Bold",12)
    c.drawCentredString(297.5,0,"Resultado")
    c.translate(0,20)
    c.setFont("Helvetica-Bold",12)
    c.translate(50,14)
    c.drawString(0,0, "Amostra 1")
    c.setFont("Helvetica",12)
    c.setFillColorRGB(1,0,0) # Vermelho
    c.drawString(0,14, resultado_amostra_1)
    c.setFillColorRGB(0,0,0) # Preto

    c.setFont("Helvetica-Bold",12)
    c.translate(150,0)
    c.drawString(0,0, "Amostra 2")
    c.setFont("Helvetica",12)
    c.setFillColorRGB(1,0,0) # Vermelho
    c.drawString(0,14, resultado_amostra_2)
    c.setFillColorRGB(0,0,0) # Preto
    c.translate(-150,0)
    
    c.setFont("Helvetica-Bold",12)
    c.drawString(0,14*2+10, "Método")
    c.setFont("Helvetica",12)
    c.drawString(0,14*3+10, metodo)
    c.setFont("Helvetica-Bold",12)
    c.drawString(0,14*4+20, "Amostra")
    c.setFont("Helvetica",12)
    c.drawString(0,14*5+20, amostra)
    c.setFont("Helvetica-Bold",12)
    c.drawString(270,14*4+20, "Data/Hora do exame")
    c.setFont("Helvetica",12)
    c.drawString(270,14*5+20, data_hora_exame)

    # PACIENTE
    c.translate(0,124)
    c.setFont("Helvetica-Bold",14)
    c.drawString(0,0, "Paciente")
    c.translate(0,2)
    c.setLineWidth(.2)
    c.line(0,0,450,0)
    c.setFont("Helvetica-Bold",12)
    c.drawString(0,14*2, "Nome")
    c.setFont("Helvetica",12)
    c.drawString(0,14*3, paciente_nome)
    c.setFont("Helvetica-Bold",12)
    c.drawString(270,14*2, "Sexo")
    c.setFont("Helvetica",12)
    c.drawString(270,14*3, paciente_sexo)
    c.setFont("Helvetica-Bold",12)
    c.drawString(0,14*4+10, "Data de nascimento")
    c.setFont("Helvetica",12)
    c.drawString(0,14*5+10, paciente_nascimento)

    # Médico
    c.translate(0,124)
    c.setFont("Helvetica-Bold",14)
    c.drawString(0,0, "Médico")
    c.translate(0,2)
    c.line(0,0,450,0)
    c.setFont("Helvetica-Bold",12)
    c.drawString(0,14*2, "Nome")
    c.setFont("Helvetica",12)
    c.drawString(0,14*3, medico_nome)
    c.setFont("Helvetica-Bold",12)
    c.drawString(270,14*2, "E-mail")
    c.setFont("Helvetica",12)
    c.drawString(270,14*3, medico_email)
    c.setFont("Helvetica-Bold",12)
    c.drawString(0,14*4+10, "CRM")
    c.setFont("Helvetica",12)
    c.drawString(0,14*5+10, medico_crm)
    c.setFont("Helvetica-Bold",12)
    c.drawString(270,14*4+10, "Estado do CRM")
    c.setFont("Helvetica",12)
    c.drawString(270,14*5+10, medico_estado_crm)

    # Informações complementares
    c.translate(0,124)
    c.setFont("Helvetica-Bold",14)
    c.drawString(0,0, "Informações complementares")
    c.translate(0,2)
    c.line(0,0,450,0)
    c.setFont("Helvetica-Bold",12)
    c.drawString(0,14*2, "E-mail do executor")
    c.setFont("Helvetica",12)
    c.drawString(0,14*3, info_nome_executor)

    c.setFont("Helvetica-Bold",12)
    c.drawString(270,14*2, "Chip identificado")
    
    c.setFont("Helvetica-Bold",12)
    c.drawString(0,14*4+10, "ID do exame")
    c.setFont("Helvetica",12)
    c.drawString(0,14*5+10, info_id)
    c.setFont("Helvetica-Bold",12)
    c.drawString(0,14*7+10, "Unidade de saúde")
    c.setFont("Helvetica",12)
    c.drawString(0,14*8+10, info_unidade_saude)

    # Salvar
    c.save()

    # Exportar para pdf
    try:
        os.mkdir("Laudo")
    except: 
        pass
    
    try:
        os.remove("Laudo/"+str(four_digit_code))
    except:
        pass
        
    try:
        os.mkdir("Laudo/"+str(four_digit_code))
    except:
        pass
    
    dir = os.listdir()
    for file in dir:
        if file == "Laudo.pdf":
            shutil.move(file,"Laudo/"+str(four_digit_code)+"/"+file)
