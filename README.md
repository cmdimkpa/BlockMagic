# BlockMagic for Python
## Simple & Fast Web I/O on a Secure Blockchain
**BlockMagic** is an I/O Client for secure data storage and retrieval on the [Monty.Link] Blockchain. It delivers fast data I/O for web and mobile applications while ensuring security and privacy of your data.

[Monty.Link] is a blockchain for secure data storage. It is currently in beta. Disclaimer: while we support public use of the blockchain for educational or commercial projects and do not track or use the data you submit to the platform in any way, we are not liable for any challenges arising from loss of service or data. Do not store sensitive or confidential information on [Monty.Link].

### Getting Started

Install BlockMagic from Pip:

<pre>
  pip2 install block_magic
</pre>

Requires: Python 2

### Using BlockMagic

To use BlockMagic after installation via Pip, import the client in your Python2 code:

<pre>
  from block_magic.blockmagic_client import *
</pre>

### Storing data: creating blocks and sending data

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

Once you mine (create) a block, it takes up to a minute to be registered on the blockchain. The client automatically manages the connection in case you want to send data immediately.

Your data is not public as it cannot be accessed from any device terminal other than the one used to create the block. Even if you use another terminal on the same device, the data will not be available. So the communication is a closed I/O circuit.

#### Sending Data

To send data, use the `SendData` command. Data must be sent as a list of records. e.g.

<pre>
myContacts = [
    {
      "name":"John Egglington",
      "phone":"1-800-212-3456",
      "email":"john.egglington@emailserve.net"
    },
    {
      "name":"Mary Tipton",
      "phone":"1-616-420-1123",
      "email":"mary_tipton@dowdandco.org"
    },
    {
      "name":"Monty Dimkpa",
      "phone":"1-820-444-6718",
      "email":"cmdimkpa@gmail.com"
    }
  ]

SendData("WebDirectory",myContacts)
</pre>

### Retrieving data: transactions and ledgers

### Public usage
You are free to use this application in your Python projects. Other clients will be developed to manage connections from other environments (Node.js, etc) soon.

### Keep in touch
Send questions or comments to: cmdimkpa@gmail.com

Happy I/O !
