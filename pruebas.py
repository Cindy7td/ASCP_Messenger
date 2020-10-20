import random

def diffiehellman(alpha, x, q):
    #Es y a la x mod q
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


x = 44513708
q = 2426697107
alpha = 1460011294

#random.randint(1,q-1)
prueba = pow(x, alpha, q)
df = diffiehellman(x, alpha, q)
print(df)

print(prueba)