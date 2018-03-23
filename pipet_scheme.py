import pandas as pd
import math
import statistics


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
    #    assignment_list.extend(['bla','blub']*(384-len(assignment_list)))

    d = dict(zip(well, assignment_list))

    filename = str(ids)+"_"+experiment+".csv"

    with open("mysite/static/download/%s" % filename, 'w') as outfile:
        for k, v in d.items():
            outfile.write(str(k) + ',' + str(v[0]) + ',' + str(v[1]) + '\n')

    #with open('experiment.csv', 'w') as outfile:
    #    writer = csv.writer(outfile)
    #    for k, v in d.items():
    #        writer.writerow([k]+ v )

    return(filename, "Amount of wells needed: ", wellsneeded, d)


def combine_files(text, csv, hkg):

    txt_name = text.split(".")[0]
    csv_name = csv.split(".")[0]

    dCp = []
    dCperr = []
    RQ=[]
    RQmin = []
    RQmax = []
    Stdev = []

    results = pd.read_csv('static/upload/%s' % text, sep="\t", header=0)
    experiment = pd.read_csv('static/download/%s' % csv, header = None)
    experiment.columns = ['Pos', 'Gene', 'Sample']

    Cp = results['Cp']
    experiment['Cp'] = Cp

    ex_m = experiment.groupby(['Sample', 'Gene'])['Cp'].mean().reset_index()
    ex_s = experiment.groupby(['Sample', 'Gene'], squeeze=True)['Cp'].sem().reset_index()

    ex_m['Sem']=ex_s['Cp']
    ex_m = ex_m.rename(columns={'Cp': 'Mean'})

    evaluate_df = ex_m

    experiment.to_csv('./static/%s_%s.csv' % (txt_name, csv_name), sep=",", header = True)

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

    df.to_csv('./static/%s_%s_evaluations.csv' % (txt_name, csv_name), sep=",", header = True)

    results = {}

    # unique_genes = set(df['Gene'])

    for i in range(len(df)):
        if df.iloc[i]["Gene"] not in results.keys() and df.iloc[i]["Gene"] != hkg:
            results[df.iloc[i]["Gene"]] = {}
            for j in range(len(df)):
                if df.iloc[j]["Sample"] not in results[df.iloc[i]["Gene"]].keys() and df.iloc[j]["Sample"] != 'water':
                    results[df.iloc[i]["Gene"]][df.iloc[j]["Sample"]] = [df.iloc[j]["RQ"], df.iloc[j]["Stdev"]]

    return(df, results)


print(combine_files('qPCr_test.txt','5_bla.csv', 'y'))

