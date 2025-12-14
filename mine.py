import random
from colorama import Fore
import time
import subprocess
ships=[3]
bsize=int(6)
targset=[(x,y) for x in range(bsize) for y in range(bsize)]

def randomboard(bs,sh):
    rbord=[]
    for x in range(bs):
        rbord.append([])
        for y in range(bs):
            rbord[x].append('* ')
    for ln in sh:
        xr=random.choice(range(bs))
        yr=random.choice(range(bs))
        while rbord[xr][yr]=='s':
            xr=random.choice(range(bs))
            yr=random.choice(range(bs))
        dcho=['u','l','d','r']
        chdone=0
        while not chdone:
            ch=random.choice(dcho)
            match ch:
                case 'u':
                    lnch=1 if xr-ln+1>=0 else 0
                    ovch=1
                    if lnch:
                        for xcheck in range(ln):
                            ovch*=(rbord[xr-xcheck][yr]=='* ')
                case 'd':
                    lnch=1 if xr+ln<=bs else 0
                    ovch=1
                    if lnch:
                        for xcheck in range(ln):
                            ovch*=(rbord[xr+xcheck][yr]=='* ')
                case 'r':
                    lnch=1 if yr+ln<=bs else 0
                    ovch=1
                    if lnch:
                        for ycheck in range(ln):
                            ovch*=(rbord[xr][yr+ycheck]=='* ')
                case 'l':
                    lnch=1 if yr-ln+1>=0 else 0
                    ovch=1
                    if lnch:
                        for ycheck in range(ln):
                            ovch*=(rbord[xr][yr-ycheck]=='* ')
            chdone=lnch and ovch
        match ch:
            case 'u':
                for xcheck in range(ln):
                    rbord[xr-xcheck][yr]='s '
            case 'd':
                for xcheck in range(ln):
                    rbord[xr+xcheck][yr]='s '
            case 'l':
                for ycheck in range(ln):
                    rbord[xr][yr-ycheck]='s '
            case 'r':
                for ycheck in range(ln):
                    rbord[xr][yr+ycheck]='s '
    return rbord

def setuboard(bs,sh):
    rbord=[]
    for x in range(bs):
        rbord.append([])
        for y in range(bs):
            rbord[x].append('* ')
    disp(rbord,'set user')
    for ln in sh:
        print('setting for ship length:',ln)
        xr=int(input('row num? '))
        yr=int(input('col num? '))
        while rbord[xr][yr]=='s':
            xr=int(input('row num? '))
            yr=int(input('col num? '))
        dcho=['u','l','d','r']
        chdone=0
        while not bool(chdone):
            ch=input('which dir?(u,d,l,r) ')
            global lnch
            match ch:
                case 'u':
                    lnch=1 if xr-ln+1>=0 else 0
                    ovch=1
                    if lnch:
                        for xcheck in range(ln):
                            ovch*=(rbord[xr-xcheck][yr]=='* ')
                case 'd':
                    lnch=1 if xr+ln<=bs else 0
                    ovch=1
                    if lnch:
                        for xcheck in range(ln):
                            ovch*=(rbord[xr+xcheck][yr]=='* ')
                case 'r':
                    lnch=1 if yr+ln<=bs else 0
                    ovch=1
                    if lnch:
                        for ycheck in range(ln):
                            ovch*=(rbord[xr][yr+ycheck]=='* ')
                case 'l':
                    lnch=1 if yr-ln+1>=0 else 0
                    ovch=1
                    if lnch:
                        for ycheck in range(ln):
                            ovch*=(rbord[xr][yr-ycheck]=='* ')
                case _:
                    lnch=0
                    ovch=0
            chdone=bool(lnch) and bool(ovch)
        match ch:
            case 'u':
                for xcheck in range(ln):
                    rbord[xr-xcheck][yr]='s '
            case 'd':
                for xcheck in range(ln):
                    rbord[xr+xcheck][yr]='s '
            case 'l':
                for ycheck in range(ln):
                    rbord[xr][yr-ycheck]='s '
            case 'r':
                for ycheck in range(ln):
                    rbord[xr][yr+ycheck]='s '
        disp(rbord,'set user')
    print('-'*4*bsize)
    return rbord

def disp(brd,txt):
    print('-'*((3*len(brd)+3-len(txt))//2),txt,'-'*((3*len(brd)+3-len(txt))//2),sep='')
    print(end='   ')
    for n in range(len(brd)):
        print(n,end='  ')
    print()
    m=0
    for x in range(len(brd)):
        print(m,end='  ')
        m+=1
        for y in range(len(brd[0])):
            if brd[x][y]=='x ':
                print(Fore.RED+brd[x][y]+Fore.RESET,end=' ')
            elif brd[x][y]=='* ':
                print(Fore.LIGHTBLUE_EX+brd[x][y]+Fore.RESET,end=' ')
            elif brd[x][y]=='s ':
                print(Fore.GREEN+brd[x][y]+Fore.RESET,end=' ')
            elif brd[x][y]=='0 ':
                print(Fore.LIGHTYELLOW_EX+brd[x][y]+Fore.RESET,end=' ')
            else:
                print(brd[x][y],end=' ')
        print()
    print()

def uhit(brd):
    xhit=int(input('row number?  '))
    yhit=int(input('col number?  '))
    if (0<=xhit<=(bsize-1) and
         0<=yhit<=(bsize-1) ):
        if brd[xhit][yhit]=='* ':
            brd[xhit][yhit]='0 '
            print('you MISS')
        elif brd[xhit][yhit]=='s ':
            brd[xhit][yhit]='x '
            print('you HIT !!')
        elif brd[xhit][yhit]in('x ','0 '):

            print('coord already hit...enter different coord ')
            uhit(brd)
    else:
        print('enter coord in range! ')
        return uhit(brd)

def aihit(brd):
    global lastsuchit, posthit
    if lastsuchit:
        match posthit:
            case 1:
                if (lastsuchit[0]==0 or  brd[lastsuchit[0]-1][lastsuchit[1]] in ('x ','0 ')):
                    posthit+=1
                    if posthit==5:
                        lastsuchit=False
                        posthit=1
                    return aihit(brd)
                xhit,yhit=(lastsuchit[0]-1),lastsuchit[1]
                if brd[xhit][yhit]=='* ':
                    brd[xhit][yhit]='0 '
                    posthit+=1
                    print('comp MISS')
                elif brd[xhit][yhit]=='s ':
                    brd[xhit][yhit]='x '
                    posthit=1
                    lastsuchit=xhit,yhit
                    print('comp HIT !!')
                return
            case 2:
                if (
                    lastsuchit[1] == bsize-1 or
                    brd[lastsuchit[0]][lastsuchit[1]+1] in ('x ', '0 ')
                ):
                    posthit += 1
                    if posthit == 5:
                        lastsuchit = False
                        posthit = 1
                    return aihit(brd)
                xhit,yhit=(lastsuchit[0]),(lastsuchit[1]+1)
                if brd[xhit][yhit]=='* ':
                    brd[xhit][yhit]='0 '
                    posthit+=1
                    print('comp MISS')
                elif brd[xhit][yhit]=='s ':
                    brd[xhit][yhit]='x '
                    posthit=1
                    lastsuchit=xhit,yhit
                    print('comp HIT !!')
                return
            case 3:
                if (
                    lastsuchit[0] == bsize-1 or
                    brd[lastsuchit[0]+1][lastsuchit[1]] in ('x ', '0 ')
                ):
                    posthit += 1
                    if posthit == 5:
                        lastsuchit = False
                        posthit = 1
                    return aihit(brd)
                xhit, yhit = lastsuchit[0]+1, lastsuchit[1]
                if brd[xhit][yhit] == '* ':
                    brd[xhit][yhit] = '0 '
                    posthit += 1
                    print("comp MISS")
                else:
                    brd[xhit][yhit] = 'x '
                    lastsuchit = (xhit, yhit)
                    posthit = 1
                    print("comp HIT !!")
                return
            case 4:
                if (
                    lastsuchit[1] == 0 or
                    brd[lastsuchit[0]][lastsuchit[1]-1] in ('x ', '0 ')
                ):
                    lastsuchit = False
                    posthit = 1
                    return aihit(brd)

                xhit, yhit = lastsuchit[0], lastsuchit[1]-1
                if brd[xhit][yhit] == '* ':
                    brd[xhit][yhit] = '0 '
                    lastsuchit = False
                    posthit = 1
                    print("comp MISS")
                else:
                    brd[xhit][yhit] = 'x '
                    lastsuchit = (xhit, yhit)
                    posthit = 1
                    print("comp HIT !!")
                return
    else:
        cord=random.choice(targset)
        xhit=cord[0]
        yhit=cord[1]
        if brd[xhit][yhit]=='* ':
            brd[xhit][yhit]='0 '
            print('comp MISS')
        elif brd[xhit][yhit]=='s ':
            brd[xhit][yhit]='x '
            lastsuchit=cord
            posthit=1
            print('comp HIT !!')
        targset.remove(cord)

def invis(brd):
    brcop=[]
    for x in brd:
        nr=[]
        for y in x:
            nr.append(y)
        brcop.append(nr)
    for i in range(bsize):
        for j in range(bsize):
            if brcop[i][j]=='s ' :
                brcop[i][j]='* '
    return brcop

def checkwin(user,comp):
    elimlist1=[]
    elimlist2=[]
    global gameon
    for x in comp:
        for y in x:
            elimlist1.append(y)
    if 's ' in elimlist1:
        pass
    else:
        txt='YOU WIIINNN!!'
        subprocess.call('cls',shell=True)
        print('-'*3*bsize)
        print('-'*((3*bsize+3-len(txt))//2),txt,'-'*((3*bsize+3-len(txt))//2),sep='')
        print('-'*3*bsize)
        disp(cmp,'comp')
        disp(usr,'USER')
        time.sleep(3)
        resp=input('Wanna play again? (y/n) ').lower()
        if resp=='y':
            return init()
        else:
            print('BYEE 😊')
            gameon=int(0)
            return
    for x in user:
        for y in x:
            elimlist2.append(y)
    if 's ' in elimlist2:
        pass
    else:
        txt='YOU Lose!!'
        subprocess.call('cls',shell=True)
        print('-'*3*bsize)
        print('-'*((3*bsize+3-len(txt))//2),txt,'-'*((3*bsize+3-len(txt))//2),sep='')
        print(''*3*bsize)
        disp(cmp,'comp')
        disp(usr,'USER')
        time.sleep(3)
        resp=input('Try again? (y/n) ').lower()
        if resp=='y':
            return init()
        else:
            print('BYEE 😊')
            gameon=int(0)
            return

def init():
    global usr
    global cmp
    global gameon
    global lastsuchit
    global posthit
    lastsuchit=False
    gameon=1
    posthit=0
    subprocess.call('cls',shell=True)
    cmp=randomboard(bsize,ships)
    usr=setuboard(bsize,ships)

init()

while gameon:
    subprocess.call('cls',shell=True)
    disp(invis(cmp),'comp')
    disp(usr,'USER')
    uhit(cmp)
    aihit(usr)
    checkwin(usr,cmp)
    time.sleep(1)