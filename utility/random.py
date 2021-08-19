import math
import random
def shuffle_array(array):
    array2=[]
    while len(array2)<len(array):
        i=random.random()
        i=i*len(array)
        i=math.floor(i)
        i=array[i]
        if i in array2:
            pass
        else:
            array2.append(i)
    return array2

if __name__=='__main__':
    array=[0,1,2,3,4,5,6,7,8,9]
    print(shuffle_array(array))