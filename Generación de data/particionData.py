import os
import sys
import numpy as np


def particionData(directorio, salida ,porcentaje_entrenamiento, porcentaje_total):
    carpeta = os.listdir(directorio)
    carpeta = np.random.permutation(carpeta)
    largo = len(carpeta)
    maximo = int ((largo/2) * porcentaje_total)
    maximo_entrenamiento =  maximo *porcentaje_entrenamiento
    train = open("train.txt",'a')
    valid = open("test.txt",'a')
    contador = 0
    for image in carpeta:
        if image[-1] =="g":
            if contador < maximo_entrenamiento:
                train.write(salida+"/"+image+"\n")
            elif contador < maximo:
                valid.write(salida+"/"+image+"\n")
            else:
                break
            contador+=1
	train.close()
    valid.close()
            
if __name__ == '__main__':
	particionData(argv[1],argv[2], argv[3],argv[4])


