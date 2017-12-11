# -*- coding: utf-8 -*-
from __future__ import division, print_function
import random

def queenss(n,p,arr):
    def placeQueens(k,rp,arr):
        if k==0:
            return [[]]
        else:
            return [[(k, column)] + queens for queens in placeQueens(k - 1,rp,arr) for column in range(1, n + 1) if isSafe((k, column), queens,p)]
    
    return placeQueens(n, p,arr)

def isSafe(queen, queens, p):
    return all(not inCheck(queen, q, p) for q in queens)

def inCheck(q1, q2,p):
    
    if q1[0] == q2[0]: # 同列
        return True
    if q1[1] == q2[1]: # 同行
        return True
    if abs(q1[0] - q2[0]) == abs(q1[1] - q2[1]): # 對角線
        return True
    return False

def isSafe2(queen, queens, p):
    return all(not inCheck2(queen, q, p) for q in queens)

def inCheck2(q1, q2,p):
    
    if q1[0] == q2[0]: # 同列
        if abs(q1[1] - q2[1])<=p:
            return True
    if q1[1] == q2[1]: # 同行
        if abs(q1[0] - q2[0])<=p:
            return True
    if abs(q1[0] - q2[0]) == abs(q1[1] - q2[1]): # 對角線
        if abs(q1[0] - q2[0])<=p and abs(q1[1] - q2[1])<=p:
            return True
    return False

number = int(input("Input map's range: "))
p = int(input("Input fire range (default is -1 ): "))
if p == -1:
    p = number

put_queen = input("Input queen's position (input -1 to end ): ")
set_queen = []
while put_queen !='-1':
    tmp = put_queen.split(' ')
    if int(tmp[0])<=number and int(tmp[1])<=number:
        set_queen.append((int(tmp[0]),int(tmp[1])))
    else:
        print("wrong position")
        break
    put_queen = input("Input queen's position (input -1 to end ): ")
    pass
print('find solution...')

all_map = queenss(number,p,[[]])

fil_map = []
for x in all_map:
    tmp = 1
    for y in set_queen:
        if y not in x:
            tmp = 0
            break
    if tmp==1:
        fil_map.append(x)

# print(fil_map)


# for qs in queenss(number,p):
#     for q in qs:
#         print(q, end="")
#     print()

# for x in fil_map:
#     print(x)
# print()
rand_map = random.randint(0,len(fil_map)-1)
queenNum = number
for x in range(1,number+1):
    for y in range(1,number+1):
        if (x,y) not in fil_map[rand_map]:
            # print('haha')
            tmp = (x,y)
            if isSafe2(tmp,fil_map[rand_map],p):
                fil_map[rand_map].append(tmp)
                queenNum+=1

print()
print(fil_map[rand_map])
print('queens\' number: ',queenNum,'\n')
for x in range(1,number+1):
    for y in range(1,number+1):
        a = (x,y)
        if a in fil_map[rand_map]:
            print('Q',end=" ")
        else:
            print('.', end=" ")
    print()
# print('\nsolutions: ',len(fil_map))



