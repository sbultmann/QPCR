def make_plate(ids, samples=[],genes=[]):

    import matplotlib.pyplot as plt
    from matplotlib import colors
    import numpy as np
    import matplotlib.patches as mpatches
    import random

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