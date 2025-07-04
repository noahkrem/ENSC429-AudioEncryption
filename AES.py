from scipy.io import wavfile
import numpy as np
import matplotlib.pyplot as plt
import sounddevice as sd

import random
import string
from Crypto.Cipher import AES


# Take input from the file called audio.wav
fs, data = wavfile.read('audio.wav')

# Save the data to a text file
with open("output.txt", "w") as txt_file:
    if data.ndim == 1:  # Mono
        for sample in data:
            txt_file.write(f"{sample}\n")
    else:  # Stereo or multi-channel
        for sample in data:
            txt_file.write(" ".join(map(str, sample)) + "\n")

plt.plot(data)            # fs = sampling frequency = 44.1kHz for CD quality
plt.title("Original Audio Plot")
plt.show()

# Open the file in binary read mode (rb)
# Read the contents of the file and store them into contents
with open('audio.wav', 'rb') as fd:
    contents = fd.read()

# Create the 256-bit AES encryption key, a random string 32 characters long
# Note: AES_KEY should be 16, 24, or 32 bytes long or else it will cause an error
AES_KEY = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for x in range(32))
# Create the 128-bit initialization vector, a random string 16 characters long
# Note: AES_IV should be 16 bytes for AES
AES_IV = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for x in range(16))

print("AES Key is ", AES_KEY)
print("AES Initialization vector is ", AES_IV)


# Encrypt the audio file 
# Pycryptodome library: Crypto.Cipher.AES.new(key, mode, *args, **kwargs)
#   CFB Mode: Cipher FeedBack, a mode of operation which turns a block cipher into a stream cipher
#   CFB Mode is ideal for encrypting data of arbitrary length like audio files
# Pycryptodome library: Crypto.Cipher.encrypt(self, plaintext, output=None)
encryptor = AES.new(AES_KEY.encode("utf-8"), AES.MODE_CFB, AES_IV.encode("utf-8"))
encrypted_audio = encryptor.encrypt(contents)

# Store the encrypted audio file in .wav format
with open('encrypted_audio_file.wav', 'wb') as fd:
    fd.write(encrypted_audio)
print("A file titled 'encrypted_audio_file.wav' is generated which is the encrypted audio to be communicated")

# Load the encrypted audio file that was just created
with open('encrypted_audio_file.wav', 'rb') as fd:
    contents = fd.read()

plt.plot(list(contents))
plt.title('Encrypted Audio')
plt.show()

# Plot a zoomed-in version of the encrypted audio
plt.plot(list(contents))
plt.title('Encrypted Audio, showing 1000 values')
plt.xlim(10000, 11000)
plt.show()

# Plot an extremely zoomed-in version of the encrypted audio
plt.plot(list(contents))
plt.title('Encrypted Audio, showing 100 values')
plt.xlim(10000, 10100)
plt.show()

# Decrypt the audio file
# Pycryptodome library: Crypto.Cipher.AES.new(key, mode, *args, **kwargs)
# Pycryptodome library: Crypto.Cipher.decrypt(self, ciphertext,  output=None)
decryptor = AES.new(AES_KEY.encode("utf-8"), AES.MODE_CFB, AES_IV.encode("utf-8"))
decrypted_audio = decryptor.decrypt(contents)

# Write the decrypted audio to a new file
with open('decrypted_audio_file.wav', 'wb') as fd:
    fd.write(decrypted_audio)

# Read the decrypted audio and plot the waveform
fs, data = wavfile.read('decrypted_audio_file.wav')
plt.plot(data)            # fs = sampling frequency = 44.1kHz for CD quality
plt.title("Decrypted audio plot")
plt.show()

# Note: If we want to do further processing that requires 32-bit precision:
#   data_1 = np.asarray(data, dtype = np.int32)
