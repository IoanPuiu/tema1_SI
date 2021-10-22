import socket
import settings
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes


def bytes_xor(bytes1, bytes2):
    if len(bytes1) != len(bytes2):
        return None
    return bytes([b1 ^ b2 for b1, b2 in zip(bytes1, bytes2)])


def decript_key(k):
    cipher = Cipher(algorithms.AES(settings.k_prim), modes.ECB(), default_backend())
    decryptor = cipher.decryptor()
    k = decryptor.update(k)
    return k


def main():
    s = socket.socket()
    host = socket.gethostname()
    port = 9600
    s.connect(("localhost", port))

    mode = s.recv(3).decode('utf-8')
    k_crypt = s.recv(16)
    k = decript_key(k_crypt)
    print("Putem incepe comunicarea")
    s.send("Putem incepe comunicarea".encode())

    if mode == 'ECB':
        block = s.recv(16)
        cipher = Cipher(algorithms.AES(k), modes.ECB(), default_backend())
        decryptor = cipher.decryptor()
        while len(block) == 16:
            dect = decryptor.update(block)
            print(dect.decode('utf-8'))
            block = s.recv(16)

    if mode == 'CBC':
        block = s.recv(16)
        block_cp = settings.vi
        cipher = Cipher(algorithms.AES(k), modes.ECB(), default_backend())
        decryptor = cipher.decryptor()
        while len(block):
            dect = decryptor.update(block)
            dect = bytes_xor(dect, block_cp)
            print(dect.decode())
            block_cp = block
            block = s.recv(16)

    s.close()


main()
