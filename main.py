import random
import threading 
import sys
from IPy import IP
from govRanges import bl1, bl2, bl3
import time
import asyncio

class generate():
    def __init__(self, fName):
        self.badTypes = ["PRIVATE", "LOOPBACK", "RESERVED", "CARRIER_GRADE_NAT"]
        self.threeBL = bl1
        self.twoBL = bl3
        self.oneBL = bl2
        self.genIPs = 0
        self.fileName = "{}".format(fName)
        threading.Thread.__init__(self)
        self.f = open(self.fileName, "w+")

    #def isIllegal(self, ip):



    async def isPrivateSubnet(self, ip):
        check = IP(ip)
        result = check.iptype()
        if(result in self.badTypes):
            return True
        else:
            return False
    
    async def isIllegalIP(self, ip):
        o = ip.split(".")
        threeCheck = ".".join(o[0:3])
        twoCheck = ".".join(o[0:2])
        oneCheck = ".".join(o[0:1])

        if(oneCheck in self.oneBL):
            return True
        elif(twoCheck in self.twoBL):
            return True
        elif(threeCheck in self.threeBL):
            return True
        else:
            return False
        
    
    async def gen(self, Mlines):
        tic = time.perf_counter()
        maxIPs = int(Mlines)
        while int(maxIPs) > int(self.genIPs):
            self.o = []

            o1 = random.randint(1, 255)
            self.o.append(str(o1)) 

            o2 = random.randint(0, 255)
            self.o.append(str(o2))

            o3 = random.randint(0, 255)
            self.o.append(str(o3))

            o4 = random.randint(0, 255)
            self.o.append(str(o4)) 

            ip = '.'.join(self.o)
            isPrivateSubnet = await self.isPrivateSubnet(ip)
            isIllegalIP = await self.isIllegalIP(ip)
            if(ip in self.f.read()):
                pass
            elif(isPrivateSubnet is False and isIllegalIP is False):
                self.f.write("{}\n".format(ip))
                #print(ip)
                self.genIPs += 1
            
        toc = time.perf_counter()
        print(f"Scraped {maxIPs} IPs in {toc - tic:0.4} seconds")
        sys.exit(0)
        


    async def run(self, AMlines):
        await self.gen(AMlines)

try:
    #threads = sys.argv[1]
    linesA = int(sys.argv[1])
except:
    print("\x1b[96mUsage\x1b[97m:\x1b[95m python3 {}\x1b[95m [\x1b[96mthreads\x1b[95m] [\x1b[96mno. of IPs\x1b[95m] [\x1b[96mfileName\x1b[95m]\x1b[97m".format(sys.argv[0]))
    sys.exit(0)

try:
    fileName = sys.argv[2]
except:
    fileName = "ips.txt"

#generate(fileName).run(threads, int(linesA))
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)
result = loop.run_until_complete(generate(fileName).run(linesA))