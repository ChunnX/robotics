import numpy as np
import torch



if __name__ == "__main__":
    # e1 = []
    # e2 = []
    # delta_e = []
    # target = []


    # e1 = np.array([837, 837, 837, 837, 837, 837, 837, 836.5, 837, 837.5,
    # 836, 835, 836, 836, 836, 836.5, 836.5, 835, 836, 836])
    # e2 = np.array([837, 837, 836.5, 836.5, 837, 836.5, 837, 837, 836.5, 836.5,
    # 836.5, 836, 836, 835.5, 835.5, 836, 836, 835.5, 836, 835.5])
    # delta_e = np.array([911, 914, 886, 884, 967, 965, 1020, 1023, 1076, 1074, 
    # 2812, 2813, 2814, 2814, 2812, 2813, 2811, 2808, 2812, 2813])
    # target = np.array([-3.4, -3.15, -6.7, -6.05, 4.55, 4.1, 11.5, 12.0, 19.4, 18.2, 
    # -2.1, -6.3, -4.85, -5.5, -1.8, -2.5, -0.9, -3.45, -2.8, -4.25])

    e1l = torch.tensor([837, 837, 1046, 1046, 1045, 1046, 1255, 1254, 1255, 1255, 
                        1673, 1674, 1674, 1673, 1360, 1360, 1464, 1464, 1046, 1046], dtype=torch.float32)
    e1r = torch.tensor([837, 838, 1046, 1046, 1046, 1046, 1255, 1255, 1256, 1256,
                        1673, 1673, 1674, 1674, 1361, 1361, 1465, 1464, 1046, 1046], dtype=torch.float32)
    etl = torch.tensor([-456, -456, -456, -456, -509, -510, -483, -482, -470, -469,
                        -456, -456, -470, -470, -442, -442, -1406, -1406, -1352, -1353], dtype=torch.float32)
    etr = torch.tensor([457, 457, 457, 458, 511, 511, 485, 484, 471, 470, 
                        456, 457, 471, 471, 443, 443, 1407, 1407, 1352, 1353], dtype=torch.float32)
    e2l = torch.tensor([836, 836, 1046, 1046, 1046, 1046, 1254, 1255, 1255, 1255,
                        1673, 1673, 1673, 1673, 1360, 1360, 1463, 1464, 1046, 1046], dtype=torch.float32)
    e2r = torch.tensor([837, 837, 1045, 1046, 1046, 1046, 1255, 1255, 1255, 1256,
                        1673, 1673, 1673, 1673, 1360, 1360, 1463, 1463, 1045, 1046], dtype=torch.float32)

    target = torch.tensor([-3.6, -3.9, -3.8, -5.4, 15.25, 13.2, 6.3, 9.1, 0, 2.8,
                            -5.3, -5.75, 3.2, 4.65, -8.5, -7.55, 3.2, 3.6, -17.1, -16.2], dtype=torch.float32)

    lr = 0.0000005
    epochs = 10000


    D = torch.tensor([0.48], dtype=torch.double, requires_grad=True)
    W = torch.tensor([14.45], dtype=torch.double, requires_grad=True)
    r = torch.tensor([1.05], dtype=torch.double, requires_grad=True)

    optimiser = torch.optim.SGD((D, W, r), lr=lr)
    for epoch in range(epochs):
        optimiser.zero_grad()
        delta_e1 = r*e1r - e1l
        sum_e1 = e1l + r*e1r

        delta_e2 = r*e2r - e2l
        sum_e2 = e2r*r + e2l 

        delta_et = etr*r - etl

        sine1 = torch.sin(delta_e1*(D/10) / (2*W))
        l1 = sine1 * sum_e1 / delta_e1 * W

        sine2 = torch.sin(delta_e2*(D/10) / (2*W))
        l2 = sine2 * sum_e1 / delta_e2 * W
        
        turned_angle = (delta_et + delta_e1) * (D/10) / W
        cosine_term = torch.cos(turned_angle)
        
        angle = turned_angle.detach()
        angle = angle - torch.floor(0.5*angle/torch.pi)*torch.pi*2
        L = torch.sqrt(l1.pow(2) + l2.pow(2) + 2*l1*l2*cosine_term)
        out = torch.where(angle > torch.pi, L, -L)

        loss = (out - target).pow(2).mean()
        loss.backward() 

        # print((lr * D.grad).item())
        # print((lr * W.grad).item())
        # print((lr * r.grad).item())
        optimiser.step()

print("loss:", loss.item())

print("D:", D.item()/10)
print("W:", W.item())
print("r:", r.item())


