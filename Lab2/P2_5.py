import os

path1 = r"./attackresult/target/"
path2 = r"./attackresult/no_attack/"
path3 = r"./attackresult/pgd_normalize/"


def P2_5():
    scores = []
    Image = sorted(os.listdir(path1))
    Image_no_attack = os.listdir(path2)
    Image_pgd_normalize1 = os.listdir(os.path.join(path3, "eps0.0300"))
    Image_pgd_normalize2 = os.listdir(os.path.join(path3, "eps0.0700"))
    Image_pgd_normalize3 = os.listdir(os.path.join(path3, "eps0.0900"))
    correct_num_0, correct_num_1, correct_num_2, correct_num_3 = 0, 0, 0, 0

    for i, file in enumerate(Image):
        with open(os.path.join(path1, file)) as fp:
            line = fp.readline()
            line = int(line.split()[1])
            Image[i] = line

    for i, file in enumerate(Image_no_attack):
        with open(os.path.join(path2, file)) as fp:
            line = fp.readline()
            line = int(line)
            Image_no_attack[i] = line
    # print(Image_no_attack)

    for i, file in enumerate(Image_pgd_normalize1):
        with open(os.path.join(path3, "eps0.0300", file)) as fp:
            line = fp.readline()
            line = int(line)
            Image_pgd_normalize1[i] = line
    # print(Image_pgd_normalize1)

    for i, file in enumerate(Image_pgd_normalize2):
        with open(os.path.join(path3, "eps0.0700", file)) as fp:
            line = fp.readline()
            line = int(line)
            Image_pgd_normalize2[i] = line

    for i, file in enumerate(Image_pgd_normalize3):
        with open(os.path.join(path3, "eps0.0900", file)) as fp:
            line = fp.readline()
            line = int(line)
            Image_pgd_normalize3[i] = line

    for i, file in enumerate(Image):
        # print(file, Image_no_attack[i], Image_pgd_normalize1[i], Image_pgd_normalize2[i])
        if file == Image_no_attack[i]:
            correct_num_0 += 1
        if file == Image_no_attack[i] and file != Image_pgd_normalize1[i]:
            correct_num_1 += 1
        if file == Image_no_attack[i] and file != Image_pgd_normalize2[i]:
            correct_num_2 += 1
        if file == Image_no_attack[i] and file != Image_pgd_normalize3[i]:
            correct_num_3 += 1
    # print(correct_num_0, correct_num_1, correct_num_2)
    scores.extend([correct_num_0 / 1000, correct_num_1 / correct_num_0, correct_num_2 / correct_num_0,
                   correct_num_3 / correct_num_0])
    for i in range(4):
        scores[i] = round(scores[i], 3)
    return scores


if __name__ == "__main__":
    tmpList = P2_5()
    print(tmpList)
    

    
    
    
    

