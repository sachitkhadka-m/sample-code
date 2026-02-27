from pwdlib import PasswordHash

pwd = input("Enter password to hash: ")

password_hash = PasswordHash.recommended()
print(password_hash.hash(pwd))
