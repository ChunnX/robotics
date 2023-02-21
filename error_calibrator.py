import numpy as np
import torch



if __name__ == "__main__":

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

    lr = 0.00001
    epochs = 1000


    D = 0.0484351167752
    W = 14.4486
    r = 1.0035822

    kf = torch.tensor([0.01], dtype=torch.double, requires_grad=True)
    kg = torch.tensor([0.01], dtype=torch.double, requires_grad=True)

    optimiser = torch.optim.Adam((kg, kf), lr=lr)

    delta_e1 = r*e1r - e1l
    sum_e1 = e1l + r*e1r

    delta_e2 = r*e2r - e2l
    sum_e2 = e2r*r + e2l 

    delta_et = etr*r - etl

    sine1 = torch.sin(delta_e1*D / (2*W))
    l1 = sine1 * sum_e1 / delta_e1 * W

    sine2 = torch.sin(delta_e2*D / (2*W))
    l2 = sine2 * sum_e1 / delta_e2 * W
    
    turned_angle = (delta_et + delta_e1) * D / W
    cosine_term = torch.cos(turned_angle)
    
    angle = turned_angle.detach()
    angle = angle - torch.floor(0.5*angle/torch.pi)*torch.pi*2

    distance = (l1 + l2) / 2
    L = target - 2*torch.sin((angle-torch.pi)/2)*distance

    for epoch in range(epochs):
        optimiser.zero_grad()
        
        var = distance.pow(2) * kg.pow(2) * turned_angle + 2 / 3 * distance.pow(3) * kf.pow(2)
        loss = (L.pow(2) / var + var.log()).mean()
        loss.backward() 

        # print(kg.grad.item())

        optimiser.step()

print("loss:", loss.item())
print("kg:", kg.pow(2).item())
print("kf:", kf.pow(2).item())




