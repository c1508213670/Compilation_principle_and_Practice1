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
            t={t:eval(temp[4])}
            tt=rules_prob.get(temp[0])
            if tt:
                tt.update(t)
                rules_prob[temp[0]]=tt
            else:
                rules_prob[temp[0]]=t
        else:
            t={temp[2]:eval(temp[3])}
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
start_symbol=temp[0]
terminal=temp[1]
non_terminal=temp[2]
rules_prob=temp[3]

print("请输入要构建统计语法书的句子：")
sentence=input()
word_list = sentence.split()
best_path = [[{} for x in range(len(word_list))] for x in range(len(word_list))]

# 初始化
for i in range(len(word_list)):  # 下标为0开始
    for j in range(len(word_list)):
        for x in non_terminal:  # 初始化每个字典，每个语法规则概率及路径为None，避免溢出和空指针
            best_path[i][j][x] = {'prob': 0.0, 'path': {'split': None, 'rule': None}}

###叶节点的计算
# 填叶结点，计算得到每个单词所有语法组成的概率
for i in range(len(word_list)):  # 下标为0开始
    for x in non_terminal:  # 遍历非终端符，找到并计算此条非终端-终端语法的概率
        if word_list[i] in rules_prob[x].keys():
            best_path[i][i][x]['prob'] = rules_prob[x][word_list[i]]  # 保存概率
            best_path[i][i][x]['path'] = {'split': None, 'rule': word_list[i]}  # 保存路径
            # 生成新的语法需要加入
            for y in non_terminal:
                if x in rules_prob[y].keys():
                    best_path[i][i][y]['prob'] = rules_prob[x][word_list[i]] * rules_prob[y][x]
                    best_path[i][i][y]['path'] = {'split': i, 'rule': x}

for l in range(1, len(word_list)):
    # 该层结点个数
    for i in range(len(word_list) - l):  # 第一层：0,1,2
        j = i + l  # 处理第二层结点，（0,j=1）,(1,2),(2,3)   1=0+1,2=1+1.3=2+1
        for x in non_terminal:  # 获取每个非终端符
            tmp_best_x = {'prob': 0, 'path': None}

            for key, value in rules_prob[x].items():  # 遍历该非终端符所有语法规则
                if key[0] not in non_terminal:
                    break
                # 计算产生的分裂点概率，保留最大概率
                for s in range(i, j):  # 第一个位置可分裂一个（0,0--1,1)
                    # for A in best_path[i][s]
                    if len(key) == 2:
                        tmp_prob = value * best_path[i][s][key[0]]['prob'] * best_path[s + 1][j][key[1]]['prob']
                    else:
                        tmp_prob = value * best_path[i][s][key[0]]['prob'] * 0
                    if tmp_prob > tmp_best_x['prob']:
                        tmp_best_x['prob'] = tmp_prob
                        tmp_best_x['path'] = {'split': s, 'rule': key}  # 保存分裂点和生成的可用规则
            best_path[i][j][x] = tmp_best_x  # 得到一个规则中最大概率

            #print("score[", i, "][", j, "]:", best_path[i][j])
best_path = best_path


lst=[]
def back(best_path, left, right, root, ind=0):
    node = best_path[left][right][root]
    if node['path']['split'] is not None:  # 判断是否存在分裂点，值为下标
        print(ind,'\t' * ind, (root,node['prob']))  # self.rules_prob[root].get(node['path']['rule']
        lst.append("["+root)

        # 递归调用
        if len(node['path']['rule']) == 2:  # 如果规则为二元，递归调用左子树、右子树，如 NP-->NP NP
            back(best_path, left, node['path']['split'], node['path']['rule'][0], ind + 1)  # 左子树
            lst.append("]")
            back(best_path, node['path']['split'] + 1, right, node['path']['rule'][1], ind + 1)  # 右子树
            lst.append("]")
        else:  # 否则，只递归左子树,如 NP-->N
            back(best_path, left, node['path']['split'], node['path']['rule'][0], ind + 1)
            lst.append("]")
    else:
        print(ind,'\t' * ind, (root,node['prob']))
        lst.append("["+root)
        print(ind+1,'\t' * (ind+1), node['path']['rule'])
        lst.append("["+node['path']['rule']+"]")



back(best_path,0,3,start_symbol)
lst.append("]")
rr="".join(lst)
print(rr)