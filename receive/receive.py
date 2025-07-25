import shutil
from audio_decryptor import *


AES_key = decrypt_key('wrapped_key.bin', 'rsa_private.pem')  # Decrypt the AES key

# Grab the initialization vector
with open("iv.txt", "r") as file:
    AES_iv = file.read()

decrypt_audio(AES_key, AES_iv, 'encrypted_audio_file.wav')  # Decrypt the audio file



