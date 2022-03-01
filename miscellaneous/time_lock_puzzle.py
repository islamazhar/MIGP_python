import sys
import os
import time 
import math

from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.fernet import Fernet


def get_num_of_squrings_per_second():
    n = 3285786053995291024746162597110139412838358775272661892775318107716191165344927757345427848056382702611991217548482991736509021625883645212790106454545497195017585448145132044372738578827498791930212402916426347131925707508686126258711062943826207298871116237649487808488101857320151400666496185978220744216918012409405023720639163175134283285977024560020603331651945308417543743975305059763361789414638183571059108305033939188405817948413256740933413802758632166075708563379039537804587526116083554909789436521105110172213373907311700810166371533442335737733231794866653580261678405035083063475513253336848748251848286963662259982416924019902436644335581946397155297493728061475695395021304823
    x = 58798929645077175193759242213234182565494662554979942504157005935506083646878
    total = 0
    for _ in range(1000):
        s1 = time.time()
        x = x**2
        x = x%n
        s2 = time.time()
        total += (s2 - s1)
    return math.ceil(1000/total)

def successive_squares(base, mod, length):
    table = [base % mod]
    prev = base % mod
    for n in range(1, length):
        squared = prev**2 % mod
        table.append(squared)
        prev = squared
    return table
    

def fast_exponentiation(n, g, x):
    # reverses binary string
    binary = bin(x)[2:][::-1]
    squares = successive_squares(g, n, len(binary))
    # keeps positive powers of two
    factors = [tup[1] for tup in zip(binary, squares) if tup[0] == '1']
    acc = 1
    for factor in factors:
        acc = acc * factor % n
    return acc


def time_lock_message(message, T, S):
        print('locking the puzzle')
        private_key = rsa.generate_private_key(
                public_exponent=65537,
                key_size=2048
                #backend=default_backend()
            )
        p, q = private_key.private_numbers().p,  private_key.private_numbers().q
        phi_n = (p-1)*(q-1)
        #print(phi_n)



        key = Fernet.generate_key()
        K = int.from_bytes(key, sys.byteorder)
        #print(K)
        cipher_suite = Fernet(key)



        #print(message, key)
        message = message.encode()
        C_M = cipher_suite.encrypt(message)


        t = T * S
        n  = private_key.public_key().public_numbers().n 
        e = fast_exponentiation(phi_n, 2, t)
        a = int.from_bytes(os.urandom(32), sys.byteorder) % n + 1

        C_K = (K%n +  fast_exponentiation(n, a, e))%n

        return C_M, C_K, t, a, n

def time_unlock_message(C_M, C_K, t, a, n):
    b = a%n
    for _ in range(t):
        b  = b**2
        b = b % n
    K = (C_K - b) % n
    #print(K)
    #K_bytes = bytearray.fromhex('{:0192x}'.format(K))
    K_bytes = int.to_bytes(K, length=K.bit_length(), byteorder=sys.byteorder)
    #print(K_bytes)
    cipher_suite = Fernet(K_bytes)
    return  cipher_suite.decrypt(C_M)


message = "This is a time lock puzzle2"
T = 7 # 5s to crack the value...
#S = 92592 # expected number of squring per seconds
#S = 2570694
S = get_num_of_squrings_per_second()
print(S)

C_M, C_K, t, a, n = time_lock_message(message, T, S)
print(a)
print(n)
print("unlocking the puzzle")
s1 = time.time()
out = time_unlock_message(C_M, C_K, t, a, n)
s2 = time.time()
print(out)
print(s2-s1)


