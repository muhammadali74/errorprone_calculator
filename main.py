
from fractions import Fraction
from math import gcd


def floaterror(statement):
    space_indexes = []
    rec_statement = ""
    for j in range(len(statement)):
        if statement[j] == " ":
            space_indexes.append(j)
    for k in range(len(statement)):
        if k in space_indexes:
            pass
        else:
            rec_statement += statement[k]
    return list(rec_statement)


def solver(stat):
    count = 0
    while count < len(stat):
        if (stat[count] == '+' or stat[count] == '-') and (stat[count+1] == '+' or stat[count+1] == '-'):
            x = stat[count]+'1'
            y = stat[count+1]+'1'
            oper = str(int(x) * int(y))
            stat[count] = '+' if oper[0] == '1' else oper[0]
            del stat[count+1]
            # count-=1
        else:
            count += 1
    last_open = []
    last_closed = 0
    tbd = []
    for i in range(len(stat)):
        if stat[i] == '(':
            last_open.append(i)
        elif stat[i] == ')':
            last_closed = i
            if stat[last_open[-1]-1] == '-':
                if stat[last_open[-1]+1] == '+':
                    tbd.append(last_open[-1]+1)
                elif stat[last_open[-1]+1] == '-':
                    tbd.append(last_open[-1]-1)
                for j in range(last_open[-1], last_closed):
                    if stat[j] == '+' and (stat[j-1] != '*' and stat[j-1] != '/'):
                        stat[j] = '-'
                    elif stat[j] == '-' and (stat[j-1] != '*' and stat[j-1] != '/'):
                        stat[j] = '+'
                tbd.append(last_open[-1])
                tbd.append(last_closed)
                del last_open[-1]
            elif stat[last_open[-1]-1] == '+':
                if stat[last_open[-1]+1] == '+' or stat[last_open[-1]+1] == '-':
                    tbd.append(last_open[-1]-1)
                tbd.append(last_open[-1])
                tbd.append(last_closed)
                del last_open[-1]
            else:
                pass
    # print(tbd)
    for q in sorted(list(set(tbd)))[::-1]:
        print(q)
        del stat[q]

    newnum = True
    while newnum:
        for _ in range(len(stat)):
            if stat[_] == '.':
                fwd = _ +1
                rws = _ - 1
                while stat[rws].isnumeric() == True and rws >= 0:
                    rws -= 1
                while stat[fwd].isnumeric() == True:
                    if fwd == len(stat)-1:
                        fwd += 1
                        break
                    else:
                        fwd += 1
                dec = "".join(stat[rws+1:fwd])
                print(rws, fwd)
                frac = str(Fraction(dec))
                frac = list(frac)
                # frac = '(' + frac + ')'
                del stat[rws+1:fwd]
                for l in range(0, len(frac)):

                    stat.insert(rws+1+l, frac[l])
                break
            elif _ == len(stat)-1:
                newnum = False

# y = floaterror(x)
# print(y)
# solver(y)
# print(y)


def LCMofArray(a):
    numert = []
    deno = []
    for i in range(len(a)):
        numden = {'*': 1, '/': 1}
        oper = ['*']
        tempnum = ''
        iter = 0
        if a[i][0] == '-':
            tempnum = '-'
            iter = 1
        for j in range(iter, len(a[i])):
            if a[i][j] == '*' or a[i][j] == '/':
                numden[oper.pop()] *= int(tempnum)
                oper.append(a[i][j])
                tempnum = ''

            else:
                tempnum += a[i][j]
        numden[oper.pop()] *= int(tempnum)
        # newarr.append(str(numden['*']) + '/' + str(numden['/']))
        numert.append(numden['*'])
        deno.append(numden['/'])
        print(numden)

    lcm = deno[0]
    for i in range(1, len(deno)):
        lcm = lcm*deno[i]//gcd(lcm, deno[i])
    for k in range(len(deno)):
        numert[k] = numert[k] * (lcm//deno[k])

    return lcm, numert


def arranger(stat):
    poslist = []
    neglist = []
    other = []
    tempnum = ""
    lastchar = ['+']
    for i in range(len(stat)-1, -1, -1):
        if stat[i] == '+' and stat[i-1] != '*' and stat[i-1] != '/':
            if lastchar[-1] == '+' or lastchar[-1] == '-':
                poslist.append(int(tempnum))
                # print(i)
            else:
                other.append(tempnum)
            tempnum = ""
            lastchar.append('+')
        elif stat[i] == '-' and stat[i-1] != '*' and stat[i-1] != '/':
            if lastchar[-1] == '+' or lastchar[-1] == '-':
                neglist.append(int('-'+tempnum))
                # print(i)
            else:
                other.append('-'+tempnum)
            tempnum = ""
            lastchar.append('-')
        elif stat[i] == '*' or stat[i] == '/':
            lastchar.append('*')
            tempnum = stat[i] + tempnum

        else:
            tempnum = stat[i] + tempnum
        # print(tempnum, poslist, neglist, lastchar)
    if tempnum.isnumeric() and (lastchar[-1] == '+' or lastchar[-1] == '-'):
        poslist.append(int(tempnum))
    else:
        other.append(tempnum)

    suum = sum(poslist) + sum(neglist)
    other.append(str(suum))

    # return suum, poslist, neglist, other, LCMofArray(other)
    simp = LCMofArray(other)
    simp2 = str(sum(simp[1])) + '/' + str(simp[0])
    ans = eval(simp2)
    return simp2, ans


def main(x):
    y = floaterror(x)
    solver(y)

    recurse = True
    while recurse:
        open = -2
        close = 0
        for i in range(len(y)):
            if y[i] == '(':
                open = i
            elif y[i] == ')':
                close = i
                subprob = arranger(y[open+1:close])
                del y[open:close+1]
                s = list(subprob[0])
                for w in range(len(s)):
                    y.insert(open+w, s[w])
                break
        if open == -2:
            recurse = False
        print(y)
    return arranger(y)


# print(arranger(y))
# x = "34*(38-(56/2-(5+3)+(0.55/3/5 - 0.1)))"
x = "1+(1/10000)-(1-1/10000)"
# x = '1.2-0.8'
# x = " 1-(5/350 + -1/56) "
# x = "1.2-1.0"
print(main(x))
