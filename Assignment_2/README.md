# DAT 510 Assignment 2: RSA Digital Signature

A program that signs messages with RSA and a self-made hash function, stores them, and verifies their signatures.Each user has their own public/private key pair.

## Files

| File | Description |
|---|---|
| `hash_function.py` | Self-made 256-bit hash function (`my_hash`) for messages of any length. |
| `rsa.py` | Prime generation, RSA key generation (2048-bit), `sign` and `verify`. |
| `main.py` | Menu program: sign messages, store them, and verify stored messages. |


## How to run

Open a terminal in this folder an run:

```
python3 main.py
```

The program shows a menu:

````
1. Sign message
2. Verify messages
3. Exit
```

- **1. Sign message**: enter your name and a message. A new user automatically gets a new 2048-bit key pair (takes a few seconds). The message is signed with the user's private key and saved to `messages.json`.
- **2. Verify messages**: checks every stored message with the sender's public key and prints `VALID` or `INVALID`.
- **3. Exit**: closes the program.

## Testing tampering

1. Sign one or more messages and verify them (all `VALID`).
2. Open `messages.json` and change the text of a message, or change its `sender` to another user.
3. Verify again. The changed message shows `INVALID`.