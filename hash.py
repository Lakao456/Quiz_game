import pickle
import hashlib

crypt = hashlib.md5()
crypt.update(b"1234")  # password
with open("password.txt", 'wb') as file:
    pickle.dump(crypt.hexdigest(), file)

with open("password.DAT", 'rb') as file:
    if hashlib.md5(input("enter password").encode()).hexdigest() == pickle.load(file):
        print('Correct')

