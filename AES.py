from scipy.io import wavfile
import numpy as np
import matplotlib.pyplot as plt
import sounddevice as sd

import random
import string
from Crypto.Cipher import AES


# Take input from the file called audio.wav
fs, data = wavfile.read('audio.wav')
plt.plot(data)            # fs = sampling frequency = 44.1kHz
plt.title("Original Audio Plot")
plt.show()

# Open the file in binary read mode (rb)
# Read the contents of the file and store them into contents
with open('audio.wav', 'rb') as fd:
    contents = fd.read()

# Play the sound back
sd.play(data, fs)
sd.wait()  # Wait for the playback to complete before moving on


# Create the 256-bit AES encryption key, a random string 32 characters long
AES_KEY = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for x in range(32))
# Create the 128-bit initialization vector, a random string 16 characters long
AES_IV = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for x in range(16))

print("AES Key is ", AES_KEY)
print("AES Initialization vector is ", AES_IV)


# Encrypt the audio file 
# Pycryptodome library: Crypto.Cipher.AES.new(key, mode, *args, **kwargs)
#   CFB Mode: Cipher FeedBack, a mode of operation which turns a block cipher into a stream cipher
# Python built-in library: string.encode(encoding=encoding, errors=errors)
encryptor = AES.new(AES_KEY.encode("utf-8"), AES.MODE_CFB, AES_IV.encode("utf-8"))
encrypted_audio = encryptor.encrypt(contents)

with open('encrypted_audio_file.wav', 'wb') as fd:
    fd.write(encrypted_audio)
print("A file titled 'encrypted_audio_file.wav' is generated which is the encrypted audio to be communicated")



with open('encrypted_audio_file.wav', 'rb') as fd:
    contents = fd.read()



decryptor = AES.new(AES_KEY.encode("utf-8"), AES.MODE_CFB, AES_IV.encode("utf-8"))
decrypted_audio = decryptor.decrypt(contents)



with open('decrypted_audio_file.wav', 'wb') as fd:
    fd.write(decrypted_audio)

fs, data = wavfile.read('decrypted_audio_file.wav')
plt.plot(data)            # fs = sampling frequency = 44.1kHz
plt.title("Decrypted audio plot")
plt.show()
data_1 = np.asarray(data, dtype = np.int32)



sd.play(data, fs)
sd.wait()
