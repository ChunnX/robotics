import numpy as np
import torch



if __name__ == "__main__":

    # e1l = torch.tensor([837, 837, 1046, 1046, 1045, 1046, 1255, 1254, 1255, 1255, 
    #                     1673, 1674, 1674, 1673, 1360, 1360, 1464, 1464, 1046, 1046], dtype=torch.float32)
    # e1r = torch.tensor([837, 838, 1046, 1046, 1046, 1046, 1255, 1255, 1256, 1256,
    #                     1673, 1673, 1674, 1674, 1361, 1361, 1465, 1464, 1046, 1046], dtype=torch.float32)
    # etl = torch.tensor([-456, -456, -456, -456, -509, -510, -483, -482, -470, -469,
    #                     -456, -456, -470, -470, -442, -442, -1406, -1406, -1352, -1353], dtype=torch.float32)
    # etr = torch.tensor([457, 457, 457, 458, 511, 511, 485, 484, 471, 470, 
    #                     456, 457, 471, 471, 443, 443, 1407, 1407, 1352, 1353], dtype=torch.float32)
    # e2l = torch.tensor([836, 836, 1046, 1046, 1046, 1046, 1254, 1255, 1255, 1255,
    #                     1673, 1673, 1673, 1673, 1360, 1360, 1463, 1464, 1046, 1046], dtype=torch.float32)
    # e2r = torch.tensor([837, 837, 1045, 1046, 1046, 1046, 1255, 1255, 1255, 1256,
    #                     1673, 1673, 1673, 1673, 1360, 1360, 1463, 1463, 1045, 1046], dtype=torch.float32)

    # target = torch.tensor([-3.6, -3.9, -3.8, -5.4, 15.25, 13.2, 6.3, 9.1, 0, 2.8,
    #                         -5.3, -5.75, 3.2, 4.65, -8.5, -7.55, 3.2, 3.6, -17.1, -16.2], dtype=torch.float32)


    e1l = torch.tensor([462, 768, 462, 768, 462, 
                        767, 460, 768, 462, 767, 
                        461, 538, 691, 614, 767, 
                        614, 768, 538, 462, 692, 
                        462, 767, 461, 768, 462, 
                        767, 462, 767, 462, 766, 
                        324, 324, 324, 404, 404, 
                        403, 402, 436, 485, 485], dtype=torch.float32)
    e1r = torch.tensor([474, 790, 475, 790, 475, 
                        789, 474, 790, 474, 788, 
                        474, 552, 710, 631, 790, 
                        632, 789, 553, 474, 710, 
                        474, 790, 474, 790, 475, 
                        789, 474, 788, 474, 789, 
                        322, 322, 322, 402, 402, 
                        401, 402, 434, 481, 482], dtype=torch.float32)
    etl = torch.tensor([-318, -317, -326, -327, -336, 
                        -336, -345, -346, -356, -355, 
                        -326, -327, -336, -355, -365, 
                        -326, -317, -346, -355, -336, 
                        -326, -325, -336, -336, -346, 
                        -344, -355, -355, -364, -364, 
                        -1074, -1084, -1094, -1095, -1084, 
                        -1115, -1053, -1064, -1034, -1054], dtype=torch.float32)
    etr = torch.tensor([328, 328, 337, 338, 348, 
                        348, 357, 358, 368, 368, 
                        338, 338, 348, 368, 378, 
                        338, 328, 358, 368, 348, 
                        338, 337, 348, 348, 358, 
                        358, 368, 368, 377, 378, 
                        1066, 1076, 1085, 1085, 1075, 
                        1105, 1044, 1056, 1024, 1046], dtype=torch.float32)
    e2l = torch.tensor([461, 767, 461, 767, 462, 
                        766, 461, 767, 461, 767, 
                        461, 538, 690, 614, 767, 
                        613, 767, 539, 461, 691, 
                        461, 767, 460, 767, 460, 
                        766, 461, 767, 461, 767, 
                        324, 322, 324, 403, 404, 
                        404, 403, 436, 484, 484], dtype=torch.float32)
    e2r = torch.tensor([475, 790, 473, 789, 474, 
                        789, 474, 789, 474, 789, 
                        474, 552, 710, 631, 790, 
                        631, 789, 553, 474, 710, 
                        474, 789, 474, 788, 474, 
                        789, 474, 789, 475, 789, 
                        322, 321, 321, 401, 401, 
                        402, 400, 434, 482, 480], dtype=torch.float32)

    target = torch.tensor([-8.75, -13.05, -6, -8.9, -4.15, 
                           -6.05, -1.5, -0.7, 1.4, 0.5, 
                           -6.5, -6.7, -4.3, 2, 10.5, 
                           -2.1, -11.2, -1.5, 1.6, -2.4, 
                           -5.8, -5.35, -4, -1.85, -1.25, 
                           0.4, 1.9, 6, 3.3, 8.85, 
                           6.5, 8, 9.3, 12.6, 10.5, 
                           16.5, 3.9, 5, -4.9, 1.7], dtype=torch.float32)
    

    lr = 0.00001
    epochs = 10000


    D = 0.06569817277947267
    W = 14.026094445799139
    r = 0.9509515851484188

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

    rotated_angle = delta_et * D / W
    
    angle = turned_angle.detach()
    angle = angle - torch.floor(0.5*angle/torch.pi)*torch.pi*2

    distance = (l1 + l2) / 2
    L = target - 2*torch.sin((angle-torch.pi)/2)*distance

    for epoch in range(epochs):
        optimiser.zero_grad()
        
        var = distance.pow(2) * kg.pow(2) * rotated_angle + 2 / 3 * distance.pow(3) * kf.pow(2)
        loss = (L.pow(2) / var + var.log()).mean()
        loss.backward()

        # print(kg.grad.item())

        optimiser.step()

print("loss:", loss.item())
print("kg:", kg.pow(2).item())
print("kf:", kf.pow(2).item())




