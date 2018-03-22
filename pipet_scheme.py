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