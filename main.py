import hashlib
from cryptography.fernet import Fernet

# Load encryption key
def load_key():
    return open("secret.key", "rb").read()

key = load_key()
cipher = Fernet(key)

# Master password (hashed)
MASTER_PASSWORD_HASH = hashlib.sha256("admin123".encode()).hexdigest()

def verify_master_password():
    password = input("Enter Master Password: ")
    return hashlib.sha256(password.encode()).hexdigest() == MASTER_PASSWORD_HASH

# Add password (ENCRYPT)
def add_password():
    website = input("Website: ")
    username = input("Username: ")
    password = input("Password: ")

    encrypted_pwd = cipher.encrypt(password.encode())

    with open("passwords.txt", "a") as file:
        file.write(f"{website} | {username} | {encrypted_pwd.decode()}\n")

    print("Password saved securely!")

# View all passwords (DECRYPT ALL)
def view_passwords():
    with open("passwords.txt", "r") as file:
        for line in file:
            website, username, enc_pwd = line.strip().split(" | ")
            decrypted_pwd = cipher.decrypt(enc_pwd.encode()).decode()
            print(f"Website: {website}, Username: {username}, Password: {decrypted_pwd}")

# 🔓 Decrypt specific password (FIXED FUNCTION)
def decrypt_password():
    website_name = input("Enter website name: ")
    found = False

    with open("passwords.txt", "r") as file:
        for line in file:
            website, username, enc_pwd = line.strip().split(" | ")
            if website == website_name:
                decrypted_pwd = cipher.decrypt(enc_pwd.encode()).decode()
                print("\nDecrypted Details:")
                print(f"Website: {website}")
                print(f"Username: {username}")
                print(f"Password: {decrypted_pwd}")
                found = True
                break

    if not found:
        print("No password found for this website!")

# MAIN FUNCTION
def main():
    if not verify_master_password():
        print("Access Denied!")
        return

    while True:
        print("\n--- Secure Password Manager ---")
        print("1. Add Password (Encrypt)")
        print("2. View All Passwords (Decrypt)")
        print("3. Decrypt Specific Password")
        print("4. Exit")

        choice = input("Choose option: ")

        if choice == "1":
            add_password()
        elif choice == "2":
            view_passwords()
        elif choice == "3":
            decrypt_password()
        elif choice == "4":
            print("Exiting securely...")
            break
        else:
            print("Invalid choice!")

main()