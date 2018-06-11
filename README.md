# BlockMagic for Python
## Simple & Fast Web I/O on Secure Blockchain
**BlockMagic** is a blockchain for secure data storage and retrieval. It delivers fast data I/O for web and mobile applications while ensuring security and privacy of your data.

BlockMagic is based on a real blockchain: To save data to the blockchain, your Python client (BlockMagic for Python) creates a **block** in the blockchain using public-key encryption. The tedious details are abstracted between the Core API/Client interaction, so you only need to do this:

<code>
  from block_magic.blockmagic_client import *
</code>

You can use the created block for a practical purpose such as "Web Phone Book", "Sales Data" or "Shipping Logs", etc. You can then simply prepare a list of records you want to upload to the block and send using a convenient function.
