import os
import cryptography
import shutil
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding

FILESIZE_LIMIT_BYTES = 256
CHOICES_YES = ["y", "yes", "yea", "yeah", "ye", "ys"]
MAX_ENCRYPT_FILE_QTY = 5

def clear():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

def wait_for_enter(message="Press Enter to continue..."):
    input(message)

def confirm_dialogue(message, default="y"):
    answer = input(message)
    if answer == "":
        answer = default
    if answer.lower() in CHOICES_YES:
        return True
    return False

def get_file_list(ext=None, dir=".\\"):

    file_list = [file for file in os.listdir(dir)
                 if os.path.isfile(dir + file)]
    
    if ext:
        file_list = [file for file in file_list
                     if file.endswith(ext)]
    
    return file_list

def generate_keypair():
    public_exponent=65537
    key_size=8192

    print(f"Generating new keypair, key size: {key_size} bytes")

    private_key = rsa.generate_private_key(
        public_exponent,
        key_size
    )

    public_key = private_key.public_key()

    return [public_key, private_key]

def write_keys_to_file(key_list, directory):
    print("Writing keypair to files")

    public_key = key_list[0]
    private_key = key_list[1]

    serial_private = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )
    with open(directory + 'private_noshare.pem', 'wb') as f:
        f.write(serial_private)

    serial_pub = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    with open(directory + 'public_shared.pem', 'wb') as f:
        f.write(serial_pub)
    
    #with open(directory + "foreign\\" + 'foreign_RENAME.pem', 'wb') as f:
    #    f.write(serial_pub)

def load_private_key (filename = "private_noshare.pem"):

    directory = ".\\keys\\"

    print(f"Loading private key from \'{directory + filename}\'")

    with open(directory + filename, "rb") as key_file:
        private_key = serialization.load_pem_private_key(
            key_file.read(),
            password=None
        )

    return private_key
                  
def load_public_key (filename = "public_shared.pem"):

    directory = ".\\keys\\"

    print(f"Loading public key from \'{directory + filename}\'")

    with open(directory + filename, "rb") as key_file:
        public_key = serialization.load_pem_public_key(
            key_file.read()
        )

    return public_key

def load_foreign_key (filename = "foreign_public.pem"):

    if filename == -1:
        return -1

    directory = ".\\keys\\foreign\\"

    print(f"Loading foreign key from \'{directory + filename}\'")

    try:
        with open(directory + filename, "rb") as key_file:
            foreign_key = serialization.load_pem_public_key(
                key_file.read()
            )

        return foreign_key
    
    except (FileNotFoundError):
        print(f"\'{filename}\' not found. Make sure to place said file in this folder.")
        return

def user_select_foreign_key ():
    foreign_keys = get_file_list(".pem", ".\\keys\\foreign\\")

    if len(foreign_keys) == 0:
        print("""
        No foreign keys detected. Please refer to README.txt on how to solve this issue.
        """)
        return -1

    print("List of stored foreign keys:\n")
    for key in foreign_keys:
        print(key[8:-4])

    target = input("\nType in the name of the foreign key you want to use for encryption:\n")
    key_name = f"foreign_{target}.pem"

    if key_name not in foreign_keys:
        print(f"Key \'{key_name}\' not found.\nPress Enter to continue...")
        input()
        return None
    
    else:
        return key_name
    
def tidy_foreign_keys():
    keys_in_pwd = [file for file in get_file_list(".pem") if file[:8] == "foreign_"]
    if len(keys_in_pwd) > 0:
        for file in keys_in_pwd:
            shutil.move(os.path.join(".", file), ".\\keys\\foreign\\")