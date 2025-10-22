import json
import os

ARQUIVO = 'socios.json'

def carregar_socios():
    if not os.path.exists(ARQUIVO):
        return []
    with open(ARQUIVO, 'r', encoding='utf-8') as f:
        return json.load(f)

def salvar_socios(socios):
    with open(ARQUIVO, 'w', encoding='utf-8') as f:
        json.dump(socios, f, indent=2, ensure_ascii=False)

def listar_socios(socios):
    print('Lista de sócios:')
    for c in socios:
        print(f"ID: {c['id']} | nome: {c['nome']} | email: {c['email']}")

def adicionar_socio(socios):
    nome = input('Nome: ')
    email = input('Email: ')
    senha = input('Senha: ')
    novo_id = max([c['id'] for c in socios], default=0) + 1
    socios.append({'id': novo_id, 'nome': nome, 'email': email, 'senha': senha})
    salvar_socios(socios)
    print('Sócio adicionado.')

def editar_socio(socios):
    try:
        id_editar = int(input('ID do sócio para editar: '))
    except ValueError:
        print('ID inválido.')
        return
    socio = next((c for c in socios if c['id'] == id_editar), None)
    if not socio:
        print('Sócio inexistente.')
        return
    nome = input(f"Novo nome ({socio['nome']}): ") or socio['nome']
    email = input(f"Novo email ({socio['email']}): ") or socio['email']
    senha = input("Nova senha: ") or socio['senha']
    socio.update({'nome': nome, 'email': email, 'senha': senha})
    salvar_socios(socios)
    print('Sócio editado.')

def remover_socio(socios):
    try:
        id_remover = int(input('ID do sócio para remover: '))
    except ValueError:
        print('ID inválido.')
        return socios
    novos_socios = [c for c in socios if c['id'] != id_remover]
    if len(novos_socios) == len(socios):
        print('Sócio não encontrado.')
    else:
        salvar_socios(novos_socios)
        print('Sócio removido.')
    return novos_socios

def menu():
    while True:
        socios = carregar_socios()
        print('\n1. Listar\n2. Adicionar\n3. Editar\n4. Remover\n5. Sair')
        op = input('Escolha: ')
        if op == '1':
            listar_socios(socios)
        elif op == '2':
            adicionar_socio(socios)
        elif op == '3':
            editar_socio(socios)
        elif op == '4':
            socios = remover_socio(socios)
        elif op == '5':
            break
        else:
            print('Opção inválida')

if __name__ == '__main__':
    menu()
