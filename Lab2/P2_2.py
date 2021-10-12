def P2_2(n) :
    y = 1
    if n == 0 or n == 1 :
        return 1
    if n == 4 :
        return 24
    for i in range(1, n + 1) :
        y *= i
    return y

if __name__ == "__main__":
    print(P2_2(3))
    
    