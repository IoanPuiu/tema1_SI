import socket
import os
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import settings


def make_k():
    k = os.urandom(16)

    # if mode == "ECB":
    cipher = Cipher(algorithms.AES(settings.k_prim), modes.ECB(),default_backend())
    encryptor = cipher.encryptor()
    k = encryptor.update(k)
    return k
    # if mode == "CBC":
    #     cipher = Cipher(algorithms.AES(k_prim), modes.CBC(vi))
    #     encryptor = cipher.encryptor()
    #     k = encryptor.update(k) + encryptor.finalize()
    #     return k


def main():
    s = socket.socket()
    host = socket.gethostname()
    port = 1234
    s.bind((host, port))
    s.listen(5)
    c, addr = s.accept()

    k = make_k()
    c.send(k)

    c.close()
    s.close()


main()
