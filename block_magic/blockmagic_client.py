#!/usr/bin/env python2
# -*- coding: latin-1 -*-

"""
BlockMagic: Official I/O Client for the [Monty.Link] data storage blockchain
Ver: 2.6
(c) Monty Dimkpa, June 2018
"""

import json,os,urllib2,datetime,cPickle

def o(x):
    s=""
    for i in x:s+=chr(int(15.968**2+0.5)-ord(i));
    s=s.decode("latin-1");s = s.replace("=","");s = s.replace("<z",":");s = s.replace("<o","/");s = s.replace("<n",".");s = s.replace("<m","-");s = s.replace("<","?");s = s.replace("<}","=");s = s.replace("<e","%");s = s.replace("<f","&");return s

wr = o("ÅÐÐÑÐ")
dr = os.getcwd()
if "/" in dr:lr=dr+"/"
else:lr=dr+"\\"
kac = lr+o("ÑÑ")
dbm = lr+o("Ñ")
dbs = {}
kacd = {}
kacd["blocks"] = {}
nbu = wr + o("ÐÒÀÂ")
pdbu = wr+o("ÚÐÚ")
pdbu2 = wr+o("ÐÒÒÀ ÂÚÙ ÂÚ")
b0 = {};b1 = {0:"0",1:"1",2:"2",3:"3",4:"4",5:"5",6:"6",7:"7",8:"8",9:"9",10:"a",11:"b",12:"c",13:"d",14:"e",15:"f"}
IO_Toolkit = {"serialize":{0:json.dumps,1:cPickle.dumps},"deserialize":{0:json.loads,1:cPickle.loads}}
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

def timestamp():
    return datetime.datetime.today()

def ReadFile(f,deserializer_id):
    process = open(f,'rb+')
    s = process.read()
    process.close()
    return IO_Toolkit["deserialize"][deserializer_id](s)

def UpdateFile(f,k,serializer_id):
    process = open(f,'wb+')
    process.write(IO_Toolkit["serialize"][serializer_id](k))
    process.close()

def ReadCache():
    return ReadFile(kac,0)

def UpdateCache():
    UpdateFile(kac,kacd,0)

def ReadDBCache():
    return ReadFile(dbm,1)

def UpdateDBCache(dbs):
    UpdateFile(dbm,dbs,1)

try:
	kacd = ReadCache()
except:
	UpdateCache()

try:
	dbs = ReadDBCache()
except:
	UpdateDBCache(dbs)

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
	return "2.5.2"

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
			return PersistentRequest(push_data_url)

def send_data(blockname,record_list):
	status = SendData(blockname,record_list)
	while bool(status!="block not found" and str(status)!="{u'message': u'Ledger updated', u'code': 201}"):
		status = SendData(blockname,record_list)
	return status


def persistent_retrieve(url):
	result = PersistentRequest(url)
	try:
		keys = result.keys()
		return result[keys[-1]]
	except:
		return persistent_retrieve(url)

def fetch_all(format_type):
	collection = {}
	block_data = ReadCache()["blocks"]
	for blockname in block_data:
		block_url, block_code = GetBlockIdentifiers(blockname)
		fetch_url = pdbu2 % (block_code,format_type)
		collection[blockname] = persistent_retrieve(fetch_url)
	return collection


def fetch_one(blockname,format_type):
	blockname = blockname.lower()
	block_data = ReadCache()["blocks"]
	if blockname not in block_data:
		return "block not found"
	else:
		block_url, block_code = GetBlockIdentifiers(blockname)
		fetch_url = pdbu2 % (block_code,format_type)
		return persistent_retrieve(fetch_url)

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

class Rigo:
    def __init__(self,name,password):
        self.name = name;
        self.password = password;
        self.Tables = {};
        self.Blocks = {};
        self.entries = {};
        self.created = timestamp();
        self.createdTime = {};
        self.deletedTime = {};
        self.editHistory = {};

    def newTable(self,tableName,blockName,password):
        if password != self.password:
            return "DBAccessError: could not connect to database [bad password]"
        tableName,blockName = map(lambda x:str(x).lower(), [tableName,blockName])
        if tableName in ["","none"]:
            return "CreateTableError: bad table name: %s" % tableName.upper()
        else:
            if tableName in self.Tables:
                return "CreateTableError: duplicate table name: %s" % tableName.upper()
            else:
                if blockName == "block not found":
                    return "CreateTableError: target block: %s not found" % blockName.upper()
                else:
                    self.Tables[tableName] = [];
                    self.Blocks[tableName] = blockName;
                    self.entries[tableName] = -1;
                    self.createdTime[tableName] = timestamp();
                    self.editHistory[tableName] = [];
                    return "CreateTableSuccess: table: %s was created" % tableName.upper()

    def deleteTable(self,tableName,password):
        if password != self.password:
            return "DBAccessError: could not connect to database [bad password]"
        proposed = str(tableName).lower()
        master = map(lambda x:str(x).lower(), self.Tables.keys())
        if proposed in master:
            self.deletedTime[proposed] = timestamp()
            del self.Tables[proposed]
            return "DeleteTableSuccess: table: %s was deleted" % tableName.upper()
        else:
            return "DeleteTableError: no such table: %s" % tableName.upper()

    def newEntry(self,tableName,entry,password):
        if password != self.password:
            return "DBAccessError: could not connect to database [bad password]"
        proposed = str(tableName).lower()
        master = map(lambda x:str(x).lower(), self.Tables.keys())
        if proposed not in master:
            return "WriteTableError: no such table: %s" % tableName.upper()
        else:
            if 'dict' not in str(type(entry)):
                return "WriteTableError: document format not valid"
            else:
                self.entries[tableName]+=1;
                self.editHistory[tableName].append(timestamp());
                self.Tables[tableName].append(entry);
                return "WriteTableSuccess: table: %s  was updated" % tableName.upper()

    def viewEntries(self,tableName,entryPos,password):
        if password != self.password:
            return "DBAccessError: could not connect to database [bad password]"
        proposed = str(tableName).lower()
        master = map(lambda x:str(x).lower(), self.Tables.keys())
        if proposed not in master:
            return "ReadTableError: no such table: %s" % tableName.upper()
        else:
            if 'list' not in str(type(entryPos)) and entryPos != "*":
                return "ReadTableError: invalid selection. Use list or *"
            else:
                if entryPos == "*":
                    return self.Tables[tableName]
                else:
                    selection = [];
                    for index in entryPos:
                        try:
                            selection.append(self.Tables[tableName][index])
                        except:
                            return "ReadTableError: row number: %d out of range (max: %d)" % (index,self.entries[tableName])
                    return selection

    def editEntry(self,tableName,entryPos,new,password):
        if password != self.password:
            return "DBAccessError: could not connect to database [bad password]"
        proposed = str(tableName).lower()
        master = map(lambda x:str(x).lower(), self.Tables.keys())
        if proposed not in master:
            return "EditTableError: no such table: %s" % tableName.upper()
        else:
            if 'int' not in str(type(entryPos)):
                return "EditTableError: invalid row number"
            else:
                try:
                    if 'dict' not in str(type(new)):
                        return "EditTableError: document format not valid"
                    else:
                        self.Tables[tableName][entryPos] = new;
                        self.editHistory[tableName].append(timestamp());
                        return "EditTableSuccess: table: %s was updated at row: %d" % (tableName.upper(),entryPos)
                except:
                    return "EditTableError: row number out of range (max: %d)" % self.entries[tableName]

    def lastChanged(self,tableName,password):
        if password != self.password:
            return "DBAccessError: could not connect to database [bad password]"
        proposed = str(tableName).lower()
        master = map(lambda x:str(x).lower(), self.Tables.keys())
        if proposed not in master:
            return "Error: no such table: %s" % tableName.upper()
        else:
            return str(self.editHistory[proposed][-1])

    def rows(self,tableName,password):
        if password != self.password:
            return "DBAccessError: could not connect to database [bad password]"
        proposed = str(tableName).lower()
        master = map(lambda x:str(x).lower(), self.Tables.keys())
        if proposed not in master:
            return "Error: no such table: %s" % tableName.upper()
        else:
            return self.entries[proposed]

    def deleteEntry(self,tableName,entryPos,password):
        if password != self.password:
            return "DBAccessError: could not connect to database [bad password]"
        proposed = str(tableName).lower()
        master = map(lambda x:str(x).lower(), self.Tables.keys())
        if proposed not in master:
            return "EditTableError: no such table: %s" % tableName.upper()
        else:
            if 'int' not in str(type(entryPos)):
                return "EditTableError: invalid row number"
            else:
                try:
                    self.Tables[tableName].pop(entryPos)
                    self.editHistory[tableName].append(timestamp());
                    self.entries[tableName]-=1
                    return "EditTableSuccess: row: %d of table: %s was deleted" % (entryPos,tableName.upper())
                except:
                    return "EditTableError: row number out of range (max: %d)" % self.entries[tableName]

def RigoDB(command,options={}):
    command = command.lower()
    if command == 'new_database':
        required = ["dbname","dbpassword"]
        provided = map(lambda x:str(x).lower(), options.keys())
        missing = [x for x in required if x not in provided]
        if missing != []:
            return "the following required fields are missing: %s" % str(missing)
        else:
            dbname = str(options["dbname"])
            dbpassword = str(options["dbpassword"])
            if dbname in ["","none"]:
                return "CreateDBError: bad database name: %s" % dbname.upper()
            if dbpassword in ["","none"]:
                return "CreateDBError: bad database password: %s" % dbpassword.upper()
            if dbname in ReadDBCache():
                    return "CreateDBError: duplicate database name: %s" % dbname.upper()
            else:
                dbs = ReadDBCache()
                dbs[dbname] = Rigo(dbname,dbpassword);
                UpdateDBCache(dbs)
                return "CreateDBSuccess: database: %s was created" % dbname.upper()

    if command == 'delete_database':
        required = ["dbname","dbpassword"]
        provided = map(lambda x:str(x).lower(), options.keys())
        missing = [x for x in required if x not in provided]
        if missing != []:
            return "the following required fields are missing: %s" % str(missing)
        else:
            dbname = str(options["dbname"])
            dbpassword = str(options["dbpassword"])
            dbs = ReadDBCache()
            if dbname not in dbs:
                return "DBAccessError: could not connect to database [not found]"
            else:
                try:
                    if dbpassword != dbs[dbname].password:
                        return "DBAccessError: could not connect to database [bad password]"
                    else:
                        del dbs[dbname]
                        UpdateDBCache(dbs)
                        return "DBOpSuccess: database %s was deleted" % dbname.upper()
                except:
                    return "DBAccessError: problem executing your query"

    if command == 'add_table':
        required = ["dbname","dbpassword","tablename","blockname"]
        provided = map(lambda x:str(x).lower(), options.keys())
        missing = [x for x in required if x not in provided]
        if missing != []:
            return "the following required fields are missing: %s" % str(missing)
        else:
            dbname = str(options["dbname"])
            dbpassword = str(options["dbpassword"])
            tablename = str(options["tablename"])
            blockname = str(options["blockname"])
            if tablename in ["","none"]:
                return "CreateTableError: bad table name: %s" % tablename.upper()
            dbs = ReadDBCache()
            if dbname not in dbs:
                return "DBAccessError: could not connect to database [not found]"
            else:
                try:
                    if dbpassword != dbs[dbname].password:
                        return "DBAccessError: could not connect to database [bad password]"
                    else:
                        if tablename in dbs[dbname].Tables:
                            return "TableAccessError: table exists"
                        else:
                            if GetBlockIdentifiers(blockname) == "block not found":
                                return "TableAccessError: target block not found"
                            else:
                                message = dbs[dbname].newTable(tablename,blockname,dbpassword)
                                UpdateDBCache(dbs)
                                return message
                except:
                    return "DBAccessError: problem executing your query"

    if command == 'delete_table':
        required = ["dbname","dbpassword","tablename"]
        provided = map(lambda x:str(x).lower(), options.keys())
        missing = [x for x in required if x not in provided]
        if missing != []:
            return "the following required fields are missing: %s" % str(missing)
        else:
            dbname = str(options["dbname"])
            dbpassword = str(options["dbpassword"])
            tablename = str(options["tablename"])
            dbs = ReadDBCache()
            if dbname not in dbs:
                return "DBAccessError: could not connect to database [not found]"
            else:
                try:
                    if dbpassword != dbs[dbname].password:
                        return "DBAccessError: could not connect to database [bad password]"
                    else:
                        if tablename not in dbs[dbname].Tables:
                            return "TableAccessError: table not found"
                        else:
                            message = dbs[dbname].deleteTable(tablename,dbpassword)
                            UpdateDBCache(dbs)
                            return message
                except:
                    return "DBAccessError: problem executing your query"

    if command == 'new_entry':
        required = ["dbname","dbpassword","tablename","entry"]
        provided = map(lambda x:str(x).lower(), options.keys())
        missing = [x for x in required if x not in provided]
        if missing != []:
            return "the following required fields are missing: %s" % str(missing)
        else:
            dbname = str(options["dbname"])
            dbpassword = str(options["dbpassword"])
            tablename = str(options["tablename"])
            entry = options["entry"]
            dbs = ReadDBCache()
            if dbname not in dbs:
                return "DBAccessError: could not connect to database [not found]"
            else:
                try:
                    if dbpassword != dbs[dbname].password:
                        return "DBAccessError: could not connect to database [bad password]"
                    else:
                        if tablename not in dbs[dbname].Tables:
                            return "TableAccessError: table not found"
                        else:
                            message = dbs[dbname].newEntry(tablename,entry,dbpassword)
                            UpdateDBCache(dbs)
                            return message
                except:
                    return "DBAccessError: problem executing your query"

    if command == 'view_entries':
        required = ["dbname","dbpassword","tablename","entrypos"]
        provided = map(lambda x:str(x).lower(), options.keys())
        missing = [x for x in required if x not in provided]
        if missing != []:
            return "the following required fields are missing: %s" % str(missing)
        else:
            dbname = str(options["dbname"])
            dbpassword = str(options["dbpassword"])
            tablename = str(options["tablename"])
            entryPos = options["entryPos"]
            dbs = ReadDBCache()
            if dbname not in dbs:
                return "DBAccessError: could not connect to database [not found]"
            else:
                try:
                    if dbpassword != dbs[dbname].password:
                        return "DBAccessError: could not connect to database [bad password]"
                    else:
                        if tablename not in dbs[dbname].Tables:
                            return "TableAccessError: table not found"
                        else:
                            message = dbs[dbname].viewEntries(tablename,entryPos,dbpassword)
                            UpdateDBCache(dbs)
                            return message
                except:
                    return "DBAccessError: problem executing your query"

    if command == 'edit_entry':
        required = ["dbname","dbpassword","tablename","entrypos","new"]
        provided = map(lambda x:str(x).lower(), options.keys())
        missing = [x for x in required if x not in provided]
        if missing != []:
            return "the following required fields are missing: %s" % str(missing)
        else:
            dbname = str(options["dbname"])
            dbpassword = str(options["dbpassword"])
            tablename = str(options["tablename"])
            entryPos = options["entryPos"]
            new = options["new"]
            dbs = ReadDBCache()
            if dbname not in dbs:
                return "DBAccessError: could not connect to database [not found]"
            else:
                try:
                    if dbpassword != dbs[dbname].password:
                        return "DBAccessError: could not connect to database [bad password]"
                    else:
                        if tablename not in dbs[dbname].Tables:
                            return "TableAccessError: table not found"
                        else:
                            message = dbs[dbname].editEntry(tablename,entryPos,new,dbpassword)
                            UpdateDBCache(dbs)
                            return message
                except:
                    return "DBAccessError: problem executing your query"

    if command == 'delete_entry':
        required = ["dbname","dbpassword","tablename","entrypos"]
        provided = map(lambda x:str(x).lower(), options.keys())
        missing = [x for x in required if x not in provided]
        if missing != []:
            return "the following required fields are missing: %s" % str(missing)
        else:
            dbname = str(options["dbname"])
            dbpassword = str(options["dbpassword"])
            tablename = str(options["tablename"])
            entryPos = options["entryPos"]
            dbs = ReadDBCache()
            if dbname not in dbs:
                return "DBAccessError: could not connect to database [not found]"
            else:
                try:
                    if dbpassword != dbs[dbname].password:
                        return "DBAccessError: could not connect to database [bad password]"
                    else:
                        if tablename not in dbs[dbname].Tables:
                            return "TableAccessError: table not found"
                        else:
                            message = dbs[dbname].deleteEntry(tablename,entryPos,dbpassword)
                            UpdateDBCache(dbs)
                            return message
                except:
                    return "DBAccessError: problem executing your query"

    if command == 'last_changed':
        required = ["dbname","dbpassword","tablename"]
        provided = map(lambda x:str(x).lower(), options.keys())
        missing = [x for x in required if x not in provided]
        if missing != []:
            return "the following required fields are missing: %s" % str(missing)
        else:
            dbname = str(options["dbname"])
            dbpassword = str(options["dbpassword"])
            tablename = str(options["tablename"])
            dbs = ReadDBCache()
            if dbname not in dbs:
                return "DBAccessError: could not connect to database [not found]"
            else:
                try:
                    if dbpassword != dbs[dbname].password:
                        return "DBAccessError: could not connect to database [bad password]"
                    else:
                        if tablename not in dbs[dbname].Tables:
                            return "TableAccessError: table not found"
                        else:
                            message = dbs[dbname].lastChanged(tablename,dbpassword)
                            UpdateDBCache(dbs)
                            return message
                except:
                    return "DBAccessError: problem executing your query"

    if command == 'row_count':
        required = ["dbname","dbpassword","tablename"]
        provided = map(lambda x:str(x).lower(), options.keys())
        missing = [x for x in required if x not in provided]
        if missing != []:
            return "the following required fields are missing: %s" % str(missing)
        else:
            dbname = str(options["dbname"])
            dbpassword = str(options["dbpassword"])
            tablename = str(options["tablename"])
            dbs = ReadDBCache()
            if dbname not in dbs:
                return "DBAccessError: could not connect to database [not found]"
            else:
                try:
                    if dbpassword != dbs[dbname].password:
                        return "DBAccessError: could not connect to database [bad password]"
                    else:
                        if tablename not in dbs[dbname].Tables:
                            return "TableAccessError: table not found"
                        else:
                            message = dbs[dbname].rows(tablename,dbpassword)
                            UpdateDBCache(dbs)
                            return message
                except:
                    return "DBAccessError: problem executing your query"


    if command == 'commit_table':
        required = ["dbname","dbpassword","tablename"]
        provided = map(lambda x:str(x).lower(), options.keys())
        missing = [x for x in required if x not in provided]
        if missing != []:
            return "the following required fields are missing: %s" % str(missing)
        else:
            dbname = str(options["dbname"])
            dbpassword = str(options["dbpassword"])
            tablename = str(options["tablename"])
            dbs = ReadDBCache()
            if dbname not in dbs:
                return "DBAccessError: could not connect to database [not found]"
            else:
                try:
                    if dbpassword != dbs[dbname].password:
                        return "DBAccessError: could not connect to database [bad password]"
                    else:
                        if tablename not in dbs[dbname].Tables:
                            return "TableAccessError: table not found"
                        else:
                            block = dbs[dbname].Blocks[tablename]
                            for data in dbs[dbname].Tables[tablename]:
                                result = send_data(block,[data])
                            dbs[dbname].deleteTable(tablename,dbpassword)
                            UpdateDBCache(dbs)
                            return "the table: [%s] was committed to the blockchain and deleted from database: [%s]" % (tablename.upper(),dbname.upper())
                except:
                    return "DBAccessError: problem executing your query"

    if command == 'commit_database':
        required = ["dbname","dbpassword"]
        provided = map(lambda x:str(x).lower(), options.keys())
        missing = [x for x in required if x not in provided]
        if missing != []:
            return "the following required fields are missing: %s" % str(missing)
        else:
            dbname = str(options["dbname"])
            dbpassword = str(options["dbpassword"])
            dbs = ReadDBCache()
            if dbname not in dbs:
                return "DBAccessError: could not connect to database [not found]"
            else:
                try:
                    if dbpassword != dbs[dbname].password:
                        return "DBAccessError: could not connect to database [bad password]"
                    else:
                        for tablename in dbs[dbname].Tables:
                            block = dbs[dbname].Blocks[tablename]
                            for data in dbs[dbname].Tables[tablename]:
                                result = send_data(block,[data])
                        del dbs[dbname]
                        UpdateDBCache(dbs)
                        return "the database: [%s] was committed to the blockchain and deleted from your Rigo instance" % dbname.upper()
                except:
                    return "DBAccessError: problem executing your query"
