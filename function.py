import matplotlib.pyplot as plt
import numpy as np
import random
from matplotlib import colors
import matplotlib.patches as mpatches
import pandas as pd
import math
import statistics
#check out seaborn for prettier plots

def make_plate(ids, samples=[],genes=[]):

    #set grid
    numb_cols = 24 #int(form["cols"])
    numb_rows = 16


    #generating mock data
    #samples = ["1","2", "3","4", "5", "6", "7","8", "9", "10"]
    if samples == [""]:
        samples = []
    if genes == [""] or genes == []:
        genes = ["no genes"]
    samples.append("Water")
    sample_numbers = list(range(1,len(samples)+1))
    #genes = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N']
    gene_numbers=list(range(1,len(genes)+1))
    replicates = 3

    #create data as a list
    data = []
    # filling up data
    for i in gene_numbers: #within the list (data), for every gene...
        for j in sample_numbers: #triplicates of every sample are appended
            r = 0
            while r < replicates:
                data.append(j)
                r += 1 # it's the same as r= r+1, it will increase until 3, and the it will stop.

    # Trim data to max number of wells
    #if len(data) > numb_cols*numb_rows:
     #   print ("Too many for 1 well plate!")
    data = data[0:min([len(data), numb_cols*numb_rows])]#data, empieza de 0 en programación, y después vemos el mínimo de la lista , la longitud de data o los 384

    #Transform data into matrix (i.e., chunks)
    chunks = [data[x:x+numb_cols] for x in range(0, len(data), numb_cols)]
    # if length of last row of chunks is less tha numb_columns
    if len(chunks[len(chunks)-1]) < numb_cols:
        # fill with 0s
    	chunks[len(chunks)-1].extend([0]*(numb_cols-len(chunks[len(chunks)-1])))

    # create discrete colormap: this part is in most parts copy-pasted and has to be uptimized
    #cmap = colors.ListedColormap(['white', 'blue', 'green','darkorchid', 'orange', 'm', 'red', 'gold','k'])
    color=[]
    color.append("#FFFFFF")
    for i in range(len(sample_numbers)-1):
        r = lambda: random.randint(0,255)
        color.append('#%02X%02X%02X' % (r(),r(),r()))
    color.append('#000000')
    #cmap=plt.get_cmap(color)
    cmap = colors.ListedColormap(color)
    bounds=[-1,0.1]
    for i in sample_numbers:
        bounds.append(i+0.1)
    norm = colors.BoundaryNorm(bounds, cmap.N)

    fig, ax = plt.subplots()
    hm = ax.imshow(chunks, cmap=cmap, norm=norm, interpolation="nearest")

    y=[""]*(numb_rows+1)
    # draw gridlines #major ticks
    ax.grid(which='major', axis='both', linestyle='-', color='k', linewidth=2)
    ax.set_xticks(np.arange(-0.5, numb_cols, 1));
    ax.set_yticks(np.arange(-0.5, numb_rows, 1));
    ax.set_yticklabels(y);
    ax.set_xticklabels(y);
    ax = plt.gca();
    ax = plt.gca();

    #ax.set_xticklabels([""]*(numb_cols))
    #ax.set_yticklabels([""]*(numb_rows))

    letters = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]
    numbers =list(range(1,100,1))

    ax.set_yticklabels(letters[0:numb_rows],minor=True)
    ax.set_xticklabels(numbers[0:numb_cols],minor=True)

    # Minor ticks
    ax.set_xticks(np.arange(0, 24, 1), minor=True);
    ax.set_yticks(np.arange(0, 16, 1), minor=True);

    #add legend
    #patches=[mpatches.Patch(color=color[1], label=samples[0]),mpatches.Patch(color=color[11], label=samples[11-1])]
    patches = []
    for i in sample_numbers:
        patches.append(mpatches.Patch(color=color[i], label=samples[i-1]))

    #split legend into cols when longer than x axis (=15)
    banana=(len(samples)//15)+1
    #apple= banana-1
    #plt.legend(handles=patches, bbox_to_anchor=(1.25 + (apple*0.185), 1.026),ncol=banana)
    plt.legend(loc='upper left',handles=patches,bbox_to_anchor=(1, 1.026),ncol=banana)

    plt.savefig("mysite/static/images/"+str(ids)+"_samples.png",bbox_inches='tight',dpi=300)
    #plt.show()
    #sample_plate = open(")

    ############start for genes

    #create data as a list
    data = []
    # filling up data
    for i in gene_numbers: #within the list (data), for every gene...
        for j in sample_numbers: #triplicates of every sample are appended
             r = 0
             while r < replicates:
                data.append(i)
                r += 1


    data = data[0:min([len(data), numb_cols*numb_rows])]#data, empieza de 0 en programación, y después vemos el mínimo de la lista , la longitud de data o los 384

    #Transform data into matrix (i.e., chunks)
    chunks = [data[x:x+numb_cols] for x in range(0, len(data), numb_cols)]
    # if length of last row of chunks is less tha numb_columns
    if len(chunks[len(chunks)-1]) < numb_cols:
        # fill with 0s
    	chunks[len(chunks)-1].extend([0]*(numb_cols-len(chunks[len(chunks)-1])))

    # create discrete colormap: this part is in most parts copy-pasted and has to be uptimized
    #cmap = colors.ListedColormap(['white', 'blue', 'green','darkorchid', 'orange', 'm', 'red', 'gold','k'])
    color=[]
    color.append("#FFFFFF")
    for i in range(len(gene_numbers)):
        r = lambda: random.randint(0,255)
        color.append('#%02X%02X%02X' % (r(),r(),r()))
    #cmap=plt.get_cmap(color)
    cmap = colors.ListedColormap(color)
    bounds=[-1,0.1]
    for i in gene_numbers:
        bounds.append(i+0.1)
    norm = colors.BoundaryNorm(bounds, cmap.N)

    fig, ax = plt.subplots()
    hm = ax.imshow(chunks, cmap=cmap, norm=norm, interpolation="nearest")

    y=[""]*(numb_rows+1)
    # draw gridlines #major ticks
    ax.grid(which='major', axis='both', linestyle='-', color='k', linewidth=2)
    ax.set_xticks(np.arange(-0.5, numb_cols, 1));
    ax.set_yticks(np.arange(-0.5, numb_rows, 1));
    ax.set_yticklabels(y);
    ax.set_xticklabels(y);
    ax = plt.gca();
    ax = plt.gca();

    #ax.set_xticklabels([""]*(numb_cols))
    #ax.set_yticklabels([""]*(numb_rows))

    letters = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]
    numbers =list(range(1,100,1))

    ax.set_yticklabels(letters[0:numb_rows],minor=True)
    ax.set_xticklabels(numbers[0:numb_cols],minor=True)

    # Minor ticks
    ax.set_xticks(np.arange(0, 24, 1), minor=True);
    ax.set_yticks(np.arange(0, 16, 1), minor=True);

    #add legend
    #patches=[mpatches.Patch(color=color[1], label=samples[0]),mpatches.Patch(color=color[11], label=samples[11-1])]
    patches = []
    for i in gene_numbers:
        patches.append(mpatches.Patch(color=color[i], label=genes[i-1]))

    #split legend into cols when longer than x axis (=15)
    banana=(len(genes)//15)+1
    #pear= banana-1
    #plt.legend(handles=patches, bbox_to_anchor=(1.185 + (pear*0.1735), 1.026),ncol=banana)
    plt.legend(loc='upper left',handles=patches,bbox_to_anchor=(1, 1.026),ncol=banana)


    plt.savefig("mysite/static/images/"+str(ids)+"_genes.png",bbox_inches='tight',dpi=300)
    return (str(ids)+"_genes.png", str(ids)+"_samples.png")


def plot_qpcr_data(qpcr_data={}):
    #give empty lists for parameters shown in graphs
    value = []
    error = []
    label = []
    files = []

    #loop through the sub-dictionaries (e.g. dictionary under key "Gene x"). For ech loop/each gene, a new graph depicting all samples is created.
    for v,w  in qpcr_data.items():
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
        plt.bar(left = np.arange(len(value)), height=value, yerr = error,align='center', tick_label = label, capsize = 5, color = color)        # plt.show()
        #save the plot
        plt.savefig("mysite/static/images/image"+str(v)+".png",bbox_inches='tight',dpi=100)
        files.append("image"+str(v)+".png")

        #reset parameters for next loop
        value = []
        error = []
        label = []
    return files

def pipet_scheme(ids, name, experiment, samples, genes):

    # wells_left = 384
    samples.append("water")
    well = []
    assignment_list = []
    d = {}

    if len(samples) == 0 or len(genes) == 0:
        wellsneeded = 0
        return("You did not enter any genes")

    else:
        wellsneeded = (len(genes)*(len(samples)*3))

    if wellsneeded > 384:
        return("Please reduce the amount of samples or genes")

    for i in ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P"]:
        for j in range(1,25):
            well.append(str(i+str(j)))

    for k in genes:
        for l in samples:
            assignment_list.append([k,l])
            assignment_list.append([k,l])
            assignment_list.append([k,l])

    #if len(assignment_list)<384:
    # assignment_list.extend(['bla','blub']*(384-len(assignment_list)))

    d = dict(zip(well, assignment_list))

    filename = str(ids)+"_"+experiment+".csv"

    with open("mysite/static/schemes/%s" % filename, 'w') as outfile:
        for k, v in d.items():
            outfile.write(str(k) + ',' + str(v[0]) + ',' + str(v[1]) + '\n')

    #with open('experiment.csv', 'w') as outfile:
    # writer = csv.writer(outfile)
    # for k, v in d.items():
    # writer.writerow([k]+ v )

    return filename


def combine_files(text, csv, hkg):

    txt_name = text.split(".")[0]
    csv_name = csv.split(".")[0]

    dCp = []
    dCperr = []
    RQ=[]
    RQmin = []
    RQmax = []
    Stdev = []

    results = pd.read_csv('mysite/static/uploads/%s' % text, sep="\t", header=0)
    experiment = pd.read_csv('mysite/static/schemes/%s' % csv, header = None)
    experiment.columns = ['Pos', 'Gene', 'Sample']

    Cp = results['Cp']
    experiment['Cp'] = Cp

    ex_m = experiment.groupby(['Sample', 'Gene'])['Cp'].mean().reset_index()
    ex_s = experiment.groupby(['Sample', 'Gene'], squeeze=True)['Cp'].sem().reset_index()

    ex_m['Sem']=ex_s['Cp']
    ex_m = ex_m.rename(columns={'Cp': 'Mean'})

    evaluate_df = ex_m

    experiment.to_csv('mysite/static/evaluations/%s_%s.csv' % (txt_name, csv_name), sep=",", header = True)

    df = evaluate_df

    for i in range(len(df)):
        if df.iloc[i]["Gene"]==hkg:
            target_sample = df.iloc[i]["Sample"]
            for j in range(len(df)):
                if df.iloc[j]["Sample"]==target_sample:
                    dcp = df.iloc[j]["Mean"]-df.iloc[i]["Mean"]
                    dCp.append(dcp)
                    RQ.append(2**(-(dcp)))

                    dcperr = (math.sqrt(df.iloc[j]["Sem"]**2+df.iloc[i]["Sem"]**2))
                    dCperr.append(dcperr)

                    rqmin = 2**(-(dcp+dcperr))
                    RQmin.append(rqmin)

                    rqmax = 2**(-(dcp-dcperr))
                    RQmax.append(rqmax)

                    Stdev.append(statistics.stdev([rqmin,rqmax]))

    df['dCp'] = dCp
    df['dCperr'] = dCperr
    df['RQ'] = RQ
    df['RQmin'] = RQmin
    df['RQmax'] = RQmax
    df['Stdev'] = Stdev

    df.to_csv('mysite/static/evaluations/%s_%s_evaluations.csv' % (txt_name, csv_name), sep=",", header = True)

    results = {}

    # unique_genes = set(df['Gene'])

    for i in range(len(df)):
        if df.iloc[i]["Gene"] not in results.keys() and df.iloc[i]["Gene"] != hkg:
            results[df.iloc[i]["Gene"]] = {}
            for j in range(len(df)):
                if df.iloc[j]["Sample"] not in results[df.iloc[i]["Gene"]].keys() and df.iloc[j]["Sample"] != 'water':
                    results[df.iloc[i]["Gene"]][df.iloc[j]["Sample"]] = [df.iloc[j]["RQ"], df.iloc[j]["Stdev"]]

    return("%s_%s_evaluations.csv" % (txt_name, csv_name), results)
