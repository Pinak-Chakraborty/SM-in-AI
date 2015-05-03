# This module takes Tokenized Sentence and retuns search chunk based on some rules
# This contains a lot of heck - which can be easily corrected 
def Search_Chunk(tokenizedSentence):
    listsent = ""
    space = " "
    firstVBZ = False
    VBZappend = ""
    Qtype = 0

    for tokentuple in tokenizedSentence: 
        #print (tokentuple[0], tokentuple[1])
        
        if tokentuple[0].lower() in ("where"):
            #print("location question")
            Qtype = 1 #location
            
        if tokentuple[0].lower() in ("when"):
            #print("date time question")
            Qtype = 2 #date time
            
        if tokentuple[1] not in ("WP", "WDT", "WRB", "."):
            if tokentuple[0] not in ("are", "is", "was", "were","will", "shall" \
                                     "have", "has", "had" \
                                     "here", "there", \
                                     "do", "does", "did"):

                if Qtype == 1 and tokentuple[0] in ("location", "located"):
                    continue

                if Qtype == 2 and tokentuple[0] in ("date", "time"):
                    continue

                listsent = listsent + space + tokentuple[0]

        if tokentuple[0] in ("is","are", "were", "has", "have", "had") \
           and firstVBZ == False:
            firstVBZ = True
            VBZappend = tokentuple[0]
            
    listsent = listsent + space + VBZappend 
    
    if Qtype == 1:
        listsent = listsent + space + "located"
    if Qtype == 2:
        listsent = listsent + space + "date time"

    return (str(listsent))

