def simple_deviders(number):
    i=2
    deviders=[]
    deviders_str=''
    limit=number**(0.5)
    while (number!=1):
        if number%i==0:
            number/=i
            deviders.append(i)
            i=2
        elif i>limit:
            deviders.append(int(number))
            break
        else:
            i+=1
    deviders_str+=str(deviders[0])
    for i in range(1,len(deviders)):
        deviders_str+=str('*')
        deviders_str+=str(deviders[i])
    return deviders_str
def all_deviders(number):
    deviders=[]

    for i in range(1,number//2+1):
        if number%i==0:
            deviders.append(i)
    
    return deviders
def summ(Array):
    summ=0
    for i in range(0,len(Array)):
        summ+=Array[i]
    return summ
def run():
    number=int(input())
    s_deviders=simple_deviders(number)
    a_deviders=all_deviders(number)
    deviders_summ=summ(a_deviders)
    print(number,'=',s_deviders)
    print('n=',len(a_deviders))
    print(a_deviders)
    print('summ=',deviders_summ)
run()
