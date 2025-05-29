memory = [0] * 65536

def getm(m):
    return memory[m]

def storem(addr, t):
    memory[addr] = int(t) % 256

def progcounter(num = None):
    if num is None:
        return int(memory[256] * 256 + memory[257])
    else:
        memory[256] = int((num - num % 256) / 256)
        memory[257] = int(num % 256)

def nextm():
    progcounter(progcounter() + 1)
    return getm(progcounter() - 1)

def run1():
    match nextm():
        case 0:
            return False
        case 1:
            mema = nextm() * 256 + nextm()
            memb = nextm() * 256 + nextm()
            storem(memb, getm(mema))
        case 2:
            mema = nextm() * 256 + nextm()
            memb = nextm() * 256 + nextm()
            storem(memb, getm(mema) + getm(memb))
        case 3:
            mema = nextm() * 256 + nextm()
            memb = nextm() * 256 + nextm()
            storem(memb, getm(memb) - getm(mema))
        case 4:
            mema = nextm() * 256 + nextm()
            memb = nextm() * 256 + nextm()
            storem(memb, getm(mema) * getm(memb))
        case 5:
            mema = nextm() * 256 + nextm()
            memb = nextm() * 256 + nextm()
            denom = getm(mema)
            storem(memb, getm(memb) // denom if denom != 0 else 0)
        case 6:
            memj = nextm() * 256 + nextm()
            progcounter(memj)
        case 7:
            memj = nextm() * 256 + nextm()
            memc = nextm() * 256 + nextm()
            memd = nextm() * 256 + nextm()
            if getm(memc) == getm(memd):
                progcounter(memj)
        case 8:
            memj = nextm() * 256 + nextm()
            memc = nextm() * 256 + nextm()
            memd = nextm() * 256 + nextm()
            if getm(memc) < getm(memd):
                progcounter(memj)
        case 9:
            memj = nextm() * 256 + nextm()
            memc = nextm() * 256 + nextm()
            memd = nextm() * 256 + nextm()
            if getm(memc) > getm(memd):
                progcounter(memj)
    return True

def displayoutput():
    t = ''
    for c in memory[384:511]:
        t += chr(c)
    print(t)

def run():
    progcounter(512)
    running = True
    while running:
        running = run1()
        displayoutput()

def loadprog(i = []):
    m = input(': ')
    for b in m.split(' '):
        i.append(int(b))
    for j in range(512, 512 + len(i)):
        memory[j] = i[j - 512] % 256
loadprog()
run()