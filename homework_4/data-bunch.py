import math, matplotlib.pyplot as plt, sys

def bunch(name,out_name,seq):
    s=0
    ssq=0
    with open(out_name,'w') as out_file:
        with open(name) as input_file:
            count=0
            previous=0
            for line in input_file:           
                parts=line.strip().split(',')
                if count%2==0:
                    previous=float(parts[-1])
                else:
                    value=float(parts[-1])
                    s+=(value+previous)
                    ssq+=(value*value+previous*previous)
                    out_file.write('{0}\n'.format((value+previous)/2))
                count+=1
                if count%1000000==0:
                    print ('Seq={0}, iteration={1}'.format(seq,count))
    mean=s/count
    return (count//2,mean, math.sqrt((ssq/count-mean*mean)/count))


def out_file_name(name,seq):
    parts=name.split('.')
    return '{0}{1}.{2}'.format(parts[0],seq,parts[1]) 

if __name__=='__main__':
    sigmas=[]
    count=sys.maxsize
    seq=1
    name='bunch.txt'
    previous=name
    while count>1:
        out=out_file_name(name,seq)  
        count,mean,sigma=bunch(previous,out,seq)
        previous=out
        sigmas.append(sigma)
        print (count,mean,sigma)
        seq+=1
    plt.plot(sigmas)