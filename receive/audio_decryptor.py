import os

from Crypto.Cipher import AES
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP


def decrypt_audio(AES_KEY: str, AES_IV: str, encrypted_audio_path: str, output_dir: str = '.'):

    # Load the encrypted audio file
    with open(encrypted_audio_path, 'rb') as fd:
        contents = fd.read()

    # Decrypt the audio file
    # Pycryptodome library: Crypto.Cipher.AES.new(key, mode, *args, **kwargs)
    # Pycryptodome library: Crypto.Cipher.decrypt(self, ciphertext,  output=None)
    decryptor = AES.new(AES_KEY.encode("utf-8"), AES.MODE_CFB, AES_IV.encode("utf-8"))
    decrypted_audio = decryptor.decrypt(contents)

    # Write the decrypted audio to a new file
    decrypted_path = os.path.join(output_dir, 'decrypted_audio_file.wav')
    with open(decrypted_path, 'wb') as fd:
        fd.write(decrypted_audio)

    print("Decrypted audio saved to", decrypted_path)


# Decrypt the key using the given wrapped key and 
def decrypt_key(wrapped_key_path: str, private_key_path: str) -> dict:
    
    with open(wrapped_key_path, "rb") as f:
        rsa_wrapped_key = f.read()

    private_key = RSA.import_key(open(private_key_path, "rb").read())
    decryptor = PKCS1_OAEP.new(private_key)  # for unwrapping

    recovered_key_bytes = decryptor.decrypt(rsa_wrapped_key)
    recovered_AES_KEY = recovered_key_bytes.decode("utf-8")

    print("Recovered AES key:", recovered_AES_KEY)

    return recovered_AES_KEY

