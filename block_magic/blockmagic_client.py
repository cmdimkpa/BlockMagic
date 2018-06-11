# I/O Client for the BlockMagic data storage blockchain

import json,os
import urllib2
from time import sleep

global WebRoot, LocalRoot, cache, cache_data, new_block_url, push_data_base_url, pull_data_base_url

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
push_data_base_url = WebRoot+'%s/block_info:%s'
pull_data_base_url = WebRoot+"api/get-block-data?block_code=%s&data_format=%s"

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

def FetchPageAsJSON(url):
	try:
		return json.loads(urllib2.urlopen(url).read())
	except:
		return {"code":401}

def CreateBlock(name,description="no info"):
	name, description = map(lambda x:x.lower(),[name,description])
	global cache_data
	if name in cache_data["blocks"]:
		return "a block with this name exists, try another name"
	else:
		server_response = FetchPageAsJSON(new_block_url)
		tracking_url = server_response["data"]["tracking_url"]
		cache_data["blocks"][name] = {"url":tracking_url,"about":description}
		UpdateCache()
		return "the block [%s] was registered on the blockchain" % name

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
	return parameters[:-1]

def SendData(blockname,record_list):
	blockname = blockname.lower()
	block_data = ReadCache()["blocks"]
	if blockname not in block_data:
		return "block not found"
	else:
		block_url, block_code = GetBlockIdentifiers(blockname)
		for record in record_list:
			push_data_url = push_data_base_url % (block_code,parameterize(record))
			code = 401
			while code == 401:
				server_response = FetchPageAsJSON(push_data_url)
				code = server_response["code"]
				if code == 401:
					sleep(5)
			print server_response

def ReturnMyLedger():
	myLedger = {}
	block_data = ReadCache()["blocks"]
	for blockname in block_data:
		block_url, block_code = GetBlockIdentifiers(blockname)
		fetch_url = pull_data_base_url % (block_code,"ledger")
		result = FetchPageAsJSON(fetch_url); keys = result.keys()
		myLedger[blockname] = result[keys[-1]]
	return myLedger

def ReturnMyTransactions():
	myTransactions = {}
	block_data = ReadCache()["blocks"]
	for blockname in block_data:
		block_url, block_code = GetBlockIdentifiers(blockname)
		fetch_url = pull_data_base_url % (block_code,"transactions")
		result = FetchPageAsJSON(fetch_url); keys = result.keys()
		myTransactions[blockname] = result[keys[-1]]
	return myTransactions

def ReturnALedger(blockname):
	blockname = blockname.lower()
	ledger = ReturnMyLedger()
	if blockname not in ledger:
		return "document not found"
	else:
		return ledger[blockname]

def ReturnATransaction(blockname):
	blockname = blockname.lower()
	transactions = ReturnMyTransactions()
	if blockname not in transactions:
		return "document not found"
	else:
		return transactions[blockname]
