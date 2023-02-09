import numpy as np

def calibrate(d11, d12, theta1, d21, d22, theta2, D, W, l1, l2):
    r = 1
    theta1 /= 57.29578
    theta2 /= 57.29578
    while True:
        # print((l1/l2)**2)
        # print(r, theta2)
        # print((np.cos(r*theta2)))
        # print(- d11**2 - d12**2)
        print(r, ((l1/l2)**2 * (d21**2 + d22**2 + 2*d21*d22*np.cos(r*theta2)) - d11**2 - d12**2) / (2*d11*d12))
        a = (l1/l2)**2 * (d21**2 + d22**2 + 2*d21*d22*np.cos(r*theta2)) - d11**2 - d12**2
        if np.isnan(a):
            raise Exception
        new_r = np.arccos(((l1/l2)**2 * (d21**2 + d22**2 + 2*d21*d22*np.cos(r*theta2)) - d11**2 - d12**2) / (2*d11*d12)) / theta1
        if abs(new_r - r) < 1e-8:
            r = (new_r + r) / 2
            break
        else:
            r = new_r
    D_prime = l1 / np.sqrt(d11**2 + d12**2 + 2*np.cos(r*theta1)*d11*d12)
    W_prime = W * D_prime / (D * r)
    return D_prime, W_prime




while True:
    try:
        d11 = float(input("d11: "))
    except:
        print("Invalid input")
    else:
        break

while True:
    try:
        d12 = float(input("d12: "))
    except:
        print("Invalid input")
    else:
        break

while True:
    try:
        theta1 = float(input("theta1: "))
    except:
        print("Invalid input")
    else:
        break

while True:
    try:
        l1 = float(input("l1: "))
    except:
        print("Invalid input")
    else:
        break

while True:
    try:
        d21 = float(input("d21: "))
    except:
        print("Invalid input")
    else:
        break

while True:
    try:
        d22 = float(input("d22: "))
    except:
        print("Invalid input")
    else:
        break


while True:
    try:
        theta2 = float(input("theta2: "))
    except:
        print("Invalid input")
    else:
        break


while True:
    try:
        l2 = float(input("l2: "))
    except:
        print("Invalid input")
    else:
        break

while True:
    try:
        D = float(input("D: "))
    except:
        print("Invalid input")
    else:
        break

while True:
    try:
        W = float(input("W: "))
    except:
        print("Invalid input")
    else:
        break

D_prime, W_prime = calibrate(d11, d12, theta1, d21, d22, theta2, D, W, l1, l2)
print("D':", round(D_prime, 8))
print("W':", round(W_prime, 4))

