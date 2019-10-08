import base64
import os
import secrets
import sys
import time
from getpass import getpass
import cryptography
import cryptography.hazmat.backends
import cryptography.hazmat.bindings
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC  # I know, cryptography is shittily structured.
import _cffi_backend
import idna.idnadata

# I know it looks like I accidentally left dead imports in here, but they're actually necessary for cx_Freeze to work
# properly. But pycharm isn't great at recognizing that.

if getattr(sys, 'frozen', False):  # This is a little compatiblility line for os.path.dirname to figure out where we are
    # even if the code is running from a frozen .exe
    boi = os.path.dirname(os.path.abspath(sys.executable))
else:
    boi = os.path.dirname(os.path.abspath(__file__))


def encrypt(fi, password):
    """
    encrypts file designated by fi
    :param password: str
    :type fi: str
    """

    salt = bytes(secrets.token_hex(256), "utf-8")  # Generates the SALT.
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA512(),
        length=32,
        salt=salt,
        iterations=1000000,
        backend=default_backend()
    )  # This is the definition of our key derivation function. Length is the size of our key itself.
    #  the iterations is how many times the encryption algorithm is run over the entire document.
    key = base64.urlsafe_b64encode(kdf.derive(bytes(password, "utf-8")))

    with open(fi, "r+b") as f:
        snek = f.read()
        token = Fernet(key).encrypt(snek)
        f.seek(0)
        f.write(salt + b"(SALT)" + token)  # This is the best way to write to a .txt without accidentally
        # leaving it open and accessible via memory.
    print("SUCCESSFULLY ENCRYPTED")
    input("Press Enter to Continue")


def decrypt(fi, password):
    with open(fi, "rb+") as f:
        j = f.read()
        sea = j[0:512]
        text = j[518:]
        # This reads and discerns the important portions of our file. Get it, sea salt?
    salt = bytes(secrets.token_hex(256), "utf-8")  # Generates the salt four our re-encryption.
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA512(),
        length=32,
        salt=sea,
        iterations=1000000,
        backend=default_backend()
    )
    kdf2 = PBKDF2HMAC(
        algorithm=hashes.SHA512(),
        length=32,
        salt=salt,
        iterations=1000000,
        backend=default_backend()
    )  # First one is for decryption, and therefore uses the old SALT, sea, and the second one uses the new SALT, salt.

    key = base64.urlsafe_b64encode(kdf.derive(bytes(password, "utf-8")))
    key2 = base64.urlsafe_b64encode(kdf2.derive(bytes(password, "utf-8")))  # Turns the salts into keys, using the
    # Password, which is taken as an input to encrypt() and decrypt().
    out = Fernet(key).decrypt(text)
    print(str(out, "utf-8"))  # Display
    with open(fi, "wb") as s:
        nout = out
        del nout
        s.write(out)  # Writes it down, erasing the encryption.
    j = input("Press Enter to re-encrypt or enter 'n' to enter a new line")
    if j is "n":
        newline = bytes("\n" + input("NEW LINE: "), "utf-8")
        with open(fi, "wb") as s:
            nout = out + newline
            encout = Fernet(key2).encrypt(nout)
            del nout
            s.write(salt + b'(SALT)' + encout)
        print("New line successfully added and file re-encrypted.")  # Erases the plaintext, and leaves an
        # encryption.
    else:
        with open(fi, "wb") as s:
            encout = Fernet(key2).encrypt(out)
            del out
            s.write(salt + b'(SALT)' + encout)  # Final output.


def filechk():
    os.chdir(boi)
    for file in os.listdir(boi):
        if file.endswith(".txt"):
            return os.path.join(boi, file)


def main():
    if filechk() is None:
        open(boi + "/SECRETSTUFF.txt", "w")
        print("No file to encrypt was found, an empty file was created. Run this program again to encrypt it.")
        time.sleep(5)
        sys.exit(0)
    else:
        gr = filechk()  # Checks for a file, and sets the target (gr) to that file.

    with open(gr, "rb") as k:
        noot = k.read()
        pork: bool = noot[512:518] == b"(SALT)"  # I don't have a good reason for calling it "pork" This uses a lil
        # tagging system to check to see if the file is plaintext or encrypted text.

    if pork:
        while True:
            try:
                password = getpass("PASSWORD: ")
                decrypt(gr, password)
                sys.exit(0)
            except cryptography.fernet.InvalidToken:
                print("You've entered the wrong password, try again")
                continue
    if not pork:
        password = getpass("PASSWORD: ")
        encrypt(gr, password)  # Where the pork turns into meat. This part runs the correct function depending on the
        # situation. If the "(SALT)" tag exists, then it decrypts, if it doesn't then it encrypts.


if __name__ == "__main__":
    main()
    sys.exit(0)  # This is a python trick that lets you run a script from another script. I doubt it'll come up but just
    # In case I included that as an option.
