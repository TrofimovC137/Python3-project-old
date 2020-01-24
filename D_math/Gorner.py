from math import fabs
class fraction():
    def __init__(self,numerator,denominator):
        for i in range(1,max(numerator,denominator)):
            if (numerator%i==0)and(denominator%i==0):
                numerator/=i
                denominator/=i
        self.numerator=int(numerator)
        self.denominator=int(denominator)
    def __str__(self):
        return str(self.numerator)+'/'+str(self.denominator)
    def __add__(self,other):
        if (type(other)==int):
            new_denominator=self.denominator
            new_numerator=self.numerator+other*self.denominator
        elif (type(other)==fraction):
            new_denominator=self.denominator*other.denominator
            new_numerator=self.numerator*other.denominator+other.numerator*self.denominator
        result=fraction(new_numerator,new_denominator)
        if (result.numerator%result.denominator==0):
            result=int(result.numerator/result.denominator)
        return result
    def __sub__(self,other):
        if (type(other)==int):
            new_denominator=self.denominator
            new_numerator=self.numerator-other*self.denominator
        elif (type(other)==fraction):
            new_denominator=self.denominator*other.denominator
            new_numerator=self.numerator*other.denominator-other.numerator*self.denominator
        result=fraction(new_numerator,new_denominator)
        if (result.numerator%result.denominator==0):
            result=int(result.numerator/result.denominator)
        return result
    def __mul__(self,other):
        result=fraction(self.numerator*other.numerator,self.denominator*other.denominator)
        if (result.numerator%result.denominator==0):
            return int(result.numerator/result.denominator)
        else:
            return result
    def __truediv__(self,other):
        result=fraction(self.numerator*other.denominator,self.denominator*other.numerator)
        if (result.numerator%result.denominator==0):
            return int(result.numerator/result.denominator)
        else:
            return result
def all_deviders(number):
    deviders=[number]
    number=int(number)
    for i in range(1,number//2+1):
        if number%i==0:
            deviders.append(i)
    l=len(deviders)
    for i in range(0,l):
        deviders.append(deviders[i]*(-1))
    return deviders
def gorner(coefficients):
    if len(coefficients)==2:
        return [coefficients[1]*(-1)]
    else:
        root=0
        new_coefficients=[]
        options_root=all_deviders(fabs(coefficients[-1]))
        for i in range(0,len(options_root)):
            root=options_root[i]
            new_coefficients=[coefficients[0]]
            for j in range(1,len(coefficients)):
                new_coefficients.append(new_coefficients[j-1]*root+coefficients[j])
                if root==18:
                    print(new_coefficients)
            if int(new_coefficients[-1])==0:
                break
        result=[]
        result.append(root)
        result+=gorner(new_coefficients[0:-1])
        return result
