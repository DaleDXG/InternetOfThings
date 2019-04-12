from sense_hat import SenseHat
import random
import time

sense = SenseHat()


cl1 = [255, 255, 255]
cl2 = [255, 0, 0]
pixel_list = [cl1, cl1, cl1, cl1, cl1, cl1, cl1, cl1,
              cl1, cl1, cl1, cl1, cl1, cl2, cl1, cl1,
              cl1, cl2, cl2, cl2, cl2, cl2, cl2, cl1,
              cl1, cl2, cl1, cl1, cl1, cl1, cl1, cl2,
              cl1, cl2, cl2, cl2, cl2, cl2, cl2, cl1,
              cl1, cl1, cl1, cl1, cl1, cl2, cl1, cl1,
              cl1, cl1, cl1, cl1, cl1, cl1, cl1, cl1,
              cl1, cl1, cl1, cl1, cl1, cl1, cl1, cl1]
pixel_list2 = []
iRecurrent = 0

while True:
    sense.clear()
    pixel_list2 = []

    i = 0
    
    while i < 8:
        j = 0
        while j < 8:
            pixel_list2.append(pixel_list[i * 8 + ((j - iRecurrent) % 8)])
            j = j + 1
        i = i + 1
    sense.set_pixels(pixel_list2)
    iRecurrent = (iRecurrent + 1) % 8
    time.sleep(1)
