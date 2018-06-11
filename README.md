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

You can then simply prepare a list of records you want to upload to the block and send using a convenient function.
