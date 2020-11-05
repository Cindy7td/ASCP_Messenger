import random
import pyDes


buffer = "11000011111010011000111011011110"
key = 10011
ks= key.to_bytes(8,'big')

k = pyDes.des(ks, pyDes.ECB, "\0\0\0\0\0\0\0\0", pad=None, padmode=pyDes.PAD_PKCS5)
msg = k.decrypt(buffer)
print(msg)