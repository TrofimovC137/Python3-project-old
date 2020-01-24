def decomposition(number):
    result=[]
    if number==0:
        result=[0]
    elif number==9:
        result=[1,10]
    elif number==4:
        result=[1,5]
    elif number==5:
        result=[5]
    elif number>5:
        result.append(5)
        number-=5
        while number!=0:
            number-=1
            result.append(1)
    else:
        while number!=0:
            number-=1
            result.append(1)
    return result
def arabian_roman(number):
    if number<=3999:
        arab_number=[]
        roman_number=''
        while number!=0:
            arab_number.append(number%10)
            number//=10
        for i in range(0,len(arab_number)//2):
            arab_number[i],arab_number[-i-1]=arab_number[-i-1],arab_number[i]
    else:
        print('Число > 3999')
    for i in range(0,len(arab_number)):
        arab_number[i]=decomposition(arab_number[i])
    rang=len(arab_number)
    for i in range(0,len(arab_number)):
        if rang==4:
            for j in range(0,len(arab_number[i])):
                roman_number+='M'
            rang-=1
        elif rang==3:
            for j in range(0,len(arab_number[i])):
                if arab_number[i][j]==10:
                    roman_number+='M'
                if arab_number[i][j]==5:
                    roman_number+='D'
                if arab_number[i][j]==1:
                    roman_number+='C'
            rang-=1
        elif rang==2:
            for j in range(0,len(arab_number[i])):
                if arab_number[i][j]==10:
                    roman_number+='C'
                if arab_number[i][j]==5:
                    roman_number+='L'
                if arab_number[i][j]==1:
                    roman_number+='X'
            rang-=1
        elif rang==1:
            for j in range(0,len(arab_number[i])):
                if arab_number[i][j]==10:
                    roman_number+='X'
                if arab_number[i][j]==5:
                    roman_number+='V'
                if arab_number[i][j]==1:
                    roman_number+='I'
            rang-=1
    return roman_number
def roman_arabian(roman_number):
    arab_number=[]
    rang=0
    for i in range(0,len(roman_number)):
        if roman_number[i]=='M':
            arab_number.append(1000)
        if roman_number[i]=='D':
            arab_number.append(500)
        if roman_number[i]=='C':
            arab_number.append(100)
        if roman_number[i]=='L':
            arab_number.append(50)
        if roman_number[i]=='X':
            arab_number.append(10)
        if roman_number[i]=='V':
            arab_number.append(5)
        if roman_number[i]=='I':
            arab_number.append(1)
    i=len(arab_number)-1
    while i!=0:
        if arab_number[i]>arab_number[i-1]:
            arab_number[i-1]=arab_number[i]-arab_number[i-1]
            arab_number[i]=0
            i-=1
        else:
            i-=1
    result=0
    for i in range(0,len(arab_number)):
        result+=arab_number[i]
    return result
def run():
    print('Введите номер команды')
    print('1)arabian->roman   2)roman-arabian   3)exit')
    operator=int(input())
    while operator!=3:
        if operator==1:
            print('Введите число')
            number=int(input())
            print(number,'=',arabian_roman(number))
        elif operator==2:
            print('Введите число')
            number=str(input())
            print(number,'=',roman_arabian(number))
        else:
            print('Некоректный номер команды')
        print('Введите номер следующей команды')
        print('1)arabian->roman   2)roman-arabian   3)exit')
        operator=int(input())
run()
