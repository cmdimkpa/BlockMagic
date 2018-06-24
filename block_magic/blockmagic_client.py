# -*- coding: latin-1 -*-

"""
BlockMagic: I/O Client for the [Monty.Link] data storage blockchain
Ver: 2.5.1
(c) Monty Dimkpa, June 2018
"""

import json,os,urllib2

def o(x):
    s=""
    for i in x:s+=chr(int(15.968**2+0.5)-ord(i));
    s=s.decode("latin-1");s = s.replace("=","");s = s.replace("<z",":");s = s.replace("<o","/");s = s.replace("<n",".");s = s.replace("<m","-");s = s.replace("<","?");s = s.replace("<}","=");s = s.replace("<e","%");s = s.replace("<f","&");return s

wr = o("ÅÐÐÑÐ")
dr = os.getcwd()
if "/" in dr:lr=dr+"/"
else:lr=dr+"\\"
kac = lr+o("ÑÑ")
kacd = {}
kacd["blocks"] = {}
nbu = wr + o("ÐÒÀÂ")
pdbu = wr+o("ÚÐÚ")
pdbu2 = wr+o("ÐÒÒÀ ÂÚÙ ÂÚ")
b0 = {};b1 = {0:"0",1:"1",2:"2",3:"3",4:"4",5:"5",6:"6",7:"7",8:"8",9:"9",10:"a",11:"b",12:"c",13:"d",14:"e",15:"f"}
for i in range(int(6.349**3+0.5)):b0[i]=chr(i)
kv_pairs = [(k,b0[k]) for k in b0];
for k,v in kv_pairs:b0[v]=k;kv_pairs = [(k,b1[k]) for k in b1];
for k,v in kv_pairs:b1[v]=k;
def r(l):
    s = ""
    for f in l:s+=f;
    return s.decode("latin-1")
def tab(j,k):
    r1 = j; c = [];
    def si():
        return r1%k, int(r1/k)
    while r1 > 0:
        r2, r1 = si()
        c.append(r2)
    return c[::-1]
def tbt(c,k):
    k2 = 0; n = len(c);j=0
    for i in c:j+=1;p = n - j;k2+=(i*(k**p));
    return k2
def fb0(c):c = map(lambda x:b0[x],c);return tbt(c,int(6.349**3+0.5))
def tb1(j):return r(map(lambda x:b1[x],tab(j,int(2.519**3+0.5))))
def th(d):return tb1(fb0(str(d)))

def ReadCache():
	process = open(kac,'rb+')
	data = process.read()
	process.close()
	return json.loads(data)

def UpdateCache():
	process = open(kac,'wb+')
	process.write(json.dumps(kacd))
	process.close()

try:
	kacd = ReadCache()
except:
	UpdateCache()

def FetchPageAsJSON(url):
	try:
		return json.loads(str(urllib2.urlopen(str(url)).read())), 200
	except Exception as e:
		return str(e), 401

def AllIsWell():
	ok = 0; attempts = 0
	while attempts < 3:
		if FetchPageAsJSON(o("ÅÐÐÑÐ"))[1] == 200:
			ok+=1
		attempts+=1
	if ok > 1:
		return True
	else:
		return False

def version():
	return "2.5.1"

ver = version

def CreateBlock(name,description="no info"):
	name, description = map(lambda x:x.lower(),[name,description])
	global kacd
	if name in kacd["blocks"]:
		return "a block with this name exists, try another name"
	else:
		server_response = PersistentRequest(nbu)
		try:
			tracking_url = server_response["data"]["tracking_url"]
			kacd["blocks"][name] = {"url":tracking_url,"about":description}
			UpdateCache()
			status = "the block [%s] was registered on the blockchain" % name
			return status
		except:
			status = "create block exception"
			return status

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

def PersistentRequest(url):
	server_response, code = FetchPageAsJSON(url)
	retry_count = 0
	while code != 200 and AllIsWell()==False:
		server_response, code = FetchPageAsJSON(url)
		if code != 200:
			print "retrying...(%d)" % retry_count
			server_response = url+" (unreachable)"
			print server_response
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
			push_data_url = pdbu % (block_code,th(parameterize(record)))
			print PersistentRequest(push_data_url)


def fetch_all(format_type):
	collection = {}
	block_data = ReadCache()["blocks"]
	for blockname in block_data:
		block_url, block_code = GetBlockIdentifiers(blockname)
		fetch_url = pdbu2 % (block_code,format_type)
		result = PersistentRequest(fetch_url)
		try:
			keys = result.keys()
			collection[blockname] = result[keys[-1]]
		except:
			collection[blockname] = "invalid block exception"
	return collection


def fetch_one(blockname,format_type):
	blockname = blockname.lower()
	block_data = ReadCache()["blocks"]
	if blockname not in block_data:
		return "block not found"
	else:
		block_url, block_code = GetBlockIdentifiers(blockname)
		fetch_url = pdbu2 % (block_code,format_type)
		result = PersistentRequest(fetch_url)
		try:
			keys = result.keys()
			return result[keys[-1]]
		except:
			return "invalid block exception"

def return_all_lx():
	return fetch_all("ledger")

def return_all_tx():
	return fetch_all("transactions")

def return_one_lx(blockname):
	return fetch_one(blockname,"ledger")

def return_one_tx(blockname):
	return fetch_one(blockname,"transactions")

def list_my_blocks():
	return ReadCache()["blocks"].keys()

