Cyphers!

This is a python program that encrypts, decrypts, and cracks cyphers.
So far, I have the...
Ceasar,
and Vigenere,
Cyphers.

Command Examples
First download my files to a happy directory on your computer.
Change your directory to your happy directory.
If you are in Linux, open your command terminal and type...
python3
If you are in Windows, open your python IDE!

To setup the object type the following commands...
from Cyphers import Cryptonomicon
C = Cryptonomicon()

To encrypt the Ceasar Cypher type...
message = 'encrypt me please i want to be encrypted'
key = 12
cypher = C.EncryptCeasar(key, message)

You can print the variable, "cypher." It should look something
like qzodkbfyqbxqmequimzffanqqzodkbfqp
To decrypt this cypher, you can type...
m = C.DecryptCeasar(key, cypher)

You can also automatically crack the ceasar cypher by typing...
C.CrackCeasar(cypher)

You will get a key returned. You can push that key into
the decryption function.

If you print m, you will get something like...
encryptmepleaseiwanttobeencrypted
This looks hard to read. So, I wrote a word tokanizer.
This tokanizer isn't the best. However, it helps.
To use the tokanizer type...
C.TokanizeWords(m)

The Tokanizer may take a while depending on how long
the message is. The result for this case would be
something like 'en crypt me please i want to been crypt e d'
I guess you cannot win them all. Not all words are
lexiconed. So, let us add our needed words by typing...
C.AddWord(20, 'encrypt')
C.AddWord(20, 'encrypted'

The 20 is just the percentage that places the word in the
priority list. So, the less percent, the higher the word is
prioritized. I chose 20% as a rule of thumb. If you
tokanize again, you will see. encrypt me please i want to
be encrypted. Not so bad, huh?
