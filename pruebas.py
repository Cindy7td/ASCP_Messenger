#import pyDes

#key_hex= "ff5ca85bccd4c387"
#key = bytes.fromhex(key_hex)
#print(len(key))
#print(key)

#bytes.fromhex(key)  
#bytearray.fromhex(hex_string)


#x = 50
#xton = chr(x)
#chr(x)
#print(x)
#print(xton)
q=353
x= 233
alpha= 3
def diffiehellman(alpha, x, q):
    #Es alpha a la x mod q
    if x == 0: 
        return 1
        
    else:
        if x % 2 == 0: 
            multi = (alpha * alpha)
            mod = multi % q
            div = x / 2
            return diffiehellman(mod, div, q)
        else:
            return alpha * diffiehellman(alpha, x - 1, q) % q

def keyis(key, x, q): 
    ### k a la x mod q
    if x == 0: 
        return 1
    else:
        if x % 2 == 0: 
            keys = key * key
            div = x / 2
            mod = keys % q
            return keyis(mod, div, q)
        else:
            return key * keyis(key, x - 1, q) % q



key1 = diffiehellman(alpha,x,q)
print(key1)
ks = diffiehellman(key1,x,q)
print(ks)