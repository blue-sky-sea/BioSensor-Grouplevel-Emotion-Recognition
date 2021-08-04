import asyncio
from bleak import BleakScanner
global h10_address
h10_address=""
async def run():
    devices = await BleakScanner.discover()
    for d in devices:
        print(str(d))
        if(": Polar H10 9563FE26" in str(d)):
        	global h10_address
        	h10_address=str(d).replace(": Polar H10 9563FE26","")
        	h10_address.strip(" ")
        	print("polar H10 address:##",h10_address,"##")

loop = asyncio.get_event_loop()
loop.run_until_complete(run())
#6E:7E:D6:86:88:41

#import asyncio
from bleak import BleakClient
#E7:AF:00:96:72:DB: Polar H10 9563FE26
address = "E7:AF:00:96:72:DB"
if( h10_address!=""):
	address = h10_address
else:
	pass

print("#"*50)
print("##",address,"##")
MODEL_NBR_UUID = "00002a24-0000-1000-8000-00805f9b34fb"

async def run(address):
    async with BleakClient(address) as client:
        model_number = await client.read_gatt_char(MODEL_NBR_UUID)
        print("Model Number: {0}".format("".join(map(chr, model_number))))

loop = asyncio.get_event_loop()
loop.run_until_complete(run(address))
