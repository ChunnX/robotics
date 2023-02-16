import numpy as np

def read_input():
    while True:
        try:
            e1 = float(input("e1: "))
        except Exception:
            print("Invalid input")
        else:
            break
    
    while True:
        try:
            e2 = float(input("e2: "))
        except Exception:
            print("Invalid input")
        else:
            break
    
    while True:
        try:
            delta_e = float(input("delta e: "))
        except Exception:
            print("Invalid input")
        else:
            break

    while True:
        try:
            l = float(input("l: "))
        except Exception:
            print("Invalid input")
        else:
            break
    
    return e1, e2, delta_e, l



if __name__ == "__main__":
    e1 = []
    e2 = []
    delta_e = []
    target = []

    while True:
        try:
            e_1, e_2, delta_e_, l = read_input()
            e1.append(e_1)
            e2.append(e_2)
            delta_e.append(delta_e_)
            target.append(l)
        except KeyboardInterrupt:
            e1 = np.array(e1)
            e2 = np.array(e2)
            delta_e = np.array(delta_e)
            target = np.array(target)
            break

    lr = 0.00000015
    epochs = 5000
    r = 0.03333
    D = 0.05
    for epoch in range(epochs):
        theta = r*delta_e/10
        theta = theta - 2*np.pi * np.floor(theta/(np.pi*2))
        predictions = np.sqrt(e1**2 + e2**2 + 2*e1*e2*np.cos(theta)) * D
        predictions = np.where(theta > np.pi, predictions, -predictions)

        delta_l = 2 / len(target) * (predictions - target)
        delta_l = delta_l.reshape(1, -1)

        dl_dD = predictions / D
        dl_dr = e1 * e2 * np.abs(np.sin(theta)) * delta_e / np.sqrt(e1**2 + e2**2 + 2*e1*e2*np.cos(theta)) * D / 10
        dl_dD = dl_dD.reshape(-1, 1)
        dl_dr = dl_dr.reshape(-1, 1)

        dL_dD = float(delta_l @ dl_dD)
        dL_dr = float(delta_l @ dl_dr)

        r -= dL_dr * lr
        D -= dL_dD * lr

        if (epoch + 1) % 100 == 0:
            print("loss:", np.sqrt(np.mean((target-predictions)**2)))
            if dL_dr * lr < 1e-8 and dL_dD * lr < 1e-10:
                print("early stop")
                break

    print("D:", round(D, 8))
    print("W:", round(D / r * 10, 4))



