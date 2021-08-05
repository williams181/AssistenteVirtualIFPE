import os
import random
import PIL
from PIL import Image
import cv2

folder=r"C:\\Users\\casa\\Desktop\\assistenteVirtualIFPE\\assistenteVirtualIFPEAvatarModelo"

# img = cv2.imread('C:\\Users\\casa\\Desktop\\assistenteVirtualIFPE\\assistenteVirtualIFPEAvatarModelo')

a=random.choice(os.listdir(folder))

print(a)

# os.open(a, os.O_RDWR)

file = folder+'\\'+a

# cv2.imshow("avatar", file)

# cv2.waitKey(0)

Image.open(file).show()