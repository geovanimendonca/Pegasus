import cv2, os
import numpy as np


def image_function(imagePointer,directory,name_image):
    # Carrega imagem e converte para HSV
    image = cv2.imread(imagePointer)
    image = cv2.rotate(image,cv2.cv2.ROTATE_90_CLOCKWISE)
    original = image.copy()
    
    hsv_frame = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Mascaras

    # Mascara para resultado negativo
    negative_mask1 = cv2.inRange(hsv_frame,(160,60,60),(180,255,255)) # (0-180, 0-255, 0-255)
    negative_mask2 = cv2.inRange(hsv_frame,(0,60,60),(14,255,255)) # (0-180, 0-255, 0-255)
    mask_negative  = cv2.bitwise_or(negative_mask1,negative_mask2)
    mask_negative  = cv2.erode(mask_negative, None, iterations=2)
    mask_negative  = cv2.dilate(mask_negative, None, iterations=2)
    mask_negative  = cv2.medianBlur(mask_negative, 5)
    
    # Mascara para resultado positivo
    positive_mask1 = cv2.inRange(hsv_frame,(15,60,60),(35,255,255)) # (0-180, 0-255, 0-255)
    positive_mask2 = cv2.inRange(hsv_frame,(15,60,60),(35,255,255)) # (0-180, 0-255, 0-255)
    mask_positive  = cv2.bitwise_or(positive_mask1,positive_mask2)
    mask_positive  = cv2.erode(mask_positive, None, iterations=2)
    mask_positive  = cv2.dilate(mask_positive, None, iterations=2)
    mask_positive  = cv2.medianBlur(mask_positive, 5)

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))

    opening_positive = cv2.morphologyEx(mask_positive, cv2.MORPH_OPEN, kernel, iterations=1)
    cnts_positive    = cv2.findContours(opening_positive, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts_positive    = cnts_positive[0] if len(cnts_positive) == 2 else cnts_positive[1]
    cnts_positive1 = sorted(cnts_positive, key=cv2.contourArea, reverse=True)[:3]


    opening_negative = cv2.morphologyEx(mask_negative, cv2.MORPH_OPEN, kernel, iterations=1)
    cnts_negative    = cv2.findContours(opening_negative, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts_negative    = cnts_negative[0] if len(cnts_negative) == 2 else cnts_negative[1]
    cnts_negative1 = sorted(cnts_negative, key=cv2.contourArea, reverse=True)[:3]
    
    info_poços = []
    pos_poços = []
    x = 0
    y = 0
    
    for c1 in cnts_positive:
        if cv2.contourArea(c1)>8000:
            cv2.drawContours(original,[c1], 0, (0,0,0), 2)
            c_positive = max(c1, key=cv2.contourArea)
            (x_p, y_p), radius_p = cv2.minEnclosingCircle(c_positive)
            info_poços.append('+')
            pos_poços.append((x_p,y_p))
            text = str(info_poços[y])
            x+=1
            y+=1
            cv2.putText(original, text, (int(x_p)-int(radius_p)-5, int(y_p)-int(radius_p)-5),
                cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 0), 2)
    
    for c2 in cnts_negative:
        if cv2.contourArea(c2)>8000:
            cv2.drawContours(original,[c2], 0, (0,0,0), 2)
            c_negative = max(c2, key=cv2.contourArea)
            (x_n, y_n), radius_n = cv2.minEnclosingCircle(c_negative)
            info_poços.append('-')
            pos_poços.append((x_n,y_n))
            text = str(info_poços[y])
            x+=1
            y+=1
            cv2.putText(original, text, (int(x_n)-int(radius_n)-5, int(y_n)-int(radius_n)-5),
                cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 0), 2)
    
    #print(pos_poços)
    dicionario = {"Area1":0, "Area2":0, "Area3":0, "Area4":0}
    for num_poços in range(len(pos_poços)):
        var_x =  pos_poços[num_poços][0]
        var_y =  pos_poços[num_poços][1]
        if  (0 <= var_x <= 215) and (320 <= var_y <= 570):
            dicionario['Area1'] = info_poços[num_poços] 
        if  (250 <= var_x <= 470) and (320 <= var_y <= 570):
            dicionario['Area2'] = info_poços[num_poços]
        if  (250 <= var_x <= 470) and (0 <= var_y <= 250):
            dicionario['Area3'] = info_poços[num_poços]
        if  (0 <= var_x <= 215) and (0 <= var_y <= 250):
            dicionario['Area4'] = info_poços[num_poços]
    # CHIP
    #  -------
    # /       \
    # |       |
    # |       |
    # |       |
    # | A4 A3 |
    # |       |
    # | A1 A2 |
    # ---------

    try:
        os.mkdir(directory)
    except FileExistsError:
        pass
    cv2.imwrite(directory+"/"+name_image+".png",original)
    resultado_final = []
    # Analise de validade do teste
    if (dicionario['Area4']=='-' and dicionario['Area3']=='+'):
        resultado_final.append("valido")
        
        # Analise da Amostra 1
        if (dicionario['Area1']=='+'):
            resultado_final.append("Reagente")
        elif(dicionario['Area1']=='-'):
            resultado_final.append("Não reagente")

        # Analise da Amostra 2
        if (dicionario['Area2']=='+'):
            resultado_final.append("Reagente")
        elif(dicionario['Area2']=='-'):
            resultado_final.append("Não reagente")

    else:
        print("invalido")
        resultado_final.append("invalido")
        resultado_final.append("invalido")
        resultado_final.append("invalido")
        

    print(resultado_final)
    print(info_poços)
    return resultado_final