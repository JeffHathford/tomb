Before using this application to encrypt or decrypt files, make sure that you have a valid
pair of RSA keys in your \keys folder. If you're not sure, use the application to
generate a new keypair.

WARNING
Generating a new keypair will make you unable to receive files encrypted with your previous keys.
Make sure to share a fresh copy of your public key with any potential senders.

How to encrypt and share files:
1. Ask the receiving user for a copy of their public key
2. Place the copy in 'keys\foreign' and name it 'foreign_<something>.pem'
   <something> means a name by which you can identify the other person
3. Place files that you want to send in the same directory as the application
   Note: .py files will not be attached and need to be archived or renamed
4. Launch the application and select "Encrypt files from this directory"
5. Review the file list and proceed
6. Type in the name of the received public key copy, earlier denoted by <something>
7. Application will create an 'archive.tomb' file in \encrypted folder
8. Send the file to the other user

How to receive and decrypt files:
1. Send the file-sending user a copy of your public key, name it 'foreign_<something>.pem'
2. Wait for the other user to send you an 'archive.tomb' file
3. Launch the application and select "Decrypt a .tomb archive from this directory"
4. Decrypted files will be placed in \decrypted folder