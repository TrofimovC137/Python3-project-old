from math import *
import itertools
class state_matrix():
    # i-Z
    # j-P
    def __init__(self,matrix,P,C,checks_performed):
        self.matrix=matrix
        self.C=C
        self.P=P
        self.checks_performed=checks_performed
    def print_matrix(self):
        for i in range(len(self.matrix)):
            print(self.matrix[i],self.P[i])
    def S0(self,zi):
        matrix=[]
        P=[]
        C=[]
        checks_performed=self.checks_performed+[zi]
        for i in range(0,len(self.matrix)):
            if (self.matrix[i][zi-1]==0):
                matrix.append(self.matrix[i])
                P.append(self.P[i])
                C.append(self.C[i])
        return state_matrix(matrix,P,C,checks_performed)
    def S1(self,zi):
        matrix=[]
        P=[]
        C=[]
        checks_performed=self.checks_performed+[zi]
        for i in range(0,len(self.matrix)):
            if (self.matrix[i][zi-1]==1):
                matrix.append(self.matrix[i])
                P.append(self.P[i])
                C.append(self.C[i])
        return state_matrix(matrix,P,C,checks_performed)
    def get_Si(self,i):
        return self.matrix[i-1]
    def get_Zi(self,i):
        Z=[]
        for j in range(len(self.matrix)):
            Z.append(self.matrix[j][i-1])
        return Z
class thread_element():
    def __init__(self, k, Z, C):
        self.k=k
        self.C=C
        self.Z=Z
        self.next_element=[]
def C(Ci,PSk):
    result=0
    for i in range(1,len(Ci)):
        result+=Ci[i]*sum(PSk[:i])
    return result
def Psum(P):
    P.sort()
    result=[]
    if (len(P)==1):
        return [0]
    else:
        for i in range(2,len(P)+1):
            result.append(sum(P[:i]))
        return result
def Cn(st_matr,Zi,C):
    s0=st_matr.S0(Zi)
    s1=st_matr.S1(Zi)
    return C*(sum(st_matr.P)+sum(Psum(s0.P))+sum(Psum(s1.P)))
def Cn2(S,Z,C):
    Sum=0
    for i in range(len(S)):
        Sum+=C*(Cn(S[i],Z[i],C)+sum(S[i].P))
    return Sum
def useless_checks(matr):
    checks=[]
    for i in range(len(matr.matrix[0])):
        if (0 in matr.get_Zi(i+1))==False or (1 in matr.get_Zi(i+1))==False:
            checks.append(i+1)
    return checks
def choose_the_best_check(matr,k,thread):
    C=[]
    useless=useless_checks(matr)
    for i in range(1,len(matr.get_Si(1))+1):
        if ((i in matr.checks_performed)==False) and ((i in useless)==False):
            C.append(Cn(matr,i,1))
        else:
            C.append(float('+inf'))
    print('имеются следующие возможные проверки:')
    for i in range(len(C)):
        if C[i]!=float('+inf'):
            print('Z',i+1,' C=',C[i])
            thread[-1].append(thread_element(k,i+1,C[i]))
    return C.index(min(C))+1
def possible_checks(matrix):
    checks=[]
    for j in range(1,len(matrix.get_Si(1))):
            if (j in matrix.checks_performed)==False and (j in useless_checks(matrix))==False:
                checks.append(j)
    return checks
def check_group(matr_list):
    possible_checks=[]
    for i in matr_list:
        possible_checks.append([])
        for j in range(1,len(i.matrix[0])+1):
            if (j in i.checks_performed)==False and (j in useless_checks(i))==False:
                possible_checks[-1].append(j)
    return list(itertools.product(*possible_checks))
def choose_the_best_check_group(matr_list,k,thread):
    checks=check_group(matr_list)
    C=[]
    for i in range(len(checks)):
        C.append(Cn2(matr_list,checks[i],1))
    print('Имеются следующие возможные группы проверок:')
    for i in range(len(checks)):
        print('Z',checks[i],' C=',C[i])
        thread[-1].append(thread_element(k,checks[i],C[i]))
    return checks[C.index(min(C))]
def main(matrix):
    checks=[]
    state=[matrix]
    thread=[[thread_element(0,0,0)]]
    k=1
    while (len(state)!=0):
        thread.append([])
        print('итерация №',k)
        print('имеются следующие не выделенные состояния системы:')
        for i in state:
            i.print_matrix()
            print('_______________________________')
        if len(state)==1:
            checks.append(choose_the_best_check(state[0],k,thread))
            print('наилучшая проверка  - Z',checks[-1])
            state=[state[0].S0(checks[-1]),state[0].S1(checks[-1])]
        else:
            checks.append(choose_the_best_check_group(state,k,thread))
            print('наилучшая группа проверок  - Z',checks[-1])
            new_state=[]
            for i in range(len(state)):
                new_state.append(state[i].S0(checks[-1][i]))
                new_state.append(state[i].S1(checks[-1][i]))
            state=new_state
        j=0
        while j<len(state):
            if len(state[j].matrix)==1 or len(state[j].matrix)==0:
                del state[j]
            else:
                j+=1
        print('=============================')
        k+=1
    print('Результат:')
    print(checks)
    return (checks,thread)
