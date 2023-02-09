import numpy as np

def calibrate(d11, d12, theta1, d21, d22, theta2, D, W, l1, l2):
    r = 1
    theta1 /= 57.29578
    theta2 /= 57.29578

    last_diff = 0
    for i in np.linspace(0, 2, 21):
        new_diff = np.cos(theta1*i) * 2*d11*d12 - (l1/l2)**2 * (d21**2 + d22**2 + 2*d21*d22*np.cos(i*theta2)) + d11**2 + d12**2
        if new_diff == 0:
            r_l = r_h = i
            break
        elif new_diff * last_diff < 0:
            r_l = i - 0.1
            r_h = i
            break
        else:
            last_diff = new_diff

    while r_h - r_l > 1e-10:
        d_h = np.cos(theta1*r_h) * 2*d11*d12 - (l1/l2)**2 * (d21**2 + d22**2 + 2*d21*d22*np.cos(r_h*theta2)) + d11**2 + d12**2
        new_r = (r_l + r_h) / 2

        d_new = np.cos(theta1*new_r) * 2*d11*d12 - (l1/l2)**2 * (d21**2 + d22**2 + 2*d21*d22*np.cos(new_r*theta2)) + d11**2 + d12**2
        if d_new == 0:
            r_h = r_l = new_r
        elif d_new * d_h < 0:
            r_l = new_r
        else:
            r_h = new_r

    r = (r_h + r_l) / 2
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

