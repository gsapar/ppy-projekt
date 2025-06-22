import json
import base64
import os
import random
import string
import hashlib
import requests
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from account import Account

class Manager:
    def __init__(self):
        self.accounts = {}
        self.master_password = None
        self.filename = None

    def get_account(self, name):
        return self.accounts.get(name, None)

    def add_account(self, name, username, password):
        if name in self.accounts:
            return False 
        self.accounts[name] = Account(name, username, password)
        return True 

    def delete_account(self, name):
        return self.accounts.pop(name, None) is not None

    def list_all(self):
        return list(self.accounts.values())

    def edit_account(self, name, new_name=None, new_username=None, new_password=None):
        account = self.get_account(name)
        if not account:
            return False 
        if new_name:
            if new_name in self.accounts:
                raise ValueError(f"An account with the name '{new_name}' already exists.")
            self.accounts.pop(name) 
            account.name = new_name
            self.accounts[new_name] = account 
        if new_username:
            account.username = new_username
        if new_password:
            account.password = new_password 
        return True 

    def serialize_accounts(self):
        return {name: account.to_dict() for name, account in self.accounts.items()}

    def deserialize_accounts(self, serialized_accounts):
        self.accounts = {name: Account.from_dict(data) for name, data in serialized_accounts.items()}

    def save_to_file(self, manager, filepath, password):
        serialized_data = json.dumps(manager.serialize_accounts())
        key, salt = self._generate_key(password)
        cipher = Fernet(key)
        encrypted_data = cipher.encrypt(serialized_data.encode())
        with open(filepath, "wb") as file:
            file.write(salt + b"\n" + encrypted_data)
        os.chdir('/'.join(filepath.split('/')[0:-1]))

    def load_from_file(self, manager, filepath, password):
        with open(filepath, "rb") as file:
            salt = file.readline().strip()
            encrypted_data = file.read()
        key, _ = self._generate_key(password, salt)
        cipher = Fernet(key)
        decrypted_data = cipher.decrypt(encrypted_data).decode()
        serialized_accounts = json.loads(decrypted_data)
        manager.deserialize_accounts(serialized_accounts)
        self.master_password = password
        os.chdir('/'.join(filepath.split('/')[0:-1]))

    @staticmethod
    def _generate_key(password, salt=None):
        if salt is None:
            salt = os.urandom(16) 
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100_000,
            backend=default_backend()
        )
        key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
        return key, salt

    @staticmethod
    def generate_password(length=12, include_uppercase=True, include_numbers=True, include_special_chars=True):
        if length < 4: 
            raise ValueError("Password length must be at least 4 characters.")
        
        lowercase_pool = string.ascii_lowercase
        uppercase_pool = string.ascii_uppercase if include_uppercase else ""
        numbers_pool = string.digits if include_numbers else ""
        special_chars_pool = string.punctuation if include_special_chars else ""

        all_chars = lowercase_pool + uppercase_pool + numbers_pool + special_chars_pool
        if not all_chars:
            raise ValueError("You must enable at least one type of character in the password.")
        
        password = []
        if include_uppercase:
            password.append(random.choice(uppercase_pool))
        if include_numbers:
            password.append(random.choice(numbers_pool))
        if include_special_chars:
            password.append(random.choice(special_chars_pool))
        password.append(random.choice(lowercase_pool)) 
        
        password += random.choices(all_chars, k=length - len(password))
        random.shuffle(password)
        return "".join(password)

    @staticmethod
    def check_password_leak(password):
        sha1_hash = hashlib.sha1(password.encode()).hexdigest().upper()
        prefix = sha1_hash[:5]
        suffix = sha1_hash[5:]

        url = f"https://api.pwnedpasswords.com/range/{prefix}"
        response = requests.get(url)
        if response.status_code != 200:
            raise ConnectionError("Failed to connect to the Have I Been Pwned API.")

        hashes = response.text.splitlines()
        for line in hashes:
            hash_suffix, _ = line.split(":")
            if hash_suffix.strip() == suffix:
                return True 

        return False 
