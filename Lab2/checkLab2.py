import os
import copy

if os.path.exists("P2_1.py"):
    from P2_1 import *
if os.path.exists("P2_2.py"):
    from P2_2 import *
if os.path.exists("P2_3.py"):
    from P2_3 import *    
if os.path.exists("P2_4.py"):
    from P2_4 import *    
if os.path.exists("P2_5.py"):
    from P2_5 import *        
        
def getColorStr2Prt(content, back_color='black', front_color='red'):
    colorList = ['black', 'red','green','yellow','blue',
        'purple','cyan','white']
    bstr = '4'+str(colorList.index(back_color))
    fstr = '3'+str(colorList.index(front_color))
    
    try:
        from colorama import init,Fore,Back,Style
        init(autoreset=True)    
        tmpstr = '\033[1;%s;%sm''%s' % (fstr, bstr, content)
    except:
        tmpstr = content
    return tmpstr
    
def check(func):
    func_name = func.__name__    
    if func_name == "P2_1":
        xys = [(100,'A'),(91,'A'),(90,'A'),(85,'B'),(80,'B'),(79,'C'),(70,'C'),
            (69,'D'),(60,'D'),(50,'E'),(120,'X'),(-1,'X')]
    
    if func_name == "P2_2":
        xys = [(0,1),(1,1),(2,2)]
    
    if func_name == "P2_3":
        xys = [(None, (['xiaoming', 'xiaohong', 'xiaojun'],[89.9, 85.9, 80.6]))]
        
    if func_name == "P2_4":    
        xys = [(None, [569322701, 736976144])]
    
    if func_name == "P2_5":
        xys = [(None, [0.737, 0.731, 0.948, 0.962])]
    
    failed = False
    for x,y in xys:
        if x is not None:
            y2 = func(x)
        else:
            y2 = func()

        ret = (y2 == y)
        if ret == False:            
            if x is not None:
                print("%s failed with input: %s" % (func_name, str(x)))
            else:
                print("%s is Failed" % (func_name))            
            print("%s %s\n" % (getColorStr2Prt("Expected output:",front_color='red'), str(y)))
            failed = True
            break
            
    if failed == False:
        print("%s is %s\n" % (func_name, getColorStr2Prt("OK",front_color='green')))

if __name__ == "__main__":
    if os.path.exists("P2_1.py"):
        check(P2_1)
    if os.path.exists("P2_2.py"):
        check(P2_2)
    if os.path.exists("P2_3.py"):
        check(P2_3)
    if os.path.exists("P2_4.py"):
        check(P2_4)
    if os.path.exists("P2_5.py"):
        check(P2_5)
        

