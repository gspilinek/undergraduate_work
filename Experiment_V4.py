
#to run simply double click the python file and choose a properly formatted text file as input
#program will generate output.txt as well as LessThanVikas.txt
from copy import deepcopy

from random import seed
from random import randint

import math

from tkinter import filedialog
from tkinter import *


                ###########
# FUNCTIONS#
                ###########

def Notdone (mat):
     for x in range(0 ,len(mat)):
         if(mat[x] != -1):  # if something is not -1 we have not finished splitting yet
             return True

     return False  # if we only found -1 then we are done looping

def EMD(a ,b):
     emd =0
     a = deepcopy(a)
     b = deepcopy(b)
     
     for x in range (0, len(a ) -1):
         if(a[x]>=b[x]):  # if the first element in a > b
                 temp = a[x ] -b[x]  # find out how much we need to move
                 a[ x +1 ]+= temp  # move it from a[x] to a[x+1]
                 a[x]-=temp  # remove it from a[x]
         else:  # else then a < b
             temp = b[x] - a[x]  # find out how much we need to move
             a[x+1]-=temp  # remove it from a[x+1]
             a[x]+=temp  # move it from a[x+1] to a[x]
         emd+=temp  # add the normalized amount to emd

     return emd /(len(a ) -1)  # return emd
     
def D1Total(mat)  :  # computes the total value of all numbers in the matrix 1D
     total =0
     for x in range(0 ,len(mat)):
         total+=mat[x]
     
     return total
     
def D2Total(mat)  :  # computes the total value of all numbers in the matrix 2D
     total =0
     for x in range(0 ,len(mat)):
         for y in range(0 ,len(mat[0])):
             total+=mat[x][y]
             
     return total

def Max_of_matrix (mat):  # returns a list formatted as [maxvalue, row_location, col_location] and removes that entry from the matrix so we don't find it again
     max = [mat[0] ,0]  # initialize max to a value in the matrix
     flag = True
     for x in range(1, len(mat)):   
         if(max[0] <mat[x]):  # if our max is smaller than a number we find
             max[0] = mat[x]  # replace our old max
             max[1 ] =x  # change old row location
             flag = False
     mat[max[1] ] =-1  # make the max location -1 so we won't consider it since all real numbers left will be >= 0
     
     return max  # return the list

def Vikas(matrix ,c):  # Split into layers according to Vika's method
     temp = deepcopy(matrix)  # make a temp variable so we don't edit the original matrix
     splitting = [[0 ]* len(temp) for x in range(c)]
     
     onLayer =0
     
     while (Notdone(temp)):
         max = Max_of_matrix(temp) 
         x = int(max[0 ] /c)
         y = max[0 ] %c
         
         for a in range(0 ,c):
             splitting[onLayer][max[1]] = x
             onLayer+=1
             if(onLayer > c -1):
                 onLayer =0

         for a in range(0 ,y):
            splitting[onLayer][max[1]] = x+ 1
            onLayer += 1
            if (onLayer > c - 1):
                onLayer = 0

         if (onLayer > c - 1):
            onLayer = 0

     return splitting


def rowSum(mat, t):  # calculates the row sum of a matrix and stores it as a list that is returned
    rsum = []

    for x in range(0, len(mat)):  # for each row
        temp = mat[x]
        if (temp != 0):
            rsum.append(temp / t)  # apppend its probability distribution
        else:
            rsum.append(0)
    return rsum


def MaxRowSumDistance(split, rsum, c):  # calculates max row sum
    maxRowSum = 0
    for x in range(0, c - 1):
        tempEMD = EMD(split[x], rsum)
        if (maxRowSum < tempEMD):
            maxRowSum = tempEMD

    return maxRowSum


def RandomSplit(inputRecords, o, c, k, R, rowsum, maxRowSum, vMethod):
    counter = 0
    flag = True
    length = len(inputRecords)

    o.write("\n")
    o.write("Here down will be Max Emd for random splittings\n")
    trial = 0
    a = []
    places = []
    remainder_to_distribute = []
    amount_for_each_spot = []
    randsum = []

    while (trial < R):

        #choose the amount of layers
        #calculate the "remainder", left over after evenly splitting between layers
        #make the "even split" matrix
        #make a matrix with the remainders randomly put into it
        #move these remainders around a random amount of times without violating restrictions
        #check to see if the random generation's EMD is better thank Vikas's method\
        #print the matrix to the output file with max EMD
        #if the max EMD is less than Vikas's print to a seperate file


        #making the matricies have random layers
        layers = randint(c // 2, c + c)  # subject to change feel free to adjust the range
        evenSplit = [[0] * length for l in range(layers)]
        addOnRemainder = [[0] * length for l in range(layers)]

#        Calculating the remainder
        for y in range(0,length):
            a.append( inputRecords[y])
            remainder_to_distribute.append( a[y] % layers )
            amount_for_each_spot.append(math.floor(a[y] // layers ))

        if sum(amount_for_each_spot) > k:

            for col in range(0,length):
                for l in range(0,layers):
                    evenSplit[l][col] = amount_for_each_spot[col]


            # #no longer using this approach because vikas method and trials can be different lengths
            # # calculating diffences between totals of matricies
            # diff = [[0] * length for x in range(c)]
            # for z in range(0, c):
            #     for x in range(0, length):
            #         print("z: "+str(z)+  "\tx: "+str(x) )
            #         print(len(diff))
            #         diff[z][x] = vMethod[z][x] - rand[z][x]

            for col in range(0,length):
                spot = randint(0,layers-1)
                while(remainder_to_distribute[col]>0):
                    if addOnRemainder[spot][col] == 0:
                        addOnRemainder[spot][col] +=1
                        remainder_to_distribute[col]-=1
                        spot+=1

                    else:
                        spot+=1


                    if spot > layers-1:
                        spot=0

            #fills a list with coordinates in addOnRemainder that are currently 1's
            for row in range(0, layers):
                for col in range(0, length):
                    if addOnRemainder[row][col] == 1:
                        places.append([row, col])

            swaps = randint(1, 10)  #generate a random amount of swaps to make subject to change
            z=0

            while (z < swaps):
                seed()


                x = randint(0, len(places) - 1)
                layer1 = places[x][0]#row
                spot_in_layer1 = places[x][1]#col

                if addOnRemainder[layer1][spot_in_layer1] == 1:

                    y = randint(0, len(places) - 1)
                    layer2 = places[y][0]#row
                    spot_in_layer2 = places[y][1]#col
                    if not x == y and addOnRemainder[layer1][spot_in_layer2] == 1:
                        z += 1
                        addOnRemainder[layer1][spot_in_layer1] -= 1
                        addOnRemainder[layer2][spot_in_layer2] -= 1


                        flag1=False
                        flag2=False
                        while (True):
                            if not flag1:
                                    layer1 += 1
                                    if (layer1 > layers - 1):
                                        layer1 = 0
                                    #print("layer1:"+str(layer1))
                                    #print("diff[layer1][spot_in_layer1]"+str(diff[layer1][spot_in_layer1]))
                                    if addOnRemainder[layer1][spot_in_layer1] == 0:
                                        addOnRemainder[layer1][spot_in_layer1] += 1
                                        flag1=True
                            if not flag2:
                                    layer2 -= 1
                                    if (layer2 < 0):
                                        layer2 = layers - 1
                                    #print("layer2:" + str(layer2))
                                    #print("diff[layer2][spot_in_layer2]"+str(diff[layer2][spot_in_layer2]))
                                    if addOnRemainder[layer2][spot_in_layer2] == 0:
                                        addOnRemainder[layer2][spot_in_layer2] += 1
                                        flag2=True

                            if(flag1 and flag2):
                                break

                        if x > y:
                            # print(str(x) +"\t"+str(y))
                            places.pop(x)
                            places.pop(y)

                        elif y > x:
                            # print(str(x) + "\t" + str(y))
                            places.pop(y)
                            places.pop(x)

                        places.append([layer1, spot_in_layer1])
                        places.append([layer2, spot_in_layer2])

            for x in range(0, layers):
                for y in range(0, length):
                    evenSplit[x][y] += addOnRemainder[x][y]



            if (flag):  # not needed just left it in in case i want to use a flag,flag is always true
                for r in range(0, layers):
                    T = D1Total(evenSplit[r])
                    randsum.append(rowSum(evenSplit[r], T))

                maxEMD = MaxRowSumDistance(randsum, rowsum, layers)

                o.write("Trial #" + str(trial) + "\n")
                o.write("Amount of layers: "+ str(layers)+ "\n")
                for w in range(0, layers):
                    o.write(str(evenSplit[w]))
                    o.write("\t")
                    o.write(str(sum(evenSplit[w])))
                    o.write("\n")

                o.write(str(maxEMD))
                o.write("\n")
                trial += 1

                if (maxEMD <= maxRowSum):
                    g = open("LessThanVikas.txt", "a")
                    for w in range(0, layers):
                        g.write(str(evenSplit[w]))
                        g.write("\n")

                    g.write("Random Split EMD: " + str(maxEMD))
                    g.write("\tVikas' EMD: " + str(maxRowSum))
                    g.write("\n")
                    g.close()

        evenSplit.clear()
        addOnRemainder.clear()
        amount_for_each_spot.clear()
        remainder_to_distribute.clear()
        randsum.clear()
        places.clear()
        a.clear()


# random = randint(0,num[0])


def main():
    root = Tk()
    root.filename = filedialog.askopenfilename(initialdir="C:\\", title="Select A file",
                                               filetypes=(("text files", "*.txt"), ("all files", "*.*")))
    print(root.filename)

    f = open(root.filename, 'r')  # open the text document, needs to be 2nd argv because 1st one is the file name itself

    try:
        k = int(f.readline())

        line = f.readline()
        length = len(line)
        m = 0
        spaces = [0]
        for y in range(0, length):
            temp = (line[y])
            if temp.isspace():
                m += 1
                spaces.append(y)

        del spaces[0]
        data = [0] * m
        start = 0
        # print(spaces)
        # print("\n")
        for y in range(0, m):  # for the length of the line
            temp = deepcopy(line)
            # print("start: "+str(start))
            # print("temp[start:(spaces[y]]): "+ temp[start:spaces[y]])
            # print("y: "+str(y))
            # print("spaces[y]: "+str(spaces[y]))

            inputNum = int(temp[start:spaces[y]])
            data[y] = (inputNum)  # add it to the array as an int
            start = spaces[y]
            # print("end of line "+str(y))
            # print("\n")
            if (start == spaces[-1]):
                break
        R = int(f.readline())  # number of random trials
    # EXCEPT
    finally:
        f.close()

    c = math.floor(D1Total(data) / k)

    o = open("output.txt", "w")  # opens the file for writing output
    o.write("K for this output is ")
    o.write(str(k))
    o.write("\n")

    vMethod = Vikas(data, c)

    rowcheck = 0  # variable to store amount or rows that had k+1

    for w in range(0, c):
        if (sum(vMethod[w]) == k + 1):
            rowcheck += 1

    for w in range(0, c):
        o.write(str(vMethod[w]))
        o.write("\t")
        o.write(str(sum(vMethod[w])))
        o.write("\n")

    vsum = []

    for x in range(0, len(vMethod)):
        T = D1Total(vMethod[x])
        vsum.append(rowSum(vMethod[x], T))

    rsum = []
    t = D1Total(data)
    for x in range(0, len(data)):
        rsum.append(data[x] / t)

    maxRowSum = MaxRowSumDistance(vsum, rsum, c)

    o.write("\n")
    o.write("Max Emd for Vikas's Method: " + str(maxRowSum))

    k = math.ceil(D1Total(data) / c)

    RandomSplit(data, o, c, k, R, rsum, maxRowSum, vMethod)

    o.close()


if __name__ == "__main__":
    main()