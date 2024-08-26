#!/usr/bin/env python3

"""
Autor: Jack Bauer
E-mail: jackbauer2018@protonmail.com
Version: 1.0
Data: 26/08/2024
"""

import secrets
import string
import os
import base64
import hashlib
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet

def gerar_senha(tamanho, maiusculas, minusculas, numeros, caracteres_especiais):
    caracteres = ''
    if maiusculas:
        caracteres += string.ascii_uppercase
    if minusculas:
        caracteres += string.ascii_lowercase
    if numeros:
        caracteres += string.digits
    if caracteres_especiais:
        caracteres += string.punctuation
    return ''.join(secrets.choice(caracteres) for _ in range(tamanho))

def gerar_chave_a_partir_da_senha(senha):
    salt = b'\x00' * 16  # Salt fixo para simplificar (não recomendado para produção)
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    chave = base64.urlsafe_b64encode(kdf.derive(senha.encode()))
    return chave

def criptografar_senha(senha, senha_de_criptografia):
    chave = gerar_chave_a_partir_da_senha(senha_de_criptografia)
    cipher_suite = Fernet(chave)
    return cipher_suite.encrypt(senha.encode()).decode()

def descriptografar_senha(senha_criptografada, senha_de_criptografia):
    chave = gerar_chave_a_partir_da_senha(senha_de_criptografia)
    cipher_suite = Fernet(chave)
    return cipher_suite.decrypt(senha_criptografada.encode()).decode()

def salvar_senha(nome, username, email, dominio, url_dominio, senha, criptografado=False):
    pasta_jackpassdrive = "JackPassDrive"
    if not os.path.exists(pasta_jackpassdrive):
        os.makedirs(pasta_jackpassdrive)
    
    nome_arquivo = f"{username}_{dominio}.txt"
    arquivo_path = os.path.join(pasta_jackpassdrive, nome_arquivo)
    
    with open(arquivo_path, 'w') as arquivo:
        arquivo.write(f"Nome: {nome}\n")
        arquivo.write(f"Username: {username}\n")
        arquivo.write(f"E-mail: {email}\n")
        arquivo.write(f"Nome do domínio: {dominio}\n")
        arquivo.write(f"URL do domínio: {url_dominio}\n")
        if criptografado:
            arquivo.write(f"Senha criptografada (Fernet): {senha}\n")
        else:
            arquivo.write(f"Senha: {senha}\n")
    
    print(f"Sua senha foi gerada e está na pasta {pasta_jackpassdrive} em {arquivo_path}")
    print("Você pode acessá-la a qualquer momento!")

def exibir_senha(senha, dominio, url_dominio):
    print("\n" + "*"*50)
    print(f"Nome do domínio: {dominio.center(48)}")
    print(f"URL do domínio: {url_dominio.center(48)}")
    print(f"Senha gerada: {senha.center(48)}")
    print("*"*50 + "\n")

def criar_senha():
    nome = input("Digite seu nome: ")
    username = input("Digite seu username: ")
    email = input("Digite seu e-mail: ")

    dominio = input("Digite o nome do domínio onde a senha será usada: ")
    url_dominio = input("Digite a URL do domínio: ")

    tamanho = int(input("Digite o tamanho da sua nova senha: "))
    maiusculas = input("Deseja incluir letras maiúsculas? (s/n): ").lower() == 's'
    minusculas = input("Deseja incluir letras minúsculas? (s/n): ").lower() == 's'
    numeros = input("Deseja incluir números? (s/n): ").lower() == 's'
    caracteres_especiais = input("Deseja incluir caracteres especiais? (s/n): ").lower() == 's'

    senha = gerar_senha(tamanho, maiusculas, minusculas, numeros, caracteres_especiais)
    exibir_senha(senha, dominio, url_dominio)

    criptografar = input("Deseja criptografar a sua senha? (s/n): ").lower() == 's'
    if criptografar:
        senha_de_criptografia = input("Digite uma senha ou frase para criptografia: ")
        senha_criptografada = criptografar_senha(senha, senha_de_criptografia)
        print(f"Senha criptografada (Fernet): {senha_criptografada}")
        salvar_senha(nome, username, email, dominio, url_dominio, senha_criptografada, criptografado=True)
    else:
        salvar_senha(nome, username, email, dominio, url_dominio, senha)

def descriptografar_senha_input():
    senha_criptografada = input("Digite ou cole a senha criptografada: ")
    senha_de_criptografia = input("Digite a senha ou frase de criptografia: ")
    try:
        senha_original = descriptografar_senha(senha_criptografada, senha_de_criptografia)
        print("\n" + "*"*50)
        print(f"A senha descriptografada é: {senha_original.center(48)}")
        print("*"*50 + "\n")
    except Exception as e:
        print(f"Erro ao descriptografar. Você inseriu a senha errada. Por favor, digite a senha ou frase correta: {e}")

def main():
    print("Jack Pass - Gerador de Senhas")
    print("Versão 1.0")

    opcao = input("Deseja (1) Criar uma senha ou (2) Descriptografar uma senha? Digite 1 ou 2: ")

    if opcao == '1':
        criar_senha()
    elif opcao == '2':
        descriptografar_senha_input()
    else:
        print("Opção inválida. Por favor, escolha 1 ou 2.")

if __name__ == "__main__":
    main()
