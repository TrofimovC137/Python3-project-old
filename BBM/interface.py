from graf import *
def read_matrix(n):
    print('введите матрицу неисправностей')
    matrix=[]
    for i in range(n):
        matrix.append([int(j) for j in input().split(' ')])
    print('Введите вероятности состояний Si')
    P=[float(i) for i in input().split(' ')]
    print('Введите стоимости проверок Zi')
    C=[float(i) for i in input().split(' ')]
    return state_matrix(matrix,P,C,[])
def run_main():
    '''print('кажите колличесвто состояний объекта контроля')
    a=read_matrix(int(input()))
    print('Задана следующая таблица неисправностей')
    a.print_matrix()
    result=main(a)
    input()'''
    matrix=Graf_State_Interface()
    print('Введите вероятности состояний Si')
    P=[float(i) for i in input().split(' ')]
    print('Введите стоимости проверок Zi')
    C=[float(i) for i in input().split(' ')]
    a=state_matrix(matrix,P,C,[])
    result=main(a)
    Thread_screen(result)
run_main()
