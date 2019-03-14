import cv2
import random
import numpy as np
from matplotlib import pyplot as plt
import os



fondo = np.array([0,0,0])
numero_clases = 5



def insertar( escena , objeto, clase, archivo):
    alto_o, ancho_o, x = objeto.shape 
    alto_e, ancho_e, x = escena.shape
    x = random.randrange(alto_e)
    y = random.randrange(ancho_e)
    
    # Elegir un punto dentro de la escena
    while np.linalg.norm(np.array(escena[x][y])-fondo) < 50:
        x = random.randrange(alto_e)
        y = random.randrange(ancho_e)
        
    # Inicialización de posiciones
    inicio_x = x - int(alto_o / 2)
    inicio_y = y - int(ancho_o / 2)
    inicio_x_escena = 0
    inicio_y_escena = 0
    
    # Valores para .txt Yolo 
    width = ancho_o / ancho_e
    height = alto_o / alto_e
    x_yolo = y/ ancho_e
    y_yolo = x/ alto_e
    archivo.write(clase+" "+str(x_yolo)+" "+str(y_yolo)+" "+str(width)+" "+str(height)+"\n")
    
    #Seteo de valores en x
    if inicio_x < 0:
        inicio_x_escena = 0
        inicio_x = inicio_x * -1  
    else:
        inicio_x_escena = inicio_x
        inicio_x = 0
        
    #Seteo de valores en y
    if inicio_y < 0:
        inicio_y_escena = 0
        inicio_y = inicio_y * -1  
    else:
        inicio_y_escena = inicio_y
        inicio_y = 0
          
    
    # Iteracion sobre la escena y el objeto
    count_x = 0
    for h in list(range(inicio_x,alto_o)):
        if count_x + inicio_x_escena >= alto_e :
            break
        count_y = 0
        for w in list(range(inicio_y, ancho_o)):
            if count_y + inicio_y_escena >= ancho_e :
                break
            if np.linalg.norm(np.array(objeto[h][w])-fondo) > 9:
                escena[count_x + inicio_x_escena][count_y +inicio_y_escena] = objeto[h][w]
            count_y += 1
        count_x += 1



def creador(dir_escenas, dir_objetos, min_elementos , max_elementos, salida= " Data "):
    os.mkdir(salida)
    escenas = os.listdir(dir_escenas)
    objetos = os.listdir(dir_objetos)
    n_objetos = len(objetos)
    contador = 0  
    #Iteracion por escenas
    for escena_x in escenas:
        escena_original = cv2.imread(dir_escenas + "/" + escena_x)
        #Iteracion por numero de objetos
        for n_elementos in list(range(min_elementos,max_elementos+1)):
            if n_elementos == 0:
                n_combinaciones = 1
            else:
                n_combinaciones = 200
            #Iteracion por combinaciones
            for alpha in list(range(n_combinaciones)):
                escena = escena_original.copy()
                archivo = open(salida + "/" +str(contador)+".txt",'a')
                # Insercion de objetos
                for i in list(range(n_elementos)):
                    c = random.randrange(numero_clases)
                    pos = random.randrange(n_objetos)
                    while int(objetos[pos].split("_")[0]) !=  c:
                        pos = random.randrange(n_objetos)
                    objeto = cv2.imread(dir_objetos + "/" + objetos[pos])
                    clase = objetos[pos].split("_")[0]
                    insertar( escena , objeto, clase, archivo)
                cv2.imwrite(salida + "/" +str(contador)+".jpg",escena)
                archivo.close()
                contador += 1
                
                
            
    
if __name__ == '__main__':
	if sys.argv.len == 6
		creador(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
	else:
		creador(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
   

