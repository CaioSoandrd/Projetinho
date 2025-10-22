import json
import os

ARQUIVO = 'clientes.json'

def carregar_clientes():
    if not os.path.exists(ARQUIVO):
        return []
    with open(ARQUIVO, 'r') as f:
        return json.load(f)

def salvar_clientes(clientes):
    with open(ARQUIVO, 'w') as f:
        json.dump(clientes, f, indent=2)

def listar_clientes(clientes):
    print('Lista de clientes:')
    for c in clientes:
        print(f"ID: {c['id']} | nome: {c['nome']} | email: {c['email']}")

def adicionar_cliente(clientes):
    nome = input('Nome: ')
    email = input('Email: ')
    novo_id = max([c['id'] for c in clientes], default=0) + 1
    clientes.append({'id': novo_id, 'nome': nome, 'email': email})
    salvar_clientes(clientes)
    print('Cliente adicionado.')

def editar_cliente(clientes):
    id_str = input('ID do cliente para editar: ')
    try:
        id = int(id_str)
    except ValueError:
        print('ID inválido.')
        return
    cliente = next((c for c in clientes if c['id'] == id), None)
    if not cliente:
        print('Cliente inexistente.')
        return
    nome = input(f"Novo nome ({cliente['nome']}): ")
    email = input(f"Novo email ({cliente['email']}): ")
    cliente['nome'] = nome or cliente['nome']
    cliente['email'] = email or cliente['email']
    salvar_clientes(clientes)
    print('Cliente editado.')

def remover_cliente(clientes):
    id_str = input('ID do cliente para remover: ')
    try:
        id = int(id_str)
    except ValueError:
        print('ID inválido.')
        return
    novos_clientes = [c for c in clientes if c['id'] != id]
    if len(novos_clientes) == len(clientes):
        print('Cliente não encontrado.')
    else:
        salvar_clientes(novos_clientes)
        print('Cliente removido.')
        clientes[:] = novos_clientes  # Atualiza a lista original

def menu():
    while True:
        clientes = carregar_clientes()
        print('\n1. Listar\n2. Adicionar\n3. Editar\n4. Remover\n5. Sair')
        op = input('Escolha: ')
        if op == '1':
            listar_clientes(clientes)
        elif op == '2':
            adicionar_cliente(clientes)
        elif op == '3':
            editar_cliente(clientes)
        elif op == '4':
            remover_cliente(clientes)
        elif op == '5':
            break
        else:
            print('Opção inválida')

if __name__ == '__main__':
    menu()
