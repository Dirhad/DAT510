import json
import os
from rsa import generate_keys, sign, verify

BASE = os.path.dirname(os.path.abspath(__file__))
KEYS_FILE = os.path.join(BASE, 'keys.json')
MESSAGE_FILE = os.path.join(BASE, 'messages.json')

def load(path):
    if os.path.exists(path):
        with open(path) as f:
            return json.load(f)
    return None

def save(path, data):
    with open(path, 'w') as f:
        json.dump(data, f, indent=2)

def get_keys(name): #Return (e, d, n) for a user. New users get new keys
    keys = load(KEYS_FILE) or {}

    if name not in keys:
        print(f"New user, generating 2048-bit keys for {name}")

        e, d, n = generate_keys()
        keys[name] = {'e': e, 'd': d, 'n': n}
        save(KEYS_FILE, keys)
    
    k = keys[name]
    return k['e'], k['d'], k['n']


 
 
def main():
    while True:
        print('\n1. Sign message\n2. Verify messages\n3. Exit')
        choice = input('Choose: ')
 
        if choice == '1':
            name = input('Your name: ').strip().lower()
            e,d,n = get_keys(name)
            text = input('Message: ')
            messages = load(MESSAGE_FILE) or []

            messages.append({'sender': name, 'message': text, 'signature': hex(sign(text, d, n))})
            save(MESSAGE_FILE, messages)
            print('Message signed and saved.')
 
        elif choice == '2':
            messages = load(MESSAGE_FILE) or []
            keys = load(KEYS_FILE) or {}
            if not messages:
                print('No stored messages.')
            for i, m in enumerate(messages, 1):
                sender = m['sender']
                if sender in keys:   # use the sender's PUBLIC key (e, n)
                    ok = verify(m['message'], int(m['signature'], 16),
                                keys[sender]['e'], keys[sender]['n'])
                else:
                    ok = False
                print(f"{i}. {sender}: {m['message']!r}: {'VALID' if ok else 'INVALID'}")
 
        elif choice == '3':
            break
 
 
if __name__ == '__main__':
    main()