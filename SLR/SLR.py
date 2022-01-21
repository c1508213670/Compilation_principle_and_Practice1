import os
def create_table(tup):
    print("可行前缀DFA集合如下：")
    for i in range(len(tup[2])):
        print(i,end='\t')
        print(tup[2][i])
        print()
    print("DFA构建预测分析表如下：")
    print("\t",end=" ")
    for i in tup[1]:
        print(i,end='\t')

    print()
    for i in range(len(tup[0])):
        print(i,end='\t')
        for j in tup[0][i]:
            print(j,end='\t')
        print()
    print("对应归约集合如下：")
    print(tup[3])

def d_gram(lst):
    resls=[]
    for i in lst:
        temp=[]
        for j in range(len(i)):
            if j==0:
                temp.append(i[0])
                continue
            if i[j]=="|":
                resls.append(temp)
                temp=[]
                temp.append(i[0])
                temp.append('->')
            else:
                temp.append(i[j])
        resls.append(temp)
    return resls

def Fls(lst,FFls):
    res=[]
    for i in lst:
        for j in i:
            if j!='->' and j not in FFls and j not in res:
                res.append(j)
    return res

def ALLls(lst):
    res=[]
    start=lst[0][0]
    for i in lst:
        for j in i:
            if j!='->' and j not  in res and j!=start:
                res.append(j)
    return res

def m_contain(C,ls):
    res=-1
    for i in C:
        if ls in i:
            res=C.index(i)
    if res!=-1:
        return res
    else:
        return -1

def where_dot(lis,str):
    lst=[]
    FFls=[]
    with open(str,'r',encoding='utf8') as f2:
        a=f2.readlines()
    for i in a:
        ls=i.split()
        lst.append(ls)
        if ls[0] not in FFls:
            FFls.append(ls[0])
        lst=d_gram(lst)
    target=lis.index("·")
    if target==len(lis)-1:
        ll=lis[:]
        ll.pop()
        aa=lst.index(ll)
        return (3,lis[0],aa)
    elif lis[target+1] in FFls:
        return (2,lis[target+1])
    else:
        if lis[target+1]=='e':
            ll=lis[:]
            ll.remove("·")
            aa=lst.index(ll)
            return (3,lis[0],aa)
        return (1,lis[target+1])

def is_e(j,lis):
    target=j.index("·")
    if target!=len(j)-1:
        if j[target+1]=='e':
            ll=j[:]
            ll.remove("·")
            aa=lis.index(ll)
            return (1,ll[0],aa)
        else:
            return (0,1)
    else:
        return (0,1)
def J_l(lst,i):
    ls=lst[:]
    ls[i:i]="·"
    return ls

def X_b(lst):
    ls=[]
    a=0
    b=0
    for i in range(len(lst)):
        if lst[i]=="·":
            a=i
    b=a+1
    for  i in range(len(lst)):
        if i==a:
            ls.append(lst[b])
        elif i==b:
            ls.append(lst[a])
        else:
            ls.append(lst[i])
    return ls

def all_dollar_list(str):
    lst=[]
    FFls=[]
    Fls1=[]
    F=[]
    start=""
    with open(str,'r',encoding='utf8') as f2:
        a=f2.readlines()
    for i in a:
        ls=i.split()
        lst.append(ls)
        if ls[0] not in FFls:
            FFls.append(ls[0])
        lst=d_gram(lst)
    start=lst[0][0]
    sta=start
    lst=list(reversed(lst))
    start=start+'1'
    lst.append([start,"->",sta])
    lst=list(reversed(lst))
    FFls.append(start)
    Fls1=Fls(lst,FFls)
    for i in Fls1:
        if i !='e':
            F.append(i)
    F.append('$')
    for i in FFls:
        if i !=start:
            F.append(i)
    return F

def f_list(lst):
    ls=[]
    for i in lst:
        ls.append(i[0])
    return ls

def First(str):
    lst=[]
    resls=[]
    lcount=1
    FFls=[]
    lresls=[]
    with open(str,'r',encoding='utf8') as f2:
        a=f2.readlines()
    for i in a:
        ls=i.split()
        lst.append(ls)
        if ls[0] not in FFls:
            FFls.append(ls[0])
        lst=d_gram(lst)
    for i in lst:
        flag=-1
        mark=-1
        temp=[]
        for j in range(len(i)):
            if j==0:
                if  i[0] not in f_list(resls):
                    temp.append(i[0])
                    mark=-1
                    continue
                else:
                    for w in range(len(resls)):
                        if  resls[w][0]==i[0]:
                            mark=w
                            break
                    continue
            if i[j]=='->':
                flag=j
                continue

            if i[flag+1] not in FFls:
                if mark==-1:
                    t=[]
                    t.append(i[flag+1])
                    temp.append(t)
                    resls.append(temp)
                    break
                else:
                    if i[flag+1] not in resls[mark][1]:
                        resls[mark][1].append(i[flag+1])
                    break
            else:
                if mark==-1:
                    t=[]
                    temp.append(t)
                    resls.append(temp)
                    break
                else:
                    f=0
                    for r in resls:
                        if r[0]==i[flag+1]:
                            for rr in r[1]:
                                if rr not in resls[mark][1]:
                                    resls[mark][1].append(rr)
                        if 'e' not in r[1]:
                            f=0
                        else:
                            f=1
                    if f==1:
                        break
    while(lcount!=0):
        lcount=0
        lresls=resls[:]
        for i in lst:
            flag=-1
            mark=-1
            temp=[]
            for j in range(len(i)):
                if j==0:
                    if  i[0] not in f_list(resls):
                        temp.append(i[0])
                        mark=-1
                        continue
                    else:
                        for w in range(len(resls)):
                            if  resls[w][0]==i[0]:
                                mark=w
                                break
                        continue
                if i[j]=='->':
                    flag=j
                    continue
                if i[flag+1] not in FFls:
                    if mark==-1:
                        t=[]
                        t.append(i[flag+1])
                        temp.append(t)
                        resls.append(temp)
                        lcount=1
                        break
                    else:
                        if i[flag+1] not in resls[mark][1]:
                            resls[mark][1].append(i[flag+1])
                            lcount=1
                        break
                else:
                    if mark==-1:
                        t=[]
                        temp.append(t)
                        resls.append(temp)
                        lcount=1
                        break
                    else:
                        f=0
                        for r in resls:
                            if r[0]==i[flag+1]:
                                for rr in r[1]:
                                    if rr not in resls[mark][1]:
                                        resls[mark][1].append(rr)
                                        lcount=1
                            if 'e' not in r[1]:
                                f=0
                            else:
                                f=1
                        if f==1:
                            lcount=1
                            break
        if(lresls==resls):
            break
    return resls

def Follow(str):
    lst=[]
    FFls=[]
    firstls=[]
    resls=[]
    lcount=1
    with open(str,'r',encoding='utf8') as f2:
        a=f2.readlines()
    for i in a:
        ls=i.split()
        lst.append(ls)
        if ls[0] not in FFls:
            FFls.append(ls[0])
        lst=d_gram(lst)
    for i in range(len(FFls)):
        if i==0:
            resls.append([FFls[i],['$']])
        else:
            if  [FFls[i],[]] not in resls:
                resls.append([FFls[i],[]])
    firstls=First(str)
    while(lcount!=0):
        lcount=0
        for i in lst:
            flag=-1
            mark=0
            target=0
            a=0
            b=-1
            bls=[]
            s=""
            for j in range(len(resls)):
                if resls[j][0]==i[0]:
                    mark=j
                    break
            for j in range(len(i)):
                if i[j]=="|":
                    flag=j
                    continue
                else:
                    for h in range(len(i)-2-flag):
                        if a==0:
                            if i[len(i)-h-1] in FFls and b==-1:
                                for w in range(len(resls)):
                                    if resls[w][0]==i[len(i)-1-h]:
                                        for r in resls[mark][1]:
                                            if r not in resls[w][1]:
                                                if r !="e":
                                                    resls[w][1].append(r)
                                                    lcount=1
                                        if len(i)-h-1<len(i)-1:
                                            for ii in bls:
                                                for r in firstls[ii][1]:
                                                    if r not in resls[w][1]:
                                                        if r !="e":
                                                            resls[w][1].append(r)
                                                            lcount=1
                                        if 'e' not in firstls[w][1]:
                                            b=len(i)-h-1
                                            bls=[]
                                            target=w
                                            bls.append(target)
                                        else:
                                            target=w
                                            bls.append(target)
                                        break
                            elif i[len(i)-h-1] in FFls and b!=-1:
                                for w in range(len(resls)):
                                    if resls[w][0]==i[len(i)-1-h]:
                                        for ii in bls:
                                            for r in firstls[ii][1]:
                                                if r not in resls[w][1]:
                                                    if r !="e":
                                                        resls[w][1].append(r)
                                                        lcount=1
                                        if s!="":
                                            if s not in resls[w][1]:
                                                if s !="e":
                                                    resls[w][1].append(s)
                                                    lcount=1
                                        if 'e' in firstls[w][1]:
                                            target=w
                                            bls.append(target)
                                        else:
                                            b=len(i)-h-1
                                            bls=[]
                                            target=w
                                            bls.append(target)
                                            s=""
                            else:
                                a=1
                                s=i[len(i)-1-h]
                                target=0
                                b=0
                                bls=[]
                        else:
                            if i[len(i)-h-1] in FFls:
                                for w in range(len(resls)):
                                    if resls[w][0]==i[len(i)-1-h]:
                                        if s not in resls[w][1]:
                                            if s !="e":
                                                resls[w][1].append(s)
                                                lcount=1
                                        a=0
                                        if 'e' in firstls[w][1]:
                                            target=w
                                            bls.append(target)

                                        else:
                                            b=len(i)-h-1
                                            bls=[]
                                            target=w
                                            bls.append(target)
                                            s=""
                            else:
                                a=1
                                s=i[len(i)-1-h]
                                target=0
                                b=0
                                bls=[]
                    break
    return resls

def CLOSURE(I,str):
    J=[]
    J.append(I)
    flag=1
    lst=[]
    FFls=[]
    with open(str,'r',encoding='utf8') as f2:
        a=f2.readlines()
    for i in a:
        ls=i.split()
        lst.append(ls)
        if ls[0] not in FFls:
            FFls.append(ls[0])
        lst=d_gram(lst)
    while (flag):
        flag=0
        for i in J:
            temp=i.index("·")
            if temp==len(i)-1:
                continue
            else:
                str1=i[temp+1]
                if str1 in FFls:
                    for j in lst:
                        if j[0]==str1:
                            temp_ls=J_l(j,2)
                            if temp_ls not in J:
                                J.append(temp_ls)
                                flag=1
    return J

def GOTO(I,X,str):
    J=[]
    Jres0=[]
    Jres1=[]
    for i in I:
        temp=i.index("·")
        if temp==len(i)-1:
            continue
        else:
            if i[temp+1]==X and X!='e':
                temp_ls=X_b(i)
                J.append(temp_ls)
    for j in J:
        Jres0.append(CLOSURE(j,str))
    for i in Jres0:
        for j in i:
            if j not in Jres0:
                Jres1.append(j)
    return Jres1

def items(str):
    lst=[]
    FFls=[]
    Fls1=[]
    flag=1
    Allls=[]
    with open(str,'r',encoding='utf8') as f2:
        a=f2.readlines()
    for i in a:
        ls=i.split()
        lst.append(ls)
        if ls[0] not in FFls:
            FFls.append(ls[0])
        lst=d_gram(lst)
    start=lst[0][0]
    sta=start
    lst=list(reversed(lst))
    start=start+'1'
    lst.append([start,"->",sta])
    lst=list(reversed(lst))
    startls=lst[0]
    FFls.append(start)
    Fls1=Fls(lst,FFls)
    Allls=ALLls(lst)
    ls=CLOSURE(J_l(startls,2),str)
    C=[]

    C.append(ls)
    while(flag):
        flag=0
        for i in C:
            for j in Allls:
                if GOTO(i,j,str)!=[] and GOTO(i,j,str) not in C:
                    C.append(GOTO(i,j,str))
                    flag=1
    return C

def SLR_table(C,str1):
    lst=[]
    FFls=[]
    Fls1=[]
    Followls=Follow(str1)
    Allls=[]
    table=[]
    with open(str1,'r',encoding='utf8') as f2:
        a=f2.readlines()
    for i in a:
        ls=i.split()
        lst.append(ls)
        if ls[0] not in FFls:
            FFls.append(ls[0])
        lst=d_gram(lst)
    start=lst[0][0]
    sta=start
    lst=list(reversed(lst))
    start=start+'1'
    lst.append([start,"->",sta])
    lst=list(reversed(lst))
    FFls.append(start)
    Fls1=Fls(lst,FFls)
    Allls=all_dollar_list(str1)
    for j in range(len(C)):
        tem=[]
        for i in range(len(Allls)):
            tem.append("err")
            # print("err",end="\t")
        table.append(tem)
    for i in C:
        for j in Allls:
            rows=C.index(i)
            if j not in FFls:
                if GOTO(i,j,str1) in C:
                    col=Allls.index(j)
                    target=C.index(GOTO(i,j,str1))
                    table[rows][col]="s"+str(target)
            else:
                if GOTO(i,j,str1) in C:
                    col=Allls.index(j)
                    target=C.index(GOTO(i,j,str1))
                    table[rows][col]=str(target)
    for i in C:
        rows=C.index(i)
        for j in i:
            jtup=is_e(j,lst)
            if j[len(j)-1]=='·':
                temp=j[:]
                temp.pop()
                if temp!=lst[0]:
                    followls=[]
                    target=lst.index(temp)
                    for ii in Followls:
                        if temp[0]==ii[0]:
                            followls=ii[1]
                            break
                    for w in range(len(Allls)):
                        if Allls[w] in followls:
                            table[rows][w]="r"+str(target)

                else:
                    cols=Allls.index('$')
                    table[rows][cols]='acc'
            elif jtup[0]==1:
                target=jtup[2]
                followls=[]
                for ii in Followls:
                    if jtup[1]==ii[0]:
                        followls=ii[1]
                        break
                for w in range(len(Allls)):
                    if Allls[w] in followls:
                        table[rows][w]="r"+str(target)

    return table,Allls,C,lst,Fls1

def shift_reduction(tup,s):
    lst=tup[3]
    C=tup[2]
    All=tup[1]
    table=tup[0]
    s=s.split()
    s.append('$')
    s=list(reversed(s))
    resls=[]
    stack=[0]
    fflag=0
    while(s!=[]):
        temp=s[len(s)-1]
        stack_end=int(stack[len(stack)-1])
        ind=All.index(temp)
        do=table[stack_end][ind]
        dols=list(do)
        target=0
        if do=='acc':
            fflag=1
            break
        elif do=='err':
            fflag=0
            break
        else:
            target=int("".join(dols[1:]))
            if dols[0]=='s':
                stack.append(temp)
                s.pop()
                stack.append(target)
            if dols[0]=='r':
                t=int("".join(dols[1:]))
                force_flag=0
                for i in range(len(stack)):
                    flag=stack[len(stack)-1]
                    if force_flag==len(lst[t])-2:
                        break

                    else:
                        if lst[t][len(lst[t])-1]=="e":
                            if len(stack)!=1:
                                stack.pop()
                            force_flag+=1
                        else:
                            if len(stack)!=1:
                                stack.pop()
                            if len(stack)!=1:
                                stack.pop()
                            force_flag+=1
                tt=lst[target][0]
                stack.append(tt)
                rows=int(stack[len(stack)-2])
                col=All.index(tt)
                stack.append(table[rows][col])
                resls.append(lst[target])
        print(stack,s,resls)
    if fflag==1:
        return  resls
    else:
        print('error!')
        return []

def creat_resls(i,Fls,lst):
    res=[]
    for j in range(len(lst[i[0]])):
        if j>=2:
            res.append("[")
            res.append(lst[i[0]][j])
            res.append("]")
    res1=res[:]
    for ii in range(len(res1)):
        temp=len(res1)-1-ii
        if res[temp] in ["[","]"]:
            continue
        if res[temp] in Fls:
            continue
        else:
            i[0]+=1
            if len(res)-len(res1)!=0:
                temp=temp-(len(res)-len(res1))+1
            res.insert(temp+1,creat_resls(i,Fls,lst))
    return res

def creat_res(lst):
    res=""
    for i in lst:
        if isinstance(i,str):
            res=res+i
        else:
            res=res+creat_res(i)
    return res


print("请输入文法文件目录：(如果不存在默认为SLR.py文件同目录下的grammar.txt，如果grammar.txt不存在则会自动创建)：")
print('''系统自动创建的grammar.txt默认文法为：["E -> E + T","E -> T","T -> T * F","T -> F","F -> ( E )","F -> id"]''')
str0=input()
if os.path.exists(str0):
    str0=str0
else:
    str0='grammar.txt'
if os.path.exists('grammar.txt'):
    str0='grammar.txt'
else:
    with open('grammar.txt','w',encoding='utf8') as f:
        lls=["E -> E + T","E -> T","T -> T * F","T -> F","F -> ( E )","F -> id"]
        for ii in lls:
            f.write(ii+"\n")
    f.close()

r=items(str0)
tup=SLR_table(r,str0)
create_table(tup)
print("请输入需要语法分析的字符串(字符间以空格隔开)：")
s=input()
print("移进-归约过程如下：")
re=shift_reduction(tup,s)
re.append([re[len(re)-1][0],'->',re[len(re)-1][0]])
re=list(reversed(re))
rels=creat_resls([0],tup[4],re)
res=creat_res(rels)
print("结果集如下：")
print(res)
with open('result.txt','w',encoding='utf8') as f1:
    f1.write(res)
f1.close()