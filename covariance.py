import numpy as np
import re



def covariance():

    coor_array = np.zeros((10, 2), dtype=np.float32)
    valid_input = 0
    dictionary = {0: 'st', 1:"nd", 2:"rd", 3:"th"}
#     input_pattern = re.compile(r"^[+-]?\d+\.?\d*,[+-]?\d+\.?\d*$")
    while valid_input < 10:
        while True:
            
            coor = input(f"Please enter the {valid_input+1}{dictionary[valid_input if valid_input < 3 else 3]} coordinate in the form x, y:").replace(" ", "")
#             if input_pattern.fullmatch(coor):
#                 x, y = coor.split(",")
#                 coor_array[valid_input, 0] = float(x)
#                 coor_array[valid_input, 1] = float(y)
#                 break
#             else:
#                 print("Invalid input, please try again")
                
            try:
                x, y = coor.split(",")
                x = float(x)
                y = float(y)
            except Exception:
                print("Invalid input, please try again")
            else:
                coor_array[valid_input, 0] = x
                coor_array[valid_input, 1] = y
                break
        valid_input += 1

    print(f"The 10 coordinates you entered are: {coor_array}")

    cov = np.cov(coor_array.T, ddof=0)
    mean = np.mean(coor_array, axis=0)

    print(f"The mean vector is {mean}")
    print(f"Covariance Matrix: {cov}")

    return cov


if __name__ == "__main__":
    covariance()
