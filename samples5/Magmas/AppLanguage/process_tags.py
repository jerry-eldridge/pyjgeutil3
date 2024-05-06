from copy import deepcopy

def process_tags_helper(tags):
    L = []
    for tup in tags:
        toks = tup[1].split('/')
        s = toks[0]
        t = toks[1]
        L.append(s)
    return ''.join(L)

def process_tags(tags, debug=False):
    x = []
    f = []
    count = 0
    counts = 0
    for tup in tags:
        toks = tup[1].split('/')
        s = toks[0]
        t = toks[1]
        if t == 'Lparen':
            count = count + 1
        if t == 'Rparen':
            count = count - 1
        if count == 0 and t in ['Lparen','Rparen']:
            counts = counts + 1
    if counts == 0:
        if debug:
            print(f"0: x = {tags}")
            q = input(f"Enter 'q' to quit> ")
            if q == 'q':
                1/0
                return
            else:
                print(f"0: x = {tags}")
        return process_tags_helper(tags)
    if counts == 1:
        c = 0
        for tup in tags:
            toks = tup[1].split('/')
            s = toks[0]
            t = toks[1]
            if t == 'Lparen':
                break
            c = c + 1
        f = tags[0:c]
        x = tags[c+1:-1]
        if debug:
            q = input(f"Enter 'q' to quit> ")
            if q == 'q':
                1/0
                return
            else:
                print(f"1: f = {f}")
            q = input(f"Enter 'q' to quit> ")
            if q == 'q':
                1/0
                return
            else:
                print(f"1: x = {x}")        
        return [process_tags(f,debug),
                process_tags(x,debug)]
    if counts == 2:
        count2 = 0
        counts2 = 0
        c = 0
        for tup in tags:
            toks = tup[1].split('/')
            s = toks[0]
            t = toks[1]
            if t == 'Lparen':
                count2 = count2 + 1
            if t == 'Rparen':
                count2 = count2 - 1
            if count2 == 0 and t in ['Lparen','Rparen']:
                counts2 = counts2 + 1
            if (t in ['Rparen']) and counts2 == 1 and\
               count2 == 0:
                break
            c = c + 1
        f = tags[0:c+1]
        x = tags[c+2:-1]
        if debug:
            q = input(f"Enter 'q' to quit> ")
            if q == 'q':
                1/0
                return
            else:
                print(f"2: f = {f}")
            q = input(f"Enter 'q' to quit> ")
            if q == 'q':
                1/0
                return
            else:
                print(f"2: x = {x}")
        return [process_tags(f,debug),
                process_tags(x,debug)]        
    return None

