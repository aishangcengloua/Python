def P2_1(score) :
    if 100 >= score >= 90 :
        return 'A'
    elif 89 >= score >= 80 :
        return 'B'
    elif 79 >= score >= 70 :
        return 'C'
    elif 69 >= score >= 60 :
        return 'D'
    elif 59 >= score >= 0 :
        return 'E'
    else :
        return 'X'
if __name__ == "__main__":
    print(P2_1(30))

