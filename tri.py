from sense_hat import SenseHat

sense = SenseHat()
sense.clear()

i = 7
while(i >= 0):
    j = 0
    while(j <= i ):
        sense.set_pixel(j, i, 255, 0, 0)
        j = j + 1
    i = i - 1