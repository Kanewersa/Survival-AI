import os
import pygame as pg

for i in os.listdir('.'):
    try:
        img = pg.image.load(i)
        pg.image.save(img, i)
    except:
        print("Failed to fix image " + i)

print('Success. All images were fixed!')
