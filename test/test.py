def create_target(str):
    orglist=[]
    with open(str,'r',encoding='utf8') as f:
        orglist=f.readlines()
    terminal={}
    terminal=set(terminal)
    start_symbol=""
    rules_prob={}
    rules_prob=dict(rules_prob)
    non_terminal={}
    non_terminal=set(non_terminal)
    for i in range(len(orglist)):
        temp=orglist[i].split()
        if i ==0:
            start_symbol=temp[0]
        if len(temp)-2>2:
            t=(temp[2],temp[3])
            t={t:temp[4]}
            tt=rules_prob.get(temp[0])
            if tt:
                tt.update(t)
                rules_prob[temp[0]]=tt
            else:
                rules_prob[temp[0]]=t
        else:
            t={temp[2]:temp[3]}
            tt=rules_prob.get(temp[0])
            if tt:
                tt.update(t)
                rules_prob[temp[0]]=tt
            else:
                rules_prob[temp[0]]=t

        for j in range(len(temp)):
            if j==0:
                non_terminal.add(temp[j])
            if j>=2:
                if temp[j].islower() :
                    terminal.add(temp[j])
    return start_symbol,terminal,non_terminal,rules_prob

temp=create_target('text.txt')
for i in temp:
    print(i)