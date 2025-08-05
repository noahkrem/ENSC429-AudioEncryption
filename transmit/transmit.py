import shutil
from audio_encryptor import *


aes_dict = encrypt_audio('audio.wav')  # Encrypt the audio using AES algorithm
encrypt_key(aes_dict['AES_KEY'])  # Encrypt the AES key using the RSA algorithm

# Save the initialization vector into a .txt file
with open("iv.txt", "w") as file:
    file.write(aes_dict['AES_IV'])


# Here is where we would transmit the encrypted audio and key.
# For simplicity, we simulate transmission by simply copying to another folder.
# However, in reality, we would transmit to another machine altogether.
# This would be done using essentially the same method.
destination_folder = '../receive'
shutil.copy('encrypted_audio_file.wav', destination_folder)
shutil.copy('wrapped_key.bin', destination_folder)
shutil.copy('iv.txt', destination_folder)


