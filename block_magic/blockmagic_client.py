# I/O Client for the BlockMagic data storage blockchain

import json,os
import urllib2
import datetime

global WebRoot, LocalRoot, cache, cache_data, base_256, base_16, new_block_url, push_data_base_url, pull_data_base_url, ticker_started

# settings

WebRoot = "http://monty.link/"
Dir = os.getcwd()
if "/" in Dir:
	LocalRoot=Dir+"/"
else:
	LocalRoot=Dir+"\\"
cache = LocalRoot+"monty.link.cache"
cache_data = {}
cache_data["blocks"] = {}
new_block_url = WebRoot + "api/new-block?target=blockchain"
push_data_base_url = WebRoot+'%s/%s'
pull_data_base_url = WebRoot+"api/get-block-data?block_code=%s&data_format=%s"

base_256 = {};

for i in range(256):
    base_256[i] = chr(i)

base_16 = {
    0:"0",1:"1",2:"2",3:"3",4:"4",5:"5",6:"6",7:"7",
    8:"8",9:"9",10:"a",11:"b",12:"c",13:"d",14:"e",15:"f"
}

kv_pairs = [(key,base_256[key]) for key in base_256];
for k,v in kv_pairs:base_256[v]=k;

kv_pairs = [(key,base_16[key]) for key in base_16];
for k,v in kv_pairs:base_16[v]=k;

def reduce(a_list):
    string = ""
    for item in a_list:
        string+=item
    return string.decode("latin-1")

def to_arbitrary_base(Z,base):
    runner = Z; conv = [];
    def result():
        return runner%base, int(runner/base)
    while runner > 0:
        rem, runner = result()
        conv.append(rem)
    return conv[::-1]

def to_base_10(conv,base):
    base10 = 0; n = len(conv)
    j=0
    for i in conv:
        j+=1
        power = n - j
        base10+=(i*(base**power))
    return base10

def from_base_256(conv):
    conv = map(lambda x:base_256[x],conv)
    return to_base_10(conv,256)

def to_base_16(Z):
    return reduce(map(lambda x:base_16[x],to_arbitrary_base(Z,16)))

def to_hash(document):
    return to_base_16(from_base_256(str(document)))

def ReadCache():
	process = open(cache,'rb+')
	data = process.read()
	process.close()
	return json.loads(data)

def UpdateCache():
	process = open(cache,'wb+')
	process.write(json.dumps(cache_data))
	process.close()

try:
	cache_data = ReadCache()
except:
	UpdateCache()

def start_ticker():
	global ticker_started
	ticker_started = datetime.datetime.today()

def time_elapsed():
	return (datetime.datetime.today() - ticker_started).seconds

def timer(seconds):
	start_ticker()
	while time_elapsed() < seconds:
		pass
	return "done"

def FetchPageAsJSON(url):
	try:
		return json.loads(str(urllib2.urlopen(str(url)).read())), 200
	except Exception as e:
		return str(e), 401

def CreateBlock(name,description="no info"):
	name, description = map(lambda x:x.lower(),[name,description])
	global cache_data
	if name in cache_data["blocks"]:
		return "a block with this name exists, try another name"
	else:
		server_response = PersistentRequest(new_block_url)
		try:
			tracking_url = server_response["data"]["tracking_url"]
			cache_data["blocks"][name] = {"url":tracking_url,"about":description}
			UpdateCache()
			return "the block [%s] was registered on the blockchain" % name
		except:
			return server_response

def AboutBlock(blockname):
	blockname = blockname.lower()
	block_data = ReadCache()["blocks"]
	if blockname not in block_data:
		return "block not found"
	else:
		return "about block: %s" % block_data[blockname]["about"]

def GetBlockIdentifiers(blockname):
	blockname = blockname.lower()
	block_data = ReadCache()["blocks"]
	if blockname not in block_data:
		return "block not found"
	else:
		block_url = block_data[blockname]["url"]
		block_code = block_url.split('/')[3]
		return block_url,block_code 

def parameterize(data):
	parameters = ""
	for key in data:
		k = str(key); v = str(data[key])
		parameters+=k+"="+v+"&"
	return "block_info:"+parameters[:-1]

def PersistentRequest(url,limit=13):
	server_response, code = FetchPageAsJSON(url)
	retry_count = 0
	while code != 200 and retry_count < limit:
		status = timer(5)
		print "retrying..."
		server_response, code = FetchPageAsJSON(url)
		print str(server_response)+" (target: %s)" % url
		retry_count+=1
	return server_response


def SendData(blockname,record_list):
	blockname = blockname.lower()
	block_data = ReadCache()["blocks"]
	if blockname not in block_data:
		return "block not found"
	else:
		block_url, block_code = GetBlockIdentifiers(blockname)
		for record in record_list:
			push_data_url = push_data_base_url % (block_code,to_hash(parameterize(record)))
			print PersistentRequest(push_data_url)

def return_all_lx():
	myLedger = {}
	block_data = ReadCache()["blocks"]
	for blockname in block_data:
		block_url, block_code = GetBlockIdentifiers(blockname)
		fetch_url = pull_data_base_url % (block_code,"ledger")
		result = PersistentRequest(fetch_url,1)
		try:
			keys = result.keys()
			myLedger[blockname] = result[keys[-1]]
		except:
			print "null block: "+str(result)
	return myLedger

def return_all_tx():
	myTransactions = {}
	block_data = ReadCache()["blocks"]
	for blockname in block_data:
		block_url, block_code = GetBlockIdentifiers(blockname)
		fetch_url = pull_data_base_url % (block_code,"transactions")
		result = PersistentRequest(fetch_url,1)
		try:
			keys = result.keys()
			myTransactions[blockname] = result[keys[-1]]
		except:
			print "null block: "+str(result)
	return myTransactions

def return_one_lx(blockname):
	blockname = blockname.lower()
	ledger = return_all_lx()
	if blockname not in ledger:
		return "document not found"
	else:
		return ledger[blockname]

def return_one_tx(blockname):
	blockname = blockname.lower()
	transactions = return_all_tx()
	if blockname not in transactions:
		return "document not found"
	else:
		return transactions[blockname]


