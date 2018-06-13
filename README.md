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

### Retrieving data: transactions and ledgers

### Public usage
You are free to use this application in your Python projects. Other clients will be developed to manage connections from other environments (Node.js, etc) soon.

### Keep in touch
Send questions or comments to: cmdimkpa@gmail.com

Happy I/O !
