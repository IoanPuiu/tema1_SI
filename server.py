import socket
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import settings


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
    mode = "ECB"

    skm = socket.socket()
    host = socket.gethostname()
    port = 1234
    skm.connect((host, port))
    k_crypt = skm.recv(16)
    skm.close()

    s = socket.socket()
    port_client = 9600
    s.bind(("localhost", port_client))

    s.listen(5)

    c, a = s.accept()

    c.send(mode.encode())

    k = decript_key(k_crypt)
    c.send(k_crypt)
    resp = c.recv(24).decode('utf-8')
    if resp == 'Putem incepe comunicarea':
        print(resp)
        file = open("message.txt")
        block = file.read(16)
        if mode == "ECB":
            cipher = Cipher(algorithms.AES(k), modes.ECB(), default_backend())
            encryptor = cipher.encryptor()
            while len(block) == 16:
                ct = encryptor.update(block.encode())
                c.send(ct)
                block = file.read(16)
            else:
                if len(block) != 0:
                    while len(block) != 16:
                        block += '\0'
                    ct = encryptor.update(block.encode())
                    c.send(ct)
        if mode == "CBC":
            cipher = Cipher(algorithms.AES(k), modes.ECB(), default_backend())
            encryptor = cipher.encryptor()
            ct = settings.vi
            while len(block) == 16:
                block = bytes_xor(block.encode(), ct)
                ct = encryptor.update(block)
                c.send(ct)
                block = file.read(16)
            else:
                if len(block) != 0:
                    while len(block) != 16:
                        block += '\0'
                    block = bytes_xor(block.encode(), ct)
                    ct = encryptor.update(block)
                    c.send(ct)

    c.close()
    s.close()


main()
