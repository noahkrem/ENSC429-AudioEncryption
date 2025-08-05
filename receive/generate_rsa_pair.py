import os
from Crypto.PublicKey import RSA
import shutil

# Generate the RSA key pair
def generate_RSA_pair():
    if not (os.path.exists("rsa_public.pem") and os.path.exists("rsa_private.pem")):
        rsa_key = RSA.generate(2048)  # 2048-bit is fine for key wrapping
        with open("rsa_private.pem", "wb") as f:
            f.write(rsa_key.export_key())
        with open("rsa_public.pem", "wb") as f:
            f.write(rsa_key.publickey().export_key())
        print("RSA key pair generated.")
    else:
        print("RSA key pair already exists.")

if __name__ == "__main__":
    generate_RSA_pair()

    # Transmit the public key to the transmitter
    destination_folder = '../transmit'
    shutil.copy('rsa_public.pem', destination_folder)
