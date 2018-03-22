def reverse_complement(sequence):
    from datetime import datetime
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    revseq = sequence[::-1]
    basepairs = {"A":"T", "T":"A", "C":"G", "G":"C"}
    rev_seq = ""
    if sequence == "":
        return "Q"
    for i in revseq.upper():
        if i not in basepairs:
            return "Q"
        else:
            rev_seq = rev_seq + basepairs[i]

    gc_cont=(rev_seq.upper().count("C")+rev_seq.upper().count("G"))/len(rev_seq)
    return(sequence.upper(),rev_seq, gc_cont,now)

