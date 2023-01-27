import numpy as np


def covariance():

    coor_list = []
    for i in range(10):

        coor = input(f"Please enter {i+1} coordinate in the form x, y:")
        coor_list.append([float(coor.split(",")[0]), float(coor.split(",")[-1])])

    print(f"The 10 coordinates you entered are: {coor_list}")

    coor_array = np.array(coor_list).T
    cov = np.cov(coor_array, ddof=0)

    print(f"Covariance Matrix: {cov}")

    return cov


if __name__ == "__main__":
    covariance()