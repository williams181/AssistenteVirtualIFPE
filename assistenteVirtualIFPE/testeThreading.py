import threading
import time

from matplotlib.pyplot import thetagrids 

def tarefa1():
    x = 0
    while x < 10:
        time.sleep(2)
        print("tarefa 1")
        x += 1 

def tarefa2():
    y = 0
    while y < 10:
        time.sleep(2)
        print("tarefa 2")
        y += 1

threading.Thread(target=tarefa1).start()
threading.Thread(target=tarefa2).start()