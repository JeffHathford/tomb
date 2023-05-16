from utility import *
from encryption import *
import signal
import sys
import random

def signal_handler(sig, frame):
    print('Exit signal received, closing...')
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

print("Running preconfig...")

#check for keys, create new if not found
if not os.path.exists(".\keys"):
    if confirm_dialogue("'keys' folder was not found. Do you want to create a new one? Y/n\n"):
        os.mkdir("keys")
        os.mkdir("keys\\foreign")
        write_keys_to_file(generate_keypair(), ".\\keys\\")

exit_flag = False
while not exit_flag:
    clear()

    print(f"""
    TOMB ver. 0.1
    Asymmetric encryption utility

    Select an option from the list below:

    1 - Generate a new keypair
    2 - Decrypt a .tomb archive from this directory
    3 - Encrypt files from this directory
    4 - Check what files TOMB can see

    0 - Quit applicatoin

    """)

    input_flag = False
    while not input_flag:

        input_flag = True
        option = input()

        # 1 - Generate new keypair
        if option == "1":
            write_keys_to_file(generate_keypair(), ".\\keys\\")

        # 2 - Decrypt files
        elif option == "2":
            archives_to_decrypt = get_file_list(".tomb")
            if len(archives_to_decrypt) != 0:
                decrypt_files(archives_to_decrypt)
            else:
                print("No .tomb archives found in current folder.")
                wait_for_enter()

        # 3 - Encrypt files
        elif option == "3":
            tidy_foreign_keys()
            files_to_encrypt = [f for f in get_file_list() if not f.endswith(".tomb") 
                                and not f.endswith(".py") and f != os.path.basename(sys.executable)]

            if len(files_to_encrypt) > MAX_ENCRYPT_FILE_QTY:

                print(f"""
                There are more than {MAX_ENCRYPT_FILE_QTY} encryptable files
                in current folder. Consider archiving them with another application
                such as 7zip and then using TOMB.
                """)

                wait_for_enter()
                continue

            if len(files_to_encrypt) == 0:
                print("No files to encrypt.")
                wait_for_enter()
                continue

            print("Encrypting files listed below:\n")
            for file in files_to_encrypt:
                print(file)
            
            if not confirm_dialogue("\nProceed? Y/n\n"):
                continue

            foreign_key = load_foreign_key(user_select_foreign_key())

            encrypt_files(files_to_encrypt, foreign_key)

        # 4 - ask TOMB what files it can see
        elif option == "4":
            files = get_file_list()

            print("TOMB can see files listed below:\n")

            for file in files:
                print(file, end="")
                if file.endswith(".tomb") or file.endswith(".py"):
                    print(" - IGNORED")
                else:
                    print()

            print()
            wait_for_enter()

        elif option == "0":
            exit_flag = True
            if random.randint(1,100) == 100:
                print("The Nile flows...")
        
        else:
            input_flag = False
            print("Invalid input, please try again\n")