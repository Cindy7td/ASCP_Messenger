import pyDes

key_hex= "5ca85bccd4c387"
key = bytes(key_hex,'utf-8')
print(len(key))
data = "Please encrypt my data"
k = pyDes.des(key, pyDes.ECB, "\0\0\0\0\0\0\0\0", pad=None, padmode=pyDes.PAD_PKCS5)
d = k.encrypt(data)
print ("Encrypted: %r" % d)
print ("Decrypted: %r" % k.decrypt(d))

