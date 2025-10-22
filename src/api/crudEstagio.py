import json
import os

ARQUIVO = 'estagiarios.json'

def carregar_estagiarios():
    if not os.path.exists(ARQUIVO):
        return []
    with open(ARQUIVO, 'r', encoding='utf-8') as f:
        return json.load(f)

def salvar_estagiarios(estagiarios):
    with open(ARQUIVO, 'w', encoding='utf-8') as f:
        json.dump(estagiarios, f, indent=2, ensure_ascii=False)

def listar_estagiarios(estagiarios):
    print('Lista de estagiários:')
    for c in estagiarios:
        print(f"ID: {c['id']} | nome: {c['nome']} | email: {c['email']}")

def adicionar_estagiario(estagiarios):
    nome = input('Nome: ')
    email = input('Email: ')
    senha = input('Senha: ')
    novo_id = max([c['id'] for c in estagiarios], default=0) + 1
    estagiarios.append({'id': novo_id, 'nome': nome, 'email': email, 'senha': senha})
    salvar_estagiarios(estagiarios)
    print('Estagiário adicionado.')

def editar_estagiario(estagiarios):
    try:
        id_editar = int(input('ID do estagiário para editar: '))
    except ValueError:
        print('ID inválido.')
        return
    estagiario = next((c for c in estagiarios if c['id'] == id_editar), None)
    if not estagiario:
        print('Estagiário inexistente.')
        return
    nome = input(f"Novo nome ({estagiario['nome']}): ") or estagiario['nome']
    email = input(f"Novo email ({estagiario['email']}): ") or estagiario['email']
    senha = input("Nova senha: ") or estagiario['senha']
    estagiario.update({'nome': nome, 'email': email, 'senha': senha})
    salvar_estagiarios(estagiarios)
    print('Estagiário editado.')

def remover_estagiario(estagiarios):
    try:
        id_remover = int(input('ID do estagiário para remover: '))
    except ValueError:
        print('ID inválido.')
        return
    novos_estagiarios = [c for c in estagiarios if c['id'] != id_remover]
    if len(novos_estagiarios) == len(estagiarios):
        print('Estagiário não encontrado.')
    else:
        salvar_estagiarios(novos_estagiarios)
        print('Estagiário removido.')
    return novos_estagiarios

def menu():
    while True:
        estagiarios = carregar_estagiarios()
        print('\n1. Listar\n2. Adicionar\n3. Editar\n4. Remover\n5. Sair')
        op = input('Escolha: ')
        if op == '1':
            listar_estagiarios(estagiarios)
        elif op == '2':
            adicionar_estagiario(estagiarios)
        elif op == '3':
            editar_estagiario(estagiarios)
        elif op == '4':
            estagiarios = remover_estagiario(estagiarios) or estagiarios
        elif op == '5':
            break
        else:
            print('Opção inválida')

if __name__ == '__main__':
    menu()
