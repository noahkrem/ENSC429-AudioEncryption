# ENSC429-AudioEncryption

## 🚀 Getting Started

Follow these steps to set up and run the code:

### 1. Clone the Repository

```bash
git clone https://github.com/noahkrem/ENSC429-AudioEncryption.git
cd ENSC429-AudioEncryption.git
```

### 2. Set Up a Virtual Environment (Recommended)

```bash
python -m venv venv
source venv/bin/activate  # On Linux/macOS
venv\scripts\activate  # On Windows
```

### 3. Install Dependencies

```bash
pip install numpy matplotlib sounddevice pycryptodome scipy
```

```bash
sudo apt install python3-tk
```

## 📄 Usage

### Generating RSA key pair

```bash
cd receive
python generate_rsa_pair.py
```

### Encrypting and Transmitting

```bash
cd transmit
python transmit.py
```

### Receiving and Decrypting

```bash
cd receive
python receive.py
```

### Displaying Graphs and Data

```bash
cd files_testing
python AES.py
```

## 🧹 Cleaning Up

When you are done editing and running the code, you can close your virtual environment:
```bash
deactivate
```



