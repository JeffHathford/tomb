from utility import *
import os
import base64
import cryptography
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding

def RSA_encrypt(data, foreign_key):
    encrypted = foreign_key.encrypt(
                    data,
                    padding.OAEP(
                        mgf=padding.MGF1(algorithm=hashes.SHA256()),
                        algorithm=hashes.SHA256(),
                        label=None
                    )
                )
    
    encoded = base64.b64encode(encrypted)
    return encoded

def RSA_decrypt(data, private_key):
    decoded = base64.b64decode(data)
    decrypted = private_key.decrypt(
                    decoded,
                    padding.OAEP(
                        mgf=padding.MGF1(algorithm=hashes.SHA256()),
                        algorithm=hashes.SHA256(),
                        label=None
                    )
    )
    return decrypted
    
def symmetric_encrypt(data, fernet_key):
    fernet = Fernet(fernet_key)
    encrypted = fernet.encrypt(data)

    return encrypted

def symmetric_decrypt(data, fernet_key):
    fernet = Fernet(fernet_key)
    decrypted = fernet.decrypt(data)

    return decrypted

def encrypt_files(file_list, foreign_key, dst_dir=".\\encrypted\\"):
    #header = f"{len(file_list)}:"
    header = ""

    # create a fresh archive.tomb file
    if not os.path.exists(dst_dir):
        os.mkdir(dst_dir)
    open(dst_dir + "archive.tomb", "wb").close()

    with open(dst_dir + "archive.tomb", "ab") as archive:
        fernet_key = Fernet.generate_key()
        encrypted_fernet_key = RSA_encrypt(fernet_key, foreign_key)

        print(f"Writing symmetric key to archive...")
        archive.write(encrypted_fernet_key + b':')

        for filename in file_list:
            with open (filename, "rb") as file:
                print(f"Encrypting {filename}...")
                file_data = file.read()
                encrypted = symmetric_encrypt(file_data, fernet_key)
                archive.write(encrypted + b';')
                #header += f"{len(encrypted)},{filename}:"
                header += f"{filename}:"

        enc_header = symmetric_encrypt(header.encode("utf-8"), fernet_key)    
        archive.write(b':' + enc_header)

def decrypt_files(file_list, private_key=None, dst_dir=".\\decrypted\\"):
    if private_key == None:
        private_key = load_private_key()

    
    for filename in file_list:
        # subtract .tomb from filename
        subdir_name = f"filename[:-5]\\"
        try:
            with open(filename, "rb") as archive:
                data = archive.read()
                [enc_fernet_key, enc_data, enc_header] = data.split(sep=b':')

                fernet_key = RSA_decrypt(enc_fernet_key, private_key)
                header = symmetric_decrypt(enc_header, fernet_key).decode("utf-8")

                filenames = header.split(sep=":")[:-1]
                enc_file_data = enc_data.split(sep=b';')[:-1]

                if not os.path.exists(dst_dir + subdir_name):
                    os.mkdir(dst_dir + subdir_name)

                for idx, filename in enumerate(filenames):
                    with open(dst_dir + subdir_name + filename, "wb") as file:
                        encrypted = enc_file_data[idx]
                        decrypted = symmetric_decrypt(encrypted, fernet_key)
                        file.write(decrypted)

        except Exception as e:
            print(e)