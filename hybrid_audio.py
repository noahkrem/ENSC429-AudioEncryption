"""
hybrid_audio.py: RSA-wrapped AES encryption for WAV files
============================================================

First run:   python hybrid_audio.py encrypt
- Generates rsa_public.pem / rsa_private.pem   (if not present)
- Produces  secure_audio.bin   = [RSA-wrapped AES key] + [IV] + [AES ciphertext]

Second run (or on another machine with rsa_private.pem):
  python hybrid_audio.py decrypt
- Produces  decrypted.wav

The private key is the ONLY way to unwrap the AES key, so RSA is now integral.
"""

import sys, os, struct
from pathlib import Path

from Crypto.PublicKey import RSA
from Crypto.Cipher    import AES, PKCS1_OAEP
from Crypto.Random    import get_random_bytes
from scipy.io         import wavfile
import matplotlib.pyplot as plt

# ---------------------------------------------------------------------------
# RSA key-pair  (create once; reuse thereafter)
# ---------------------------------------------------------------------------
PUB_PEM  = Path("rsa_public.pem")
PRIV_PEM = Path("rsa_private.pem")

if not (PUB_PEM.exists() and PRIV_PEM.exists()):
    rsa_key = RSA.generate(2048)
    PRIV_PEM.write_bytes(rsa_key.export_key())
    PUB_PEM.write_bytes(rsa_key.publickey().export_key())
    print("Generated new RSA-2048 key-pair")

PUB  = RSA.import_key(PUB_PEM.read_bytes())
PRIV = RSA.import_key(PRIV_PEM.read_bytes())

wrap   = PKCS1_OAEP.new(PUB)    # public key encrypt (wrap)
unwrap = PKCS1_OAEP.new(PRIV)   # private key decrypt (unwrap)

# ---------------------------------------------------------------------------
# Sender side (encrypt)
# ---------------------------------------------------------------------------
def encrypt_wav(src="audio.wav", dst="secure_audio.bin", plot=True):
    if not Path(src).exists():
        sys.exit(f"'{src}' not found")

    # Read raw WAV bytes & (optional) peek at waveform
    fs, data = wavfile.read(src)
    if plot:
        plt.plot(data); plt.title("Original audio"); plt.show()

    wav_bytes = Path(src).read_bytes()

    # Make fresh AES-256 key + IV
    aes_key = get_random_bytes(32)   # 256-bit key
    aes_iv  = get_random_bytes(16)   # 128-bit IV

    # Encrypt the audio with AES/CFB
    cipher_aes  = AES.new(aes_key, AES.MODE_CFB, aes_iv)
    ciphertext  = cipher_aes.encrypt(wav_bytes)

    # RSA-wrap the AES key
    wrapped_key = wrap.encrypt(aes_key)          # 256-byte blob (2048-bit RSA)

    # Package = [2-byte len] [wrapped_key] [16-byte IV] [ciphertext]
    with open(dst, "wb") as f:
        f.write(struct.pack("<H", len(wrapped_key)))
        f.write(wrapped_key)
        f.write(aes_iv)
        f.write(ciphertext)

    print(f"Encrypted: {dst}  (payload {len(ciphertext):,} B)")
    print("   AES key exists only inside the RSA-encrypted blob.")

    # optional: quick look at encrypted byte values
    if plot:
        plt.plot(list(ciphertext)[:20000])
        plt.title("Encrypted audio bytes (first 20k)"); plt.show()

    # scrub plaintext key from memory (best-effort)
    del aes_key

# ---------------------------------------------------------------------------
# Receiver side  (decrypt)
# ---------------------------------------------------------------------------
def decrypt_wav(src="secure_audio.bin", dst="decrypted.wav", plot=True):
    if not Path(src).exists():
        sys.exit(f"'{src}' not found")

    blob = Path(src).read_bytes()

    key_len       = struct.unpack("<H", blob[:2])[0]
    wrapped_key   = blob[2 : 2 + key_len]
    aes_iv        = blob[2 + key_len : 2 + key_len + 16]
    ciphertext    = blob[2 + key_len + 16 :]

    # Unwrap AES key with *private* RSA key
    aes_key = unwrap.decrypt(wrapped_key)

    # AES-decrypt the audio
    cipher_aes = AES.new(aes_key, AES.MODE_CFB, aes_iv)
    wav_bytes  = cipher_aes.decrypt(ciphertext)

    Path(dst).write_bytes(wav_bytes)
    print(f"Decrypted: {dst}")

    if plot:
        fs, data = wavfile.read(dst)
        plt.plot(data); plt.title("Decrypted audio"); plt.show()

# ---------------------------------------------------------------------------
# CLI gateway
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    if len(sys.argv) != 2 or sys.argv[1] not in {"encrypt", "decrypt"}:
        sys.exit("Usage:  python hybrid_audio.py  encrypt|decrypt")

    if sys.argv[1] == "encrypt":
        encrypt_wav()
    else:
        decrypt_wav()
