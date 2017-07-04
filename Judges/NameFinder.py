#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Ryan Hübert
# Department of Political Science
# University of California, Davis

"""
A set of tools to identify names in strings from predefined list.
"""

import re

def NameFinder(namedict,string,subset=None,namekeys=("First Name","Middle Name","Last Name")):
    bl = '(?:^|$|[^A-z])'
    string = string.upper()
    string = re.sub('`',"'",string)
    string = re.sub("[\.]"," ",string)
    string = re.sub("  +"," ",string)

    subset = namedict.keys() if subset == None else subset
    
    allmatches = {}
    for k in subset:
        ln = re.sub("[\.]"," ",namedict[k][namekeys[2]].upper().strip())
        ln = re.sub("  +"," ",ln)
        if not re.search(bl+ln+bl,string) or ln == "":
            continue
        fn = namedict[k][namekeys[0]].upper().strip()
        fi = namedict[k][namekeys[0]].upper()[0].strip()
        mn = namedict[k][namekeys[1]].upper().strip()
        mi = namedict[k][namekeys[1]].upper()[0].strip()
        
        # First name first
        name_string = re.findall("([^,;:]{,19}"+bl+ln+")"+bl,string)
        c = 0
        for n in name_string:
            c += 1
            matches = []
            if re.search(bl+fn+bl+mn+bl+ln+bl,n):
                matches.append((1,re.findall(bl+"("+fn+bl+mn+bl+ln+")"+bl,n)[0],k))
            elif re.search(bl+fn+bl+mi+bl+ln+bl,n):
                matches.append((2,re.findall(bl+"("+fn+bl+mi+bl+ln+")"+bl,n)[0],k))
            elif re.search(bl+fi+bl+mn+bl+ln+bl,n):
                matches.append((3,re.findall(bl+"("+fi+bl+mn+bl+ln+")"+bl,n)[0],k))
            elif re.search(bl+fi+bl+mi+bl+ln+bl,n):
                matches.append((4,re.findall(bl+"("+fi+bl+mi+bl+ln+")"+bl,n)[0],k))
            elif re.search(bl+fn+" [A-Z]"+bl+ln+bl,n):
                matches.append((5,re.findall(bl+"("+fn+" [A-Z]"+bl+ln+")"+bl,n)[0],k))
            elif re.search(bl+fn+bl+ln+bl,n) and fn != '':
                matches.append((6,re.findall(bl+"("+fn+bl+ln+")"+bl,n)[0],k))
            elif re.search(bl+mn+bl+ln+bl,n) and mn != '':
                matches.append((7,re.findall(bl+"("+mn+bl+ln+")"+bl,n)[0],k))
            elif re.search("(?:JUDGE|JUSTICE)"+bl+ln+bl,n):
                matches.append((8,re.findall(bl+"("+ln+")"+bl,n)[0],k))
            elif re.search(bl+fi+bl+ln+bl,n) and fn != '':
                matches.append((9,re.findall(bl+"("+fi+bl+ln+")"+bl,n)[0],k))
            elif re.search(bl+mi+bl+ln+bl,n) and mn != '':
                matches.append((10,re.findall(bl+"("+mi+bl+ln+")"+bl,n)[0],k))
            else:
                matches.append((11,re.findall(bl+"("+ln+")"+bl,n)[0],k))

            if matches != [] and namedict[k][namekeys[2]].upper()+'-'+str(c) not in allmatches:
                allmatches[namedict[k][namekeys[2]].upper()+'-'+str(c)] = matches
            elif matches != [] and namedict[k][namekeys[2]].upper()+'-'+str(c) in allmatches:
                allmatches[namedict[k][namekeys[2]].upper()+'-'+str(c)].extend(matches)

        # Last name first
        #name_string = re.findall(ln+bl+".{,19}",string)
    
    # This takes the "best" match identified for a given last name
    allmatches = {k: list(filter(None,[y if y[0] == min([z[0] for z in allmatches[k]]) else '' for y in allmatches[k]])) for k in allmatches}

    # This removes faulty matches -- e.g., matching judges with last name 
    # THOMAS to string "KEVIN THOMAS DUFFY" (THOMAS is middle name here)
    collapse = [y for x in allmatches for y in allmatches[x]]    
    toreturn = []
    for c1 in collapse:
        tr = 1
        for c2 in collapse:
            if c1 != c2 and re.search(c1[1],c2[1]) and len(c1[1]) < len(c2[1]):
                tr = 0
        if tr == 1:
            toreturn.append(c1[1:])
            
    for k in list(allmatches.keys()):
        allmatches[k] = list(filter(None,[x[1:] if x[1:] in toreturn else '' for x in allmatches[k]]))
        if allmatches[k] == []:
            del allmatches[k]  
    d2 = {tuple(v): k for k, v in allmatches.items()}
    allmatches = {v: list(set(list(k))) for k, v in d2.items()}
    return(allmatches)