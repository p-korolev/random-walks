#helper function
def partition_set(lst, n):
    '''Partitions list into n lists'''
    length = len(lst)
    index_border = (length//n)*n
     
    p = []
    final_P = []
    for i in range(index_border):
        if ((i+1)%n) == 0:
            p.append(lst[i])
            final_P.append(p)
            p=[]
            continue
        if i+1%n != 0 or i==0:
            p.append(lst[i])      
    if (len(lst)%n!=0):
        final_P.append(lst[index_border:])
    return final_P
