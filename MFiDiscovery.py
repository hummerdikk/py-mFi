from socket import *
import trollius as asyncio

class MFiDiscover:

    def __init__(self, loop=None):
        self.discoveryPayload = bytearray()
        self.discoveryPayload.append(0x01)
        self.discoveryPayload.append(0x00)
        self.discoveryPayload.append(0x00)
        self.discoveryPayload.append(0x00)

        self.sock = socket(AF_INET, SOCK_DGRAM)
        self.sock.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
        self.sock.setblocking(0)

        self.loop = loop
        if not self.loop:
            self.loop = asyncio.get_event_loop()

        self.loop.create_task(self.sendDiscovery())
        self.loop.create_task(self.readData())

    @asyncio.coroutine
    def sendDiscovery(self):
        while True:
            print("sending discovery packet")
            self.sock.sendto(self.discoveryPayload, ('<broadcast>', 10001))
            #sleep for 10 mins:
            yield asyncio.From(asyncio.sleep(600))

    @asyncio.coroutine
    def readData(self):
        while True:
            try:
                data, addrport = self.sock.recvfrom(1024)
                address, port = addrport
                print("Received:", data, address)
            except BlockingIOError:
                yield asyncio.From(asyncio.sleep(3))
            except:
                import sys, traceback
                exc_type, exc_value, exc_traceback = sys.exc_info()
                traceback.print_tb(exc_traceback, limit=1, file=sys.stdout)
                traceback.print_exception(exc_type, exc_value, exc_traceback,
                        limit=2, file=sys.stdout)
                yield asyncio.From(asyncio.sleep(3))
                

            



def testDiscoverMFI():
    sock = socket(AF_INET, SOCK_DGRAM)
    sock.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
    sock.settimeout(30)
    
    payload = bytearray()
    payload.append(0x01)
    payload.append(0x00)
    payload.append(0x00)
    payload.append(0x00)

    print ("payload: {}".format(payload))
    sock.sendto(payload, ('<broadcast>', 10001))
    recv = ''
    MFIs = []
    while True:
        try:
            response = sock.recvfrom(1024)
        except:
            break
        print(response)
    # Parse response        

if __name__ == '__main__':

    #testDiscoverMFI()

    discovery = MFiDiscover()

    asyncio.get_event_loop().run_forever()