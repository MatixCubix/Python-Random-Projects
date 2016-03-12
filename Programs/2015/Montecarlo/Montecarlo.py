import random
import math
from timeit import default_timer as timer

def in_Circle(x,y,r):
    c = x**2 + y**2
    if c <= r**2:
        return True
    return False

def pi(r,iteraciones):
    count_in = 0
    for i in range(iteraciones):
        x = random.random()
        y = random.random()
        x = r*x
        y = r*y
        if in_Circle(x,y,r) == True:
            count_in +=1
        if i == (iteraciones):
            print("*100% Completo.")
        elif i == (iteraciones*(9/10)):
            print("*90% Completo.")
        elif i == (iteraciones*(8/10)):
            print("*80% Completo.")
        elif i == (iteraciones*(7/10)):
            print("*70% Completo.")
        elif i == (iteraciones*(6/10)):
            print("*60% Completo.")
        elif i == (iteraciones*(5/10)):
            print("*50% Completo.")
        elif i == (iteraciones*(4/10)):
            print("*40% Completo.")
        elif i == (iteraciones*(3/10)):
            print("*30% Completo.")
        elif i == (iteraciones*(2/10)):
            print("*20% Completo.")
        elif i == (iteraciones*(1/10)):
            print("*10% Completo.")
            
    pi = (4*count_in)/iteraciones
    return pi

def pi_int(r,dx):
    u = 0
    x = 0
    while x <= r:
        u += math.sqrt(r**2 - (x**2))*dx
        x += dx
    pi = (u*4)/(r**2)    
    return pi

def pi_ramj(i):
    u = 0
    for k in range(i):
        u += float((math.factorial((4*k)) * (1103 + 26390*k))/(((math.factorial(k))**4)*(396**(4*k))))
    pi = u *(2*math.sqrt(2))/9801
    pi = pi ** (-1)
    return pi
        
           
while True:
    Q = input("Montecarlo(1), Integral(2), Ramj(3): ")
    print(" ")
    if Q == "1":
        
        i = int(input("Iteraciones: "))
        r = float(input("Radio: "))
        start = timer()
        num = pi(r,i)
        end = timer()
        print(" ")
        print("Pi =",num)
        print(" ")
        print("Tiempo =",(end-start))
        print(" ")
        
    elif Q == "2":
        r = float(input("Radio: "))
        dx = float(input("dx: "))
        start = timer()
        g = pi_int(r,dx)
        end = timer()
        print(" ")
        print("pi =",g)
        print(" ")
        print("Tiempo =",(end-start))
        print(" ")
    elif Q == "3":
        i = int(input("Iteraciones: "))
        start = timer()
        num = pi_ramj(i)
        end = timer()
        print(" ")
        print("pi =",num)
        end = timer()
        print(" ")
        print("Tiempo =",(end-start))
        print(" ")
        
    Q = input("Continuar? ").upper()
    if Q == "NO":
        break
    
    print("-------------------------------------------")
    print(" ")

