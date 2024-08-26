#!/usr/bin/env python3

"""
Autor: Jack Bauer
E-mail: jackbauer2018@protonmail.com
Version: 1.0
Data: 25/08/2024
"""
print("Jack Pass - Gerador de Senhas")
print("Versão 1.0")

import random
import string

# Função para gerar a senha
def generate_password(length, uppercase, lowercase, digits, special_chars):
    characters = ""
    if uppercase:
        characters += string.ascii_uppercase
    if lowercase:
        characters += string.ascii_lowercase
    if digits:
        characters += string.digits
    if special_chars:
        characters += string.punctuation

    if not characters:
        raise ValueError("Pelo menos um tipo de caractere deve ser selecionado")

    password = ''.join(random.choice(characters) for i in range(length))
    return password

# Função para salvar a senha em um arquivo .txt
def save_password(filename, password_data):
    with open(filename, 'w') as file:
        file.write(password_data)
    print(f"Senha salva em {filename}")

# Função para exibir a senha de forma legível na tela
def display_password(password):
    print("\n" + "*"*50)
    print(f"Senha gerada: {password.center(48)}")
    print("*"*50 + "\n")

# Coletar dados do usuário
name = input("Nome: ")
username = input("Username: ")
email = input("E-mail: ")
url = input("URL do site: ")
length = int(input("Quantidade de caracteres: "))
uppercase = input("Incluir letras maiúsculas? (s/n): ").lower() == 's'
lowercase = input("Incluir letras minúsculas? (s/n): ").lower() == 's'
digits = input("Incluir números? (s/n): ").lower() == 's'
special_chars = input("Incluir caracteres especiais? (s/n): ").lower() == 's'

password = generate_password(length, uppercase, lowercase, digits, special_chars)

password_data = f"Nome: {name}\nUsername: {username}\nE-mail: {email}\nURL: {url}\nSenha: {password}\n"

# Exibir a senha de forma legível na tela
display_password(password)

# Opção para salvar a senha em um arquivo txt
save_option = input("Deseja salvar a senha no PC? (s/n): ").lower()

if save_option == 's':
    filename = input("Nome do arquivo para salvar: ") + ".txt"
    save_password(filename, password_data)
else:
    print("Senha não salva.")
