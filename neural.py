import numpy as np
from random import randint,uniform
from Settings import ALPHA,ACTIVE,NEURAL_IN_CALCULATE

def fitnes_buble_sort(a):
    s = len(a)
    while s >= 0:
        s = s - 1
        for i in range(0, s):
            if a[i].fit < a[i + 1].fit:
                a[i], a[i + 1] = a[i + 1], a[i]

    return a

def mutation(i):
    return uniform(0,1)*i

def new_generation(a):
    new_gener=fitnes_buble_sort(a)
    new_gener[4].w01=new_gener[0].w01*(uniform(0,1)*mutation(new_gener[4].num))
    new_gener[4].w02 = new_gener[1].w02*(uniform(0,1)*mutation(new_gener[4].num))
    for i in range(5,8):
        new_gener[i].w01=new_gener[randint(0,3)].w01*(uniform(0,1)*mutation(new_gener[i].num))
        new_gener[i].w02 = new_gener[randint(0, 3)].w02*(uniform(0,1)*mutation(new_gener[i].num))
    for i in range(9,len(new_gener)-1):
        k=new_gener[randint(0, 3)]
        new_gener[i].w01 = k.w01*(uniform(0,1)*mutation(new_gener[i].num))
        new_gener[i].w02 = k.w02*(uniform(0,1)*mutation(new_gener[i].num))
    return new_gener


inp=np.array([[100, 50]])
inp=inp/100
def invert(x):
    return (x>0)*x

def inn(x):
    return x**(x<1)

def invert_one(x):
    return x>0

def first_generation(d,h,sd):
    np.random.seed(randint(1,100))
    hidden_size=6
    weights_0_1=2*np.random.random((2,hidden_size))-1
    weights_1_2=2*np.random.random((hidden_size,1))-1
    return neural_network(d,h,weights_0_1,weights_1_2,sd)


def neural_network(d,h,w01,w12,sd):
    h=invert(h)
    inp = np.array([[d, h]])
    inp = inp / 100
    for itera in range(0):
        alpha=ALPHA#0.2,2
        for i in range(len(inp)):
            l0 = inp[i:i+1]
            l1=invert(np.dot(l0,w01))
            l2=np.dot(l1,w12)
            l2_d=(l2-sd/10)
            l1_d=l2_d.dot(w12.T)*invert_one(l1)
            w12-=alpha*l1.T.dot(l2_d)
            w01-=alpha*l0.T.dot(l1_d)
    return  w01,w12

def calcul(d,h,w01,w12,sd):
    inp = np.array([[d, h]])
    inp=inp/100
    l0 = inp
    if NEURAL_IN_CALCULATE:
        w01,w02=neural_network(d,h,w01,w12,sd)
    l1 = invert(np.dot(l0, w01))
    l2=np.dot(l1,w12)
    #0.5
    if l2[0][0]>ACTIVE:
        return True
    else:
        return False

