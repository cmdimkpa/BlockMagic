# BlockMagic for Python
## Simple & Fast Web I/O on Secure Blockchain
**BlockMagic** is a blockchain for secure data storage and retrieval. It delivers fast data I/O for web and mobile applications while ensuring security and privacy of your data.

Install from Pip:

<pre>
  pip install block_magic
</pre>

Requires: Python 2.7

To use within Python 2.7, import the client:

<pre>
  from block_magic.blockmagic_client import *
</pre>

BlockMagic is based on a real blockchain: To save data to the blockchain, your Python client (BlockMagic for Python) creates a **block** in the blockchain using public-key encryption. The tedious details are abstracted between the Core API/Client interaction, so you only need to do this:

<pre>
  print CreateBlock("block_name","block_description")
</pre>

The "print" allows you to see the output of the command. For scripting you can just trap the output.

You can use the created block for a practical purpose such as "Web Phone Book", "Sales Data" or "Shipping Logs", etc:

<pre>
  print CreateBlock("WebPhoneBook","web store for my contacts data")
</pre>

<pre>
  <b>Output: </b>the block [webphonebook] was registered on the blockchain
</pre>

<b>A note on data security: </b> Only you can access the data you store on the blockchain. In fact, you must use the same machine or terminal you used to create the block to be able to access the data you saved on that block. There are no public methods for accessing data on the blockchain, as you must supply a block key (your client does this for you) to the block chain, and the supplied key must match the private key the blockchain tracks for your device or terminal. It is a closed data circuit.

Also, because the blockchain is immutable, the data you have saved on it cannot change, except you wish to add new data to your block, or create a new block.

Now let's demonstrate how to send some data to your block. Let's prepare some sample data:

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
</pre>

Note that you should always package your data as a list of records, even if you have a single record.

Sending data to the block is as simple as:

<pre>
  SendData("WebPhoneBook",myContacts)
</pre>
