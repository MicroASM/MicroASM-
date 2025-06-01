from multiprocessing import shared_memory

def exists_shared_memory(name):
    try:
        shm = shared_memory.SharedMemory(name=name)
        shm.close()
        return True
    except FileNotFoundError:
        return False
def create_shared_memory(n):
    shm = shared_memory.SharedMemory(create=not exists_shared_memory('MicroASMsharedmemory_main_output_abv'), size=128, name = n)
    return shm

def write_text(shm, text):
    btext = text.encode('utf-8')[:128]
    shm.buf[:len(btext)] = btext
    if len(btext) < 128:
        shm.buf[len(btext):128] = b'\x00' * (128 - len(btext))
outputshm = create_shared_memory('MicroASMsharedmemory_main_output_abv')

memory = []
for i in range(256):
    memory.append(i)
for _ in range(65280):
    memory.append(0)
def getm(m):
    return memory[m]
def progcounter(num = None):
    global memory
    if num is None:
        return int(memory[256]*256+memory[257])
    else:
        memory[256] = int((num - num % 256) / 256)
        memory[257] = int(num % 256)
progcounter(512)
def storem(addr, t):
    global memory
    memory[addr] =int(t) % 256
def nextm():
    progcounter(progcounter()+1)
    return getm(progcounter()-1)
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
            storem(memb, getm(mema)+getm(memb))
        case 3:
            mema = nextm() * 256 + nextm()
            memb = nextm() * 256 + nextm()
            storem(memb, getm(memb)-getm(mema))
        case 4:
            mema = nextm() * 256 + nextm()
            memb = nextm() * 256 + nextm()
            storem(memb, getm(mema)*getm(memb))
        case 5:
            mema = nextm() * 256 + nextm()
            memb = nextm() * 256 + nextm()
            denom = getm(memb)
            if denom == 0:
                storem(memb, 0)
            else:
                storem(memb, denom // getm(mema))
        case 6:
            memj = nextm() * 256 + nextm()
            progcounter(num = memj)
        case 7:
            memj = nextm() * 256 + nextm()
            memc = nextm() * 256 + nextm()
            memd = nextm() * 256 + nextm()
            if getm(memc) == getm(memd):
                progcounter(num = memj)
        case 8:
            memj = nextm() * 256 + nextm()
            memc = nextm() * 256 + nextm()
            memd = nextm() * 256 + nextm()
            if getm(memc) < getm(memd):
                progcounternum = (memj)
        case 9:
            memj = nextm() * 256 + nextm()
            memc = nextm() * 256 + nextm()
            memd = nextm() * 256 + nextm()
            if getm(memc) > getm(memd):
                progcounter(num = memj)
        case 10: #blank
            memj = nextm() * 256 + nextm()
            memc = nextm() * 256 + nextm()
            memd = nextm() * 256 + nextm()
            if getm(memc) == getm(memd):
                progcounter(memj)
        case 11: #blank
            memj = nextm() * 256 + nextm()
            memc = nextm() * 256 + nextm()
            memd = nextm() * 256 + nextm()
            if getm(memc) == getm(memd):
                progcounter(memj)
    return True
def displayoutput():
    t = ''
    t = bytes(memory[384:512]).decode('utf-8', errors='ignore')
    write_text(outputshm, t)
    print(memory[384:512])
def run():
    running  = True
    print(memory[512:])
    while running:
        running = run1()
        displayoutput()
def loadprog(i = []):
    m = input(': ')
    for b in m.split(' '):
        i.append(int(b))
    for j in range(512, 512 + len(i)):
        memory[j] = i[j-512] % 256
loadprog()
run()
