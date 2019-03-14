import cv2
import numpy as np
import sys

if __name__ == '__main__':
    textura = cv2.imread(sys.argv[1])
    textura = cv2.resize(textura,(3000,1900))
    mask = np.zeros([3000, 4000, 3])
    blanco = np.ones([1900, 3000,3])
    mask[600:2500,500:3500]= blanco*textura
    cv2.imwrite("ejemplo.jpg",mask)

    rows,cols, _ = mask.shape

    pts1 = np.float32([[600,500],[600,3500],[2500,500]])
    pts2 = np.float32([[1100,2000],[100,3000],[3000,2000]])
    pts3 = np.float32([[50,2000],[1100,3000],[2200, 2000]])
    pts4 = np.float32([[200,2000],[1500,3000],[2000,1500]])

    M = cv2.getAffineTransform(pts1,pts2)
    dst = cv2.warpAffine(mask,M,(cols,rows))
    cv2.imwrite("contexto1.jpg",dst)


    M2 = cv2.getAffineTransform(pts1,pts3)
    dst = cv2.warpAffine(mask,M2,(cols,rows))
    cv2.imwrite("contexto2.jpg",dst)

    M3 = cv2.getAffineTransform(pts1,pts4)
    dst = cv2.warpAffine(mask,M3,(cols,rows))
    cv2.imwrite("contexto3.jpg",dst)

    pts1 = np.float32([[600,500],[600,3500],[2500,500],[3000,3500]])
    pts2 = np.float32([[1000,1500],[-8000,18000],[2000,1500],[8000,18000]])
    pts3 = np.float32([[2000,1000],[-500,3000],[3400, 1500],[1200,3500]])

    M = cv2.getPerspectiveTransform(pts1,pts2)
    dst = cv2.warpPerspective(mask,M,(cols,rows))
    cv2.imwrite("contexto4.jpg",dst)

    M = cv2.getPerspectiveTransform(pts1,pts3)
    dst = cv2.warpPerspective(mask,M,(cols,rows))
    cv2.imwrite("contexto5.jpg",dst)

