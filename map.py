# transpose map matrix for compatibility

mapBorder = 150

def transpose(l1, l2):
    for i in range(len(l1[0])):
        # print(i)
        row =[]
        for item in l1:
            row.append(item[i])
        l2.append(row)
    return l2

seedMapOG = [[2,1,2,0,2,1,0,2,1,2,0],
             [1,1,1,0,2,1,0,2,2,0,0],
             [6,6,8,7,0,2,1,0,0,1,1],
             [1,2,2,8,2,0,6,8,7,6,7],
             [0,0,0,6,8,7,9,2,2,0,1],
             [0,2,1,0,0,1,0,1,2,2,2],
             [0,0,1,2,1,2,1,0,1,1,1]]

seedMap = []
seedMap = transpose(seedMapOG, seedMap)
