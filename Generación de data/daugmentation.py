import imgaug as ia
from imgaug import augmenters as iaa
import numpy as np
import os
import cv2
from Bordes import maxContorno
from Bordes import auto_canny
import shutil


#Convoluciones
#dau1 = iaa.Grayscale(alpha=(0.1, 0.5))
#dau2 = iaa.GaussianBlur(sigma=(0.0, 3.0))
#dau3 = iaa.AverageBlur(k=(2, 4))
#dau4 = iaa.Add((-40, 40))
dau5 = iaa.Add((-20, -20), per_channel=0.5)
#dau6 = iaa.Multiply((0.7, 1.2))
dau7 = iaa.Dropout(p=(0, 0.1))
dau8 = iaa.ContrastNormalization((0.7, 1.3))

conv = [dau5, dau7, dau8]

# Transformacion afin
dau9  = iaa.Affine(scale=(0.4, 0.7))
dau10 = iaa.Affine(rotate=(-90, 90))
dau11 = iaa.Affine(shear=(-2, 2))

afines = [dau9, dau11,dau10]



def aumentarData(dir_in, transformaciones, contador, iterador, copia = False):
    for dau in transformaciones:
        carpeta = os.listdir(dir_in)
        for img in carpeta:
            if img[-1] == 'g':
                foto = img.split(".")[0]
                image = cv2.imread(dir_in+"/"+img)
                count = 0
                for _ in range(iterador):
                    image_au = dau.augment_image(image)
                    cv2.imwrite(dir_in+"/"+foto+"_"+str(contador)+"-"+str(count)+".jpg", image_au)
                    # Copia de coordenadas para Yolo
                    if copia:
                        with open(dir_in+"/"+foto+".txt", 'rb') as forigen:
                            with open(dir_in+"/"+foto+"_"+str(contador)+"-"+str(count)+".txt", 'wb') as fdestino:
                                shutil.copyfileobj(forigen, fdestino)
                    count += 1
        contador += 1

            
def obtenerRecuadro(dir_in):
    carpeta = os.listdir(dir_in)
    for img in carpeta:
        if img[-1] == 'g':
            foto = img.split(".")[0]
            image = cv2.imread(dir_in+"/"+img)
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            auto = auto_canny(gray)
            lados = cv2.dilate(auto, None,iterations=1)
            max_contorno= maxContorno(lados)
            x,y,w,h = cv2.boundingRect(max_contorno[0])
            rec= image[y:y+h , x:x+w]
            cv2.imwrite(dir_in+"/"+img, rec)
            


if __name__ == '__main__':
    aumentarData(sys.ar, afines, 0, 3)
    if sys.argv[2] == 1
        aumentarData(sys.argv[1],afines,0,sys.argv[3])
        obtenerRecuadro(sys.argv[1])
    else :
        aumentarData(sys.argv[1],conv,3,sys.argv[3],True)
        
    

