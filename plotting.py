import matplotlib.pyplot as plt
import numpy as np
import random #just if you want random colors for plots
#check out seaborn for prettier plots

#create mock-data
results={"Gene x":{"A": [2,0.5], "B": [3,0.6], "C": [4,0.8], "D":[5, 1]},
         "Gene y":{"A": [2.5,0.5], "B": [3.5,0.6], "C": [4.5,0.8], "D":[5.5, 1]},
         "Gene z":{"A": [3.5,0.5], "B": [4.5,0.6], "C": [5.5,0.8], "D":[1.5, 1]}
}

#give empty lists for parameters shown in graphs
value = []
error = []
label = []

#loop through the sub-dictionaries (e.g. dictionary under key "Gene x"). For ech loop/each gene, a new graph depicting all samples is created.
for v,w  in results.items():
    #print(w) #just for testing

    #start creation of NEW plot. Without that, plots would just be added on top of each other
    plt.figure()
    #loop through keys within the sub-dictionaries
    for x in w:
        #print (w[x][0]) #just for testing
        #create lists for each parameter shown in graph for current gene
        value.append (float(w[x][0]))
        error.append (float(w[x][1]))
        label.append (x) #have to make that more elegant
    #print (value) #just for testing
    #print (error) #just for testing
    #make toitle for current gene
    plt.title("Result for " + str(v))
    #rotate labels 90° to make long lables fit on graph
    plt.xticks(rotation= -90)
    #create random colors from gene to gene
    r = lambda: random.randint(0,255)
    color = ('#%02X%02X%02X' % (r(),r(),r()))
    #create graph with one bar per sample, lables and error bars with caps of size 5
    plt.bar(x = np.arange(len(value)), height=value, yerr = error,align='center', tick_label = label, capsize = 5, color = color)
   # plt.show()
   #save the plot
    plt.savefig("image"+str(v)+".png",bbox_inches='tight',dpi=100)

    #reset parameters for next loop
    value = []
    error = []
    label = []










"""
#Old Versions:
A=[]
B=[]
for v,w  in results.items():
    #print(w)
    for x in w:
        #print (w[x][0])
        A.append (float(w[x][0]))
        B.append (float(w[x][1]))
    print (A)
    print (B)
    A = []
    B = []
A = [2.5, 3.5, 4.5, 5.5]
B = [0.5, 0.6, 0.8, 1.0]
my_plot = plt.bar(x = np.arange(len(A)), height=A, yerr = B,align='center')



#for genes in results:
#    for sample in [genes]:
#        for key in genes[sample]:
#            print (key)



#fig, ax = plt.subplots()
#rects1 = ax.bar(data = results ["Gene X"][1])




#plt.show()"""