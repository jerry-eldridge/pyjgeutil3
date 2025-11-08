# Token processor and automaton interpreter

# [1] Microsoft Copilot, a large language model

def load_automaton(filename):
    transitions = {}
    with open(filename, 'r') as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) == 4 and parts[2] == '->':
                key = (parts[0], parts[1])
                transitions[key] = parts[3]
    return transitions

def run_automaton(tokens, transitions):
    state = 'START'
    for token in tokens:
        key = (state, token)
        if key not in transitions:
            print(f"Invalid transition "+\
                f"from {state} with token {token}")
        state = transitions[key]
    if state != 'HALT':
        print(f"Did not reach HALT "+\
                    f"state, ended at {state}")
        return False
    return True


count_BEGIN = 0
count_END = 0
def pop(tokens,values):
    global count_BEGIN, count_END
    assert(len(tokens)==len(values))
    if len(tokens) == 0 and len(values) == 0:
        return tokens,values,None,None
    tok = tokens[0] # x
    tokens = tokens[1:]
    val = values[0]
    if val == "BEGIN":
        count_BEGIN += 1
    if val == "END":
        count_END += 1
    values = values[1:]
    return tokens,values,tok,val

def boolean_flag(variables,var1,op1,val1):
    flag = False
    if op1 == "LT":
        flag = variables[var1] < val1
    elif op1 == "GT":
        flag = variables[var1] > val1
    elif op1 == "LE":
        flag = variables[var1] <= val1
    elif op1 == "GE":
        flag = variables[var1] >= val1
    elif op1 == "EQ":
        flag = variables[var1] == val1    
    return flag
def interpret(tokens,values,variables):
    while len(tokens) > 0:
        tokens,values,tok0,val0 = pop(tokens,values)
        #print(tok0,val0)
        if tok0 == 'WHILE':  # while body do
            # x < 10
            tokens,values,tok,val = pop(tokens,values)
            var1 = val
            tokens,values,tok,val = pop(tokens,values)
            op1 = val
            tokens,values,tok,val = pop(tokens,values)
            val1 = val
            tokens,values,tok,val = pop(tokens,values)
            # do
            tokens,values,tok,val = pop(tokens,values)
            tokens2 = []
            values2 = []
            while count_BEGIN > count_END:
                tokens2.append(tok)
                values2.append(val)
                tokens,values,tok,val = pop(tokens,values)
            maxcount = 1000 # limit while loop
            count = 0
            while True and count < maxcount :
                flag = boolean_flag(variables,\
                            var1,op1,val1)
                if not flag:
                    break
                variables = interpret(\
                    tokens2,values2,variables)
                count = count + 1
        elif tok0 == 'NAME':
            # pop assign
            # get var name
            A_LHS = val0
            tokens,values,tok,val = pop(tokens,values)
            if tok == 'ASSIGN':
                tokens,values,tok,val = pop(tokens,values)
                A_RHS = val
                tokens,values,tok,val = pop(tokens,values)
                op_RHS = val
                tokens,values,tok,val = pop(tokens,values)
                B_RHS = val
                variables[A_LHS] = \
                            variables[A_RHS] + \
                            float(B_RHS)
                # semicolon
                tokens,values,tok,val = pop(tokens,values)
        elif tok0 == 'PRINT':
            tokens,values,tok,val = pop(tokens,values)
            if tok == "NAME":
                A_VAR = val
                # pop assign
                print(f"{A_VAR} = "+\
                    f"'{variables[A_VAR]}'")
                # semicolon
                tokens,values,tok,val = \
                        pop(tokens,values)
            elif tok == "QUOTE":
                L = []
                tokens,values,tok2,val2 = \
                        pop(tokens,values)
                while tok2 != "QUOTE":
                    L.append(val2)
                    tokens,values,tok2,val2 = \
                        pop(tokens,values)
                s = " ".join(L)
                print(f"{s}")
                # semicolon
                tokens,values,tok,val = \
                        pop(tokens,values)
        elif tok0 == 'IF':
            # get then body
            # x < 10
            tokens,values,tok,val = pop(tokens,values)
            var1 = val
            tokens,values,tok,val = pop(tokens,values)
            op1 = val
            tokens,values,tok,val = pop(tokens,values)
            val1 = val
            # begin
            tokens,values,tok,val = pop(tokens,values)
            # first token
            tokens,values,tok,val = pop(tokens,values)
            tokens2 = []
            values2 = []
            while count_BEGIN > count_END:
                tokens2.append(tok)
                values2.append(val)
                tokens,values,tok,val = pop(tokens,values)
            # get else body
            tokens3 = []
            values3 = []
            # else
            tokens,values,tok,val = pop(tokens,values)
            # begin
            tokens,values,tok,val = pop(tokens,values)
            # first token
            tokens,values,tok,val = pop(tokens,values)
            while count_BEGIN > count_END:
                tokens3.append(tok)
                values3.append(val)
                tokens,values,tok,val = pop(tokens,values)            
            #

            flag = boolean_flag(variables,\
                            var1,op1,val1)

            if flag:
                variables = interpret(\
                    tokens2,values2,variables)
            else:
                variables = interpret(\
                    tokens3,values3,variables)
        elif tok0 == "FINISH":
            return variables
    return variables
