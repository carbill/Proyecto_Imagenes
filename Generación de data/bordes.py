import numpy as np
import cv2
import os
import sys
import matplotlib.pyplot as plt

MASK_COLOR = (0,0,0) # In BGR format 


def auto_canny(image, sigma=0.2):
    # compute the median of the single channel pixel intensities
    v = np.median(image)

    # apply automatic Canny edge detection using the computed median
    lower = int(max(0, (1.0 - sigma) * v))
    upper = int(min(255, (1.0 + sigma) * v))
    edged = cv2.Canny(image, lower, upper)

    # return the edged image
    return edged

def maxContorno(lados):
    contornos_info = [] 
    contornos, hierarchy = cv2.findContours(lados, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE) 
    for c in contornos: 
        contornos_info.append((
         c, 
         cv2.isContourConvex(c), 
         cv2.contourArea(c), 
        )) 
    contornos_info = sorted(contornos_info, key=lambda c: c[2], reverse=True) 
    return contornos_info[0] 

def mascarasObjetos(directorio,clase, c, out):
    contador = 0
    carpeta = os.listdir(directorio+"/"+clase)
    for img in carpeta:
        image = cv2.imread(directorio+"/"+clase+"/"+img)
        print("\t" + img)
        height, width,  _ = image.shape
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blurred_x = cv2.GaussianBlur(gray, (3, 3),0)
        blurred3 = cv2.resize(gray,(int(width/2),int(height/2)))
        blurred2 = cv2.resize(blurred3,(int(width/4),int(height/4)))
        blurred = cv2.resize(blurred2,(int(width/6),int(height/6)))

        # Deteccion de bordes con canny
        auto = auto_canny(blurred)
        edges = cv2.dilate(auto, None,iterations=3)
        edges  = cv2.resize(edges,(int(width/8),int(height/8)))

        auto2 = auto_canny(blurred2)
        edges2 = cv2.dilate(auto2, None,iterations=3)
        edges2  = cv2.resize(edges2,(int(width/8),int(height/8)))

        auto3 = auto_canny(blurred3)
        edges3 = cv2.dilate(auto2, None,iterations=3)
        edges3  = cv2.resize(edges3,(int(width/8),int(height/8)))

        # Consolidación de bordes
        #cv2.imwrite(foto+"-edges.jpg",np.hstack([edges,edges2,edges3]))
        edges = edges + edges2 + edges3


        edges = cv2.resize(edges,(int(width/8),int(height/8)))
        image  = cv2.resize(image,(int(width/8),int(height/8)))


        #Busqueda del contorno mas grande
        max_contour = maxContorno(edges) 


        # Creacion de la máscara
        mask = np.zeros(edges.shape) 
        cv2.fillConvexPoly(mask, max_contour[0], (255)) 


        #--Darle suavidad a la mascara -------------------------------------------------------- 
        #mask = cv2.dilate(mask, None, iterations=1) 
        #mask = cv2.erode(mask, None, iterations=3) 
        #mask = cv2.GaussianBlur(mask, (7, 7), 0) 
        mask_stack = np.dstack([mask]*3) # Create 3-channel alpha mask 

        #-- Obtencion de objeto segmentado -------------------------------------- 
        mask_stack = mask_stack.astype('float32')/255.0   # Use float matrices, 
        image   = image.astype('float32')/255.0     # for easy blending 
        masked = (mask_stack * image) + ((1-mask_stack) * MASK_COLOR) # Blend 
        masked = (masked * 255).astype('uint8')      # Convert back to 8-bit

		# Guardar elementos segmentado
        cv2.imwrite(out+ "/"+c+"_"+str(contador)+".jpg", masked)   # Save 
        contador += 1





if __name__ == '__main__':
    count = 0
    carpeta = os.listdir(sys.argv[1])
	archivo = open("obj.names",'a')
    for clase in carpeta:
        mascarasObjetos(sys.argv[1], clase, str(count),sys.argv[2])
		archivo.write(clase+"\n")
        count += 1
	archivo.close()

