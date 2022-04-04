# Jundan Haris - 13520155
# Tugas Kecil 3 - 15-Puzzle Solver
# IF2211 Strategi Algoritma

#import
import time
from node import *
from prioqueue import *
import copy

#membaca file dari folder testcase
def readfile(dir):
    f = open(dir, 'r')
    lines = f.readlines()
    matrix = []
    #masukkan ke dalam matrix
    for line in lines:
        temp = line.strip("\n").split(" ")
        matrix.append(temp)
    for i in range(4):
        for j in range(4):
            if matrix[i][j] == '-':
                matrix[i][j] = 16
            else :
                matrix[i][j] = int(matrix[i][j])
    return matrix

#menampilkan matrix puzzle
def printmatrix(matrix):
    for i in range(4):
        for j in range(4):
            if (matrix[i][j] == 16):
                print("-", end="  ")
            else:
                if (matrix[i][j] >= 10):
                    print(matrix[i][j], end=" ")
                else :
                    print(matrix[i][j], end="  ")
        print()

#mencetak tabel kurang(i)
def printkurangi(matrix):
    print("i : kurang(i)")
    for i in range(1, 17):
        x, y = findidx(matrix, i)
        kurangi = hitungkurangi(matrix, x, y)
        print(i, ":", kurangi)

#mencari indeks dari number di matrix
def findidx(matrix, i):
    for x in range(4):
        for y in range(4):
            if matrix[x][y] == i:
                return x, y

#menghitung kurang(i) dari posisi x, y
def hitungkurangi(matrix, x, y):
    count = 0
    number = matrix[x][y]
    for i in range(x, 4):
        for j in range(4):
            if (i == x and j < y):
                continue
            else :
                if (matrix[i][j] < number):
                    count += 1
    return count

#menghitung sigma kurang(i)
def sigmakurangi(matrix):
    sigma = 0
    for i in range(1, 17):
        x, y = findidx(matrix, i)
        kurangi = hitungkurangi(matrix, x, y)
        sigma += kurangi
    return sigma

#menentukan X adalah 0 atau 1
def isXone(matrix):
    x, y = findidx(matrix, 16)
    if ((x % 2 == 0 and y % 2 != 0) or (x % 2 != 0 and y % 2 == 0)):
        return 1
    return 0

#memeriksa apakah matrix sudah solved
def isSolved(matrix):
    idx = 1
    for i in range(4):
        for j in range(4):
            if (matrix[i][j] != idx):
                return False
            idx += 1
    return True

#menghitung jumlah indeks yang tidak sesuai
def countWrongPosition(matrix):
    count = 0
    number = 1
    for i in range(4):
        for j in range(4):
            if (matrix[i][j] != number):
                count += 1
            number += 1
    return count

#mencari semua possible move
def findpossiblemove(node):
    x, y = findidx(node.matrix, 16)
    temp = []
    if (x > 0):
        temp.append("up")
    if (x < 3):
        temp.append("down")
    if (y > 0):
        temp.append("left")
    if (y < 3):
        temp.append("right")
    return temp

#menggeser ubin kosong
def movetiles(matrix, move):
    x, y = findidx(matrix, 16)
    temp = matrix[x][y]
    if move == "up":
        matrix[x][y] = matrix[x - 1][y]
        matrix[x - 1][y] = temp
    elif move == "right":
        matrix[x][y] = matrix[x][y + 1]
        matrix[x][y + 1] = temp
    elif move == "down":
        matrix[x][y] = matrix[x + 1][y]
        matrix[x + 1][y] = temp
    elif move == "left":
        matrix[x][y] = matrix[x][y - 1]
        matrix[x][y - 1] = temp
    return matrix

#melihat matriks apabila digeser dengan arah move   
def seemovetiles(matrix, move):
    x, y = findidx(matrix, 16)
    temp = copy.deepcopy(matrix)
    if move == "up":
        temp[x][y] = temp[x - 1][y]
        temp[x - 1][y] = 16
    elif move == "right":
        temp[x][y] = temp[x][y + 1]
        temp[x][y + 1] = 16
    elif move == "down":
        temp[x][y] = temp[x + 1][y]
        temp[x + 1][y] = 16
    elif move == "left":
        temp[x][y] = temp[x][y - 1]
        temp[x][y - 1] = 16
    return temp

#menampilkan solusi secara step by step
def showSolution(node, matrix):
    move = []
    while (node.parent != None):
        move.append(node.move)
        node = node.parent
    idx = 1
    if move == []:
        print("Puzzle merupakan solusi!")
    for i in range(len(move)-1, -1, -1):
        print("MOVE "+ str(idx), ": ", end="")
        idx += 1
        temp = move[i]
        if (temp == "up"):
            print("UP")
        elif (temp == "down"):
            print("DOWN")
        elif (temp == "left"):
            print("LEFT")
        elif (temp == "right"):
            print("RIGHT")
        printmatrix(movetiles(matrix, move[i]))
        print()
    print()
    print("Jumlah step =", len(move))

#main program
print("======= 15-Puzzle Solver =======\n")
filename = input("Masukkan nama file: ")
filefound = True
try :
    matrix = readfile("testcase/" + filename)
except:
    print("file tidak ditemukan")
    filefound = False

if filefound:
    print("\n=========== Puzzle ===========")
    printmatrix(matrix)
    print("\n====== Tabel KURANG(i) =======")
    printkurangi(matrix)
    print("sigma kurang(i) =", sigmakurangi(matrix))
    print("nilai X =", isXone(matrix))
    temp = sigmakurangi(matrix) + isXone(matrix)
    print("sigma kurang(i) + X =", temp)

    #Puzzle tidak dapat diselesaikan
    if (temp % 2 != 0):
        print("\nGoal state tidak dapat dicapai")
    
    #Puzzle dapat diselesaikan
    else :

        #Algoritma Branch and Bound
        print("\nGoal state dapat dicapai")
        print("solving puzzle...")
        
        #untuk menghitung waktu eksekusi
        start = time.time()
        
        #inisialisasi
        prioq = PriorityQueue(lambda a,b : a.cost < b.cost)
        nodecount = 1
        depth = 0
        statevisited = {}
        nodesolution = None

        finished = isSolved(matrix)
        #apabila matriks awal adalah matriks goal
        if finished:
            statevisited[str(matrix)] = True
            nodesolution = node()
            nodesolution.matrix = matrix
            nodesolution.parent = None
        #apabila matriks awal bukan matriks goal
        else :
            #inisialisasi root node
            rootNode = node()
            rootNode.matrix = matrix
            rootNode.cost = countWrongPosition(matrix) + depth
            rootNode.depth = depth
            rootNode.parent = None
            rootNode.move = ""

            prioq.enqueue(rootNode)

            #loop
            while((not finished) or (not prioq.is_empty)):
                temp = prioq.dequeue()
                
                #memeriksa matriks
                if (isSolved(temp.matrix)):
                    nodesolution = temp
                    finished = True
                    continue
                statevisited[str(temp.matrix)] = True
                
                for move in findpossiblemove(temp):
                    #memasukkan state-state baru ke prioqueue
                    moved = seemovetiles(temp.matrix, move)
                    if (str(moved) not in statevisited):
                        temp1 = node()
                        temp1.matrix = moved
                        temp1.depth = temp.depth + 1
                        temp1.cost = countWrongPosition(moved) + temp1.depth
                        temp1.parent = temp
                        temp1.move = move

                        prioq.enqueue(temp1)
                        nodecount += 1

        #menampilkan solusi
        print("solved!\n")
        print(">> SOLUTION STEP BY STEP\n")
        showSolution(nodesolution, matrix)
        print("jumlah node =", nodecount)
        end = time.time()
        print("Waktu yang dibutuhkan : " + str(end-start) + " detik")
        print()