from cryptography.fernet import Fernet
def generate_key():
    key = Fernet.generate_key()
    with open("secret.key", "wb") as key_file:
        key_file.write(key)
def load_key():
    return open("secret.key", "rb").read()
def encrypt_message(message):
    key = load_key()
    b_str = message.encode()
    f = Fernet(key)
    encrypted_message = f.encrypt(b_str)
    # return encrypted_message
    str=encrypted_message.decode()
    return str
def decrypt_message(str):
    b_str = str.encode()
    key = load_key()
    f = Fernet(key)
    decrypted_message = f.decrypt(b_str)
    str = decrypted_message.decode()
    return str

a='9 vy hẻo vy heo lùn vy lủn hahah vy lun'
a = encrypt_message(a)
# a = a.split()
# print(a)
#print(s)
t=decrypt_message(a)
print(t)

