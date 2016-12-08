from __future__ import division


category = [[],[],[],[],[]]
category[0].append("normal")
with open("training_attack_types.txt", "r") as f:
    for line in f.readlines():
        attack, cat = line.strip().split(" ")
        if cat == "dos": category[1].append(attack)
        elif cat == "u2r": category[2].append(attack)
        elif cat == "r2l": category[3].append(attack)
        elif cat == "probe": category[4].append(attack)

def find_cat(attack):
    for idc, cats in enumerate(category):
        if attack in cats: return idc


protocol = set([])
server = set([])
status = set([])
minmax = []
for _ in range(41):
    minmax.append([float("inf"), 0])


def find_margin(datas):
    for idd, data in enumerate(datas):
        if idd in [1,2,3]: continue
        else:
            data = float(data)
            if data < minmax[idd][0]: minmax[idd][0] = data
            elif data >= minmax[idd][1]: minmax[idd][1] = data


def normalization(lines, filetype):
    if filetype == "train": filename = "train.in"
    elif filetype == "test": filename = "test.in"

    with open(filename, "w") as fout:
        for line in lines:
            if filetype == "train": *datas, attack = line.strip().split(",")
            elif filetype == "test": datas = line.strip().split(",")
            

            for idd, data in enumerate(datas):
                
                # Non-numerical data
                if idd == 1:
                    for idp, p in enumerate(protocol):
                        if data == p: data = (idp+1)/len(protocol)
                elif idd == 2:
                    for ids, s in enumerate(server):
                        if data == s: data = (ids+1)/len(server)+1
                    # Last one
                    if type(data) != type(1.1): data = 1.0
                elif idd == 3:
                    for ids, sta in enumerate(status):
                        if data == sta: data = (ids+1)/len(status)

                else:
                    # Numerical data
                    data = float(data)
                    margin = minmax[idd][1] - minmax[idd][0]
                    try:
                        data /= margin
                    except ZeroDivisionError: data = float(data)

                fout.write("{},".format(data))
            fout.write("\n")


# For training data
with open("train") as ftrain:
    lines = ftrain.readlines()
    
    fout = open("train.out", "w")
    # Read the category
    for line in lines:
        *datas, attack = line.strip().split(",")
        
        # Write .out file as labels
        fout.write(str(find_cat(attack)) + "\n")
        
        # Read non-numerical data
        prot, serv, stat = datas[1], datas[2], datas[3]
        protocol.add(prot)
        server.add(serv)
        status.add(stat)

        # Find margin
        find_margin(datas)

    fout.close()
    print (protocol, server, status)
    # Normalization
    normalization(lines, "train")
    
# For testing data
with open("test", "r") as ftest:
    # Initial the minmax value
    minmax = []
    for _ in range(41):
        minmax.append([float("inf"), 0])
    
    lines = ftest.readlines()
    for line in lines:
        datas = line.strip().split(",")
        find_margin(datas)
    
    normalization(lines, "test")