from cryptography.fernet import Fernet
import json
import os
import base64
import random
import string

class PasswordManager:
    def __init__(self, key_file='key.key', data_file='passwords.json'):
        # Constructor to initialize key file, data file, and load encryption key
        self.key_file = key_file
        self.data_file = data_file
        self.key = self.load_key()  # Initialize the key during object creation

    def generate_key(self):
        # Generate a new encryption key using Fernet
        return Fernet.generate_key()

    def load_key(self):
        # Load the encryption key from the key file or generate a new one if not exists
        if os.path.exists(self.key_file):
            with open(self.key_file, 'rb') as key_file:
                return key_file.read()
        else:
            key = self.generate_key()
            with open(self.key_file, 'wb') as key_file:
                key_file.write(key)
            return key

    def encrypt_password(self, password):
        # Encrypt a password using Fernet encryption
        cipher_suite = Fernet(self.key)
        encrypted_password = cipher_suite.encrypt(password.encode())
        return base64.b64encode(encrypted_password).decode()

    def decrypt_password(self, encrypted_password):
        # Decrypt an encrypted password using Fernet decryption
        cipher_suite = Fernet(self.key)
        decoded_password = base64.b64decode(encrypted_password.encode())
        decrypted_password = cipher_suite.decrypt(decoded_password).decode()
        return decrypted_password

    def generate_strong_password(self, length=12):
        # Generate a strong random password with specified length
        characters = string.ascii_letters + string.digits + string.punctuation
        password = ''.join(random.choice(characters) for _ in range(length))
        return password

    def save_password(self, category, account, auto_generate=True):
        # Save a password, either auto-generate or manually input by the user
        if auto_generate:
            password = self.generate_strong_password()
            print(f"Generated Strong Password: {password}")
        else:
            password = input("Enter the password manually: ")

        encrypted_password = self.encrypt_password(password)
        data = self.load_data()
        if category not in data:
            data[category] = {}
        data[category][account] = encrypted_password
        self.save_data(data)

    def retrieve_password(self, category, account):
        # Retrieve a decrypted password from the stored data
        data = self.load_data()
        if category in data and account in data[category]:
            encrypted_password = data[category][account]
            decrypted_password = self.decrypt_password(encrypted_password)
            return decrypted_password
        else:
            return None

    def load_data(self):
        # Load password data from the data file
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r') as file:
                try:
                    data = json.load(file)
                except json.JSONDecodeError:
                    data = {}
        else:
            data = {}
        return data

    def save_data(self, data):
        # Save password data to the data file
        with open(self.data_file, 'w') as file:
            json.dump(data, file, indent=2)

if __name__ == "__main__":
    # Main program execution
    password_manager = PasswordManager()

    while True:
        # Display the main menu to the user
        print("\nPassword Manager Menu:")
        print("1. Save Password")
        print("2. Retrieve Password")
        print("3. Generate Strong Password")
        print("4. Exit")

        # Get user's choice
        choice = input("Enter your choice (1/2/3/4): ")

        if choice == '1':
            # Save Password option
            category = input("Enter category: ")
            account = input("Enter account: ")
            
            # Ask the user if they want to auto-generate a strong password
            auto_generate = input("Auto-generate strong password? (y/n): ").lower() == 'y'
            
            password_manager.save_password(category, account, auto_generate)
            print("Password saved successfully!")

        elif choice == '2':
            # Retrieve Password option
            category = input("Enter category: ")
            account = input("Enter account: ")
            retrieved_password = password_manager.retrieve_password(category, account)
            if retrieved_password:
                print(f"\nRetrieved Password: {retrieved_password}")
            else:
                print("Password not found!")

        elif choice == '3':
            # Generate Strong Password option
            category = input("Enter category : ")
            account = input("Enter account : ")
            password_manager.save_password(category, account)
            print("Password generated successfully!")

        elif choice == '4':
            # Exit the program
            break

        else:
            print("Invalid choice. Please enter 1, 2, 3, or 4.")
