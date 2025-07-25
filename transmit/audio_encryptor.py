import os
import random
import string
from scipy.io import wavfile
import base64

from Crypto.Cipher import AES
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP


# Encrypt a .wav file using the AES algorithm
def encrypt_audio(input_wav_path: str, output_dir: str = ".") -> dict:
    
    # Read input WAV file
    fs, data = wavfile.read(input_wav_path)

    # Read raw binary contents
    with open(input_wav_path, 'rb') as fd:
        contents = fd.read()

    # Generate AES key and IV
    AES_KEY = ''.join(random.choices(string.ascii_letters + string.digits, k=32))
    AES_IV = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
    print("AES Key:", AES_KEY)
    print("AES IV:", AES_IV)

    # Encrypt contents
    encryptor = AES.new(AES_KEY.encode("utf-8"), AES.MODE_CFB, AES_IV.encode("utf-8"))
    encrypted_audio = encryptor.encrypt(contents)

    encrypted_path = os.path.join(output_dir, 'encrypted_audio_file.wav')
    with open(encrypted_path, 'wb') as fd:
        fd.write(encrypted_audio)
    print("Encrypted audio saved to", encrypted_path)

    # Return key and initialization vector
    return {
        "AES_KEY": AES_KEY,
        "AES_IV": AES_IV
    }


# Encrypt the AES key
def encrypt_key(AES_key: str):

    # Generate an RSA key pair
    if not (os.path.exists("rsa_public.pem") and os.path.exists("rsa_private.pem")):
        rsa_key = RSA.generate(2048)                     # 2048-bit is fine for key wrapping
        with open("rsa_private.pem", "wb") as f: f.write(rsa_key.export_key())
        with open("rsa_public.pem",  "wb") as f: f.write(rsa_key.publickey().export_key())

    public_key  = RSA.import_key(open("rsa_public.pem",  "rb").read())
    encryptor = PKCS1_OAEP.new(public_key)   # for wrapping


    # WRAP (encrypt) the AES key
    key_bytes = AES_key.encode("utf-8")      # AES_KEY is your 32-char string
    rsa_wrapped_key = encryptor.encrypt(key_bytes)

    # Persist or transmit the wrapped key
    with open("wrapped_key.bin", "wb") as f:
        f.write(rsa_wrapped_key)

    print("Wrapped AES key (base64):", base64.b64encode(rsa_wrapped_key).decode())
