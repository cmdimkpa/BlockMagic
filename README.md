![blockmagic logo](http://ceres-ai.com:6765/static/blockmagiclogo.jpg)
![rigo logo](http://ceres-ai.com:6765/static/logo-rigo.jpg)
# BlockMagic for Python
## Simple & Fast Web I/O on a Secure Blockchain
**BlockMagic** is an I/O Client for secure data storage and retrieval on the [Monty.Link] Blockchain. It delivers fast data I/O for web applications while ensuring security and privacy of your data.

[**RigoDB**](https://github.com/cmdimkpa/Rigo) is a lightweight database application for Python, and it is bundled with BlockMagic to provide CRUD capabilities prior to final commits to the blockchain. This is because blockchains are **immutable**, meaning the data you store cannot be altered -- however, with RigoDB, you can enjoy traditional CRUD database facilities until you are ready to make a final commit to the blockchain.

### Getting Started

Install BlockMagic from Pip (already bundled with RigoDB as from v2.6):

<pre>
  pip2 install --upgrade block_magic
</pre>

Requires: Python 2.7

### Using BlockMagic

To use BlockMagic after installation via Pip, import the client in your Python2 code:

<pre>
  from block_magic.blockmagic_client import *
</pre>

### Storing data: creating blocks and performing CRUD operations with RigoDB

You can store data on the blockchain by creating blocks. Create a different block for each of your data stores e.g. "WebDirectory", "SalesLogs", "DeviceActivity", "Logins", and so on. It's as easy as invoking the `CreateBlock` command:

<pre>
CreateBlock("WebDirectory","contact information")  # block description is optional
CreateBlock("SalesLogs")
CreateBlock("DeviceActivity")
CreateBlock("Logins")
</pre>

Running the above code generates the following success messages:

<pre>
'the block [webdirectory] was registered on the blockchain'
'the block [saleslogs] was registered on the blockchain'
'the block [deviceactivity] was registered on the blockchain'
'the block [logins] was registered on the blockchain'
</pre>

Once you mine (create) a block, it takes up to a minute to be registered on the blockchain. The client automatically manages the connection for you in case you want to send data immediately.

Your data is not public as it cannot be accessed from any device terminal other than the one used to create the block. Even if you use another terminal type on the same device, the data will not be available. So the communication is a closed I/O circuit.

#### Working with RigoDB: CRUD operations

The first thing to do when planning to save data is to create a database:

<pre>
>>> RigoDB("new_database",{"dbname":"DB_NAME_HERE","dbpassword":"DB_PASSWORD_HERE"})

'CreateDBSuccess: database: DB_NAME_HERE was created'
</pre>

Then we need to add a table:

<pre>
>>> RigoDB("add_table",{"dbname":"DB_NAME_HERE","dbpassword":"DB_PASSWORD_HERE", "tablename":"TABLE_NAME_HERE", "blockname":"TARGET_BLOCK_HERE"})

'CreateTableSuccess: table: TABLE_NAME_HERE was created'
</pre>

Notice that in addition to specifying a table name, we had to include a block name as well: that is because every table must point to a block. When you finally commit your table, the data in the table will be transferred to the block you designate, and the table itself will cease to exist. Without committing, you can hold on to the table and the data in it as long as you wish.

Let's add some data (say, some phone records) to our table:

<pre>
>>> RigoDB("new_entry",{"dbname":"DB_NAME_HERE","dbpassword":"DB_PASSWORD_HERE", "tablename":"table_name_here", "entry":{"name":"John Egglington","phone":"1-800-212-3456","email":"john.egglington@emailserve.net"}})

'WriteTableSuccess: table: TABLE_NAME_HERE  was updated'
</pre>

Note: always use lowercase when providing credentials. Also, note that you must always provide an Object (e.g. JSON document or Python dict) as your entry. 

Now, let's add some more data:

<pre>
>>> RigoDB("new_entry",{"dbname":"DB_NAME_HERE","dbpassword":"DB_PASSWORD_HERE", "tablename":"table_name_here", "entry":{"name":"Monty Dimkpa","phone":"1-820-444-6718","email":"cmdimkpa@gmail.com"}})

'WriteTableSuccess: table: TABLE_NAME_HERE  was updated'
</pre>

<pre>
>>> RigoDB("new_entry",{"dbname":"DB_NAME_HERE","dbpassword":"DB_PASSWORD_HERE", "tablename":"table_name_here", "entry":{"name":"Mary Tipton","phone":"1-616-420-1123","email":"mary_tipton@dowdandco.org"}})

'WriteTableSuccess: table: TABLE_NAME_HERE  was updated'
</pre>

OK, let's see if we can get the data back:

<pre>
>>> RigoDB("view_entries",{"dbname":"DB_NAME_HERE","dbpassword":"DB_PASSWORD_HERE", "tablename":"table_name_here", "entryPos":"*"})

[{'phone': '1-800-212-3456', 'name': 'John Egglington', 'email': 'john.egglington@emailserve.net'}, {'phone': '1-616-420-1123', 'name': 'Mary Tipton', 'email': 'mary_tipton@dowdandco.org'}, {'phone': '1-820-444-6718', 'name': 'Monty Dimkpa', 'email': 'cmdimkpa@gmail.com'}]
</pre>

That was easy enough. We can also edit and delete data:

Editing:

Let's substitute the data on the second row with another dataset:

<pre>
>>> RigoDB("edit_entry",{"dbname":"DB_NAME_HERE","dbpassword":"DB_PASSWORD_HERE", "tablename":"table_name_here", "entryPos":1, "new":{'phone': '1-222-520-4150', 'name': 'Eduardo Salazar', 'email': 'eddy_french@dowdandco.org'}})

'EditTableSuccess: table: TABLE_NAME_HERE was updated at row: 1'
</pre>

Note: row numbers are zero-indexed; meaning the first row is 0 and the second is 1, and so on.

Now, let's see if the data changed:

<pre>
>>> RigoDB("view_entries",{"dbname":"DB_NAME_HERE","dbpassword":"DB_PASSWORD_HERE", "tablename":"table_name_here", "entryPos":"*"})

[{'phone': '1-800-212-3456', 'name': 'John Egglington', 'email': 'john.egglington@emailserve.net'}, {'phone': '1-222-520-4150', 'name': 'Eduardo Salazar', 'email': 'eddy_french@dowdandco.org'}, {'phone': '1-820-444-6718', 'name': 'Monty Dimkpa', 'email': 'cmdimkpa@gmail.com'}]


</pre>

It sure did. How about deleting?

Deleting data:

Let's delete the 2nd row we just edited:

<pre>
>>> RigoDB("delete_entry",{"dbname":"DB_NAME_HERE","dbpassword":"DB_PASSWORD_HERE", "tablename":"table_name_here", "entryPos":1})

'EditTableSuccess: row: 1 of table: TABLE_NAME_HERE was deleted'
</pre>

Let's verify:
<pre>
>>> RigoDB("view_entries",{"dbname":"DB_NAME_HERE","dbpassword":"DB_PASSWORD_HERE", "tablename":"table_name_here", "entryPos":"*"})

[{'phone': '1-800-212-3456', 'name': 'John Egglington', 'email': 'john.egglington@emailserve.net'}, {'phone': '1-820-444-6718', 'name': 'Monty Dimkpa', 'email': 'cmdimkpa@gmail.com'}]
</pre>

The data is no longer there. OK so everything works. For a more comprehensive RigoDB Tutorial, go to the [**RigoDB Github page**](https://github.com/cmdimkpa/Rigo).

Now let's review committing this data to the blockchain.


#### Committing Data to the Blockchain

Prior to committing your data, you can hold it in your RigoDB tables and databases without limit. Once you commit, however, the data disappears from your local persistence and is transferred to the Blockchain.

You can either **commit a table** or **commit a database**:

1. Committing a table

For example, let's commit our sample table:

<pre>
>>> RigoDB("commit_table",{"dbname":"DB_NAME_HERE","dbpassword":"DB_PASSWORD_HERE", "tablename":"table_name_here"})

'the table: [TABLE_NAME_HERE] was committed to the blockchain and deleted from database: [DB_NAME_HERE]'

</pre>

Let's see if we can still access the table:

<pre>
>>> RigoDB("view_entries",{"dbname":"DB_NAME_HERE","dbpassword":"DB_PASSWORD_HERE", "tablename":"table_name_here", "entryPos":"*"})

'TableAccessError: table not found'
</pre>

So the table is gone, as expected.

Now, the table was pointing to a block called "TARGET_BLOCK_HERE", so let's quickly see if we can fetch the data from this block on the blockchain:

<pre>
>>> return_one_tx("TARGET_BLOCK_HERE")

[{u'phone': u'1-800-212-3456', u'name': u'John Egglington', u'email': u'john.egglington@emailserve.net'}, {u'phone': u'1-820-444-6718', u'name': u'Monty Dimkpa', u'email': u'cmdimkpa@gmail.com'}]

</pre>

So this worked perfectly.

2. Committing a database

Committing a database effectively commits all the tables in the database, before removing it from RigoDB persistence. 

Let's go ahead and just commit our test database:

<pre>
>>> RigoDB("commit_database",{"dbname":"DB_NAME_HERE","dbpassword":"DB_PASSWORD_HERE"})

'the database: [DB_NAME_HERE] was committed to the blockchain and deleted from your Rigo instance'

</pre>

A quick check if its still there:

<pre>
>>> RigoDB("view_entries",{"dbname":"DB_NAME_HERE","dbpassword":"DB_PASSWORD_HERE", "tablename":"table_name_here", "entryPos":"*"})

'DBAccessError: could not connect to database [not found]'
</pre>

OK, so that's how to use BlockMagic and RigoDB in a nutshell.

Data transport to the blockchain is fully managed by a connection manager and reporting tool that displays status in your terminal. If you have just created the block, the connection manager will keep retrying until the block is available, then it will send all the data. In general, your data is always reliably delivered to the block.

An example process output:

<pre>
retrying...
{u'message': u'Ledger updated', u'code': 201} (target: http://monty.link/2iSkFewPh2/626c6f636b5f696e666f3a70686f6e653d312d3830302d3231322d33343536266e616d653d4a6f686e204567676c696e67746f6e26656d61696c3d6a6f686e2e6567676c696e67746f6e40656d61696c73657276652e6e6574)
{u'message': u'Ledger updated', u'code': 201}
{u'message': u'Ledger updated', u'code': 201}
{u'message': u'Ledger updated', u'code': 201}
</pre>

#### Data security

BlockMagic encrypts your data as a "hash" before sending e.g. 

<pre>
626c6f636b5f696e666f3a70686f6e653d312d3830302d3231322d33343536266e616d653d4a6f686e204567676c696e67746f6e26656d61696c3d6a6f686e2e6567676c696e67746f6e40656d61696c73657276652e6e6574
</pre>

So your data is private (encrypted) even on an open connection. Also, the client builds a "tunnel" connection to the blockchain. Any blocks created using that tunnel can only be reached via that tunnel. The tunnel is effectively a public key - private key connection between your terminal and the blockchain. This ensures that another device or user cannot access your blocks.

### Retrieving data: transactions and ledgers

You can access your data as a `transaction` or a `ledger`. Transactions are stored the same way you sent them, while ledgers have been grouped by field, allowing you to access aggregated data for applications that require that format.

There are 4 convenience functions you can use to retrieve data: `return_all_tx`, `return_one_tx`, `return_all_lx`, and `return_one_lx`. As you might have guessed, these allow you to: return all transactions, return one transaction, return all ledgers and return one ledger, respectively.

For this example, we have created a block called "WebDirectory" and saved some data to it. Let's explore some scenarios for retrieving our data:

1. store "WebDirectory" in a variable e.g.

<pre>
phonebook = return_one_tx("WebDirectory")
print phonebook
</pre>

Sample output:
<pre>
>>> phonebook
[{u'phone': u'1-800-212-3456', u'name': u'John Egglington', u'email': u'john.egglington@emailserve.net'}, {u'phone': u'1-616-420-1123', u'name': u'Mary Tipton', u'email': u'mary_tipton@dowdandco.org'}, {u'phone': u'1-820-444-6718', u'name': u'Monty Dimkpa', u'email': u'cmdimkpa@gmail.com'}]
</pre>

Notice the data was returned the way it was sent. With a ledger, it will be grouped:

<pre>
phonebook = return_one_lx("WebDirectory")
print phonebook
</pre>

Sample output:
<pre>
>>> phonebook
{u'phone': [u'1-800-212-3456', u'1-616-420-1123', u'1-820-444-6718'], u'name': [u'John Egglington', u'Mary Tipton', u'Monty Dimkpa'], u'email': [u'john.egglington@emailserve.net', u'mary_tipton@dowdandco.org', u'cmdimkpa@gmail.com']}
</pre>

Note: if you are operating on a terminal, you might see some diagnostic messages during operation. Simply ignore them as your data will always be saved to the variable you have declared.

So far, we have returned one transaction and one ledger. That's because we only have data in one block. Let's store some data in the "Logins" block, so we can demonstrate returning all transactions and all ledgers.

<pre>
SampleLogins = [
  {"user":"altair444", "pass":"ojwfjefjoejfeojf8765"},
  {"user":"shazam67@y", "pass":"lacazaette686"},
  {"user":"romulusTiDer", "pass":"kljwdkwjdwdjd675"}
]
</pre>

<pre>
send_data("Logins",SampleLogins)
</pre>

Sample output:

<pre>
retrying...
{u'message': u'Ledger updated', u'code': 201} (target: http://monty.link/pZt6b4sX7/626c6f636b5f696e666f3a757365723d616c7461697234343426706173733d6f6a77666a65666a6f656a66656f6a6638373635)
{u'message': u'Ledger updated', u'code': 201}
{u'message': u'Ledger updated', u'code': 201}
{u'message': u'Ledger updated', u'code': 201}
</pre>

So, we have some sample login data on the blockchain. Now's let retrieve it in our application:

<pre>
logins = return_one_tx("Logins")
print logins
</pre>

Output:
<pre>
>>> logins
[{u'user': u'altair444', u'pass': u'ojwfjefjoejfeojf8765'}, {u'user': u'shazam67@y', u'pass': u'lacazaette686'}, {u'user': u'romulusTiDer', u'pass': u'kljwdkwjdwdjd675'}]
</pre>

Additionally, since we have more than one block, we can use the `return_all` functions:

1. Return all transactions

<pre>
transactions = return_all_tx()
print transactions
</pre>

Sample output:

<pre>
>>> transactions
{u'logins': [{u'user': u'altair444', u'pass': u'ojwfjefjoejfeojf8765'}, {u'user': u'shazam67@y', u'pass': u'lacazaette686'}, {u'user': u'romulusTiDer', u'pass': u'kljwdkwjdwdjd675'}], u'webdirectory': [{u'phone': u'1-800-212-3456', u'name': u'John Egglington', u'email': u'john.egglington@emailserve.net'}, {u'phone': u'1-616-420-1123', u'name': u'Mary Tipton', u'email': u'mary_tipton@dowdandco.org'}, {u'phone': u'1-820-444-6718', u'name': u'Monty Dimkpa', u'email': u'cmdimkpa@gmail.com'}]}
</pre>

Notice that this combines data from "WebDirectory" and "Logins" blocks.

2. Return all ledgers (grouped data)

<pre>
ledgers = return_all_lx()
print ledgers
</pre>

Sample output:

<pre>
>>> ledgers
{u'logins': {u'user': [u'altair444', u'shazam67@y', u'romulusTiDer'], u'pass': [u'ojwfjefjoejfeojf8765', u'lacazaette686', u'kljwdkwjdwdjd675']}, u'webdirectory': {u'phone': [u'1-800-212-3456', u'1-616-420-1123', u'1-820-444-6718'], u'name': [u'John Egglington', u'Mary Tipton', u'Monty Dimkpa'], u'email': [u'john.egglington@emailserve.net', u'mary_tipton@dowdandco.org', u'cmdimkpa@gmail.com']}}
</pre>

Notice that the data for each block has been grouped. Nice and easy.

### Benefits

BlockMagic allows you to securely and conveniently store your data in a blockchain. With RigoDB, an add-on product, you can enjoy traditional CRUD database facilities prior to immutable data commits to the blockchain. You can use BlockMagic or  [**RigoDB**](https://github.com/cmdimkpa/Rigo) seamlessly in your Python2 code while building web applications. No fancy configurations, accounts or registration required. No fees or gimmicks -- Just easy data storage and retrieval.

### Connect
Send questions or comments to: cmdimkpa (at) gmail.com

Happy I/O !
