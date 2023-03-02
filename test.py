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

    e1l = torch.tensor([462, 768, 462, 768, 462, 767, 460, 768, 462, 767, 461, 538, 691, 614, 767, 614, 768, 538, 462, 692, 462, 767, 461, 768, 462, 767, 462, 767, 462, 766, 324, 324, 324, 404, 404, 403, 402, 436, 485, 485], dtype=torch.float32)
    e1r = torch.tensor([474, 790, 475, 790, 475, 789, 474, 790, 474, 788, 474, 552, 710, 631, 790, 632, 789, 553, 474, 710, 474, 790, 474, 790, 475, 789, 474, 788, 474, 789, 322, 322, 322, 402, 402, 401, 402, 434, 481, 482], dtype=torch.float32)
    etl = torch.tensor([-318, -317, -326, -327, -336, -336, -345, -346, -356, -355, -326, -327, -336, -355, -365, -326, -317, -346, -355, -336, -326, -325, -336, -336, -346, -344, -355, -355, -364, -364, -1074, -1084, -1094, -1095, -1084, -1115, -1053, -1064, -1034, -1054], dtype=torch.float32)
    etr = torch.tensor([328, 328, 337, 338, 348, 348, 357, 358, 368, 368, 338, 338, 348, 368, 378, 338, 328, 358, 368, 348, 338, 337, 348, 348, 358, 358, 368, 368, 377, 378, 1066, 1076, 1085, 1085, 1075, 1105, 1044, 1056, 1024, 1046], dtype=torch.float32)
    e2l = torch.tensor([461, 767, 461, 767, 462, 766, 461, 767, 461, 767, 461, 538, 690, 614, 767, 613, 767, 539, 461, 691, 461, 767, 460, 767, 460, 766, 461, 767, 461, 767, 324, 322, 324, 403, 404, 404, 403, 436, 484, 484], dtype=torch.float32)
    e2r = torch.tensor([475, 790, 473, 789, 474, 789, 474, 789, 474, 789, 474, 552, 710, 631, 790, 631, 789, 553, 474, 710, 474, 789, 474, 788, 474, 789, 474, 789, 475, 789, 322, 321, 321, 401, 401, 402, 400, 434, 482, 480], dtype=torch.float32)

    target = torch.tensor([-8.75, -13.05, -6, -8.9, -4.15, -6.05, -1.5, -0.7, 1.4, 0.5, -6.5, -6.7, -4.3, 2, 10.5, -2.1, -11.2, -1.5, 1.6, -2.4, -5.8, -5.35, -4, -1.85, -1.25, 0.4, 1.9, 6, 3.3, 8.85, 6.5, 8, 9.3, 12.6, 10.5, 16.5, 3.9, 5, -4.9, 1.7], dtype=torch.float32)

    lr = 0.0000005
    epochs = 10000


    D = torch.tensor([0.6528915], dtype=torch.double, requires_grad=True)
    W = torch.tensor([14.447332], dtype=torch.double, requires_grad=True)
    r = torch.tensor([0.9730196], dtype=torch.double, requires_grad=True) # 如果报错 改成小于1

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

