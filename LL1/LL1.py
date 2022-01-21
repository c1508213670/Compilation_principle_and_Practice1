def getnext(ls):
    a=ls[0]
    del(ls[0])
    return a

def add_res(res,str):
    temp=res
    res=res.rstrip("]")
    res+=str
    return res

def E(a,result):
    result=add_res(result,"[E]")
    res=T(a,result)
    result=res[0]
    a=res[1]

    res=E1(a,result)
    result=res[0]
    a=res[1]

    return result+"] ",a

def T(a,result):
    result=add_res(result,"[T]")

    res=F(a,result)
    result=res[0]
    a=res[1]

    res=T1(a,result)
    result=res[0]
    a=res[1]

    return result+"] ",a

def E1(a,result):
    result=add_res(result,"[E']")

    if a=="+":
        result=add_res(result,"[+] ")
        a=getnext(ls)
        res=T(a,result)
        result=res[0]
        a=res[1]

        res=E1(a,result)
        result=res[0]
        a=res[1]

        return result+"] ",a

    else:
        if a==")" or a=="$":
                result=add_res(result,"[e]")
                return result+"] ",a
        else:
            print("Input error!")

def F(a,result):
    result=add_res(result,"[F]")
    if a=="(":
        result=add_res(result,"[(] ")
        a=getnext(ls)
        res=E(a,result)
        result=res[0]
        a=res[1]
        if a==")":
            result=add_res(result,"[)] ")
            a=getnext(ls)
            return result+"] ",a
        else:
            print("Input error!")
    else:
        if a=="id":
            result=add_res(result,"[id] ")
            a=getnext(ls)
            return  result+"] ",a
        else:
            print("Input error!")

def T1(a,result):
    result=add_res(result,"[T']")
    if a=="*":
        result=add_res(result,"[*] ")
        a=getnext(ls)
        res=F(a,result)
        result=res[0]
        a=res[1]
        res=T1(a,result)
        result=res[0]
        a=res[1]

        return result+"] ",a
    else:
        if a=="+" or a==")" or a=="$":
                result=add_res(result,"[e]")
                return result+"] ",a
        else:
            print("Input error!")







a=input()
ls=a.split()
ls.append("$")
result=" "
res=E(getnext(ls),result)
result=res[0]
print(result)

# res="[E[T[F[id]] ]]"
# res=add_res(res,"[F id]")
# print(res)