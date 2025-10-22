const fs = require('fs');
const readline = require('readline');

const ARQUIVO = 'clientes.json';

function carregarClients() {
  if (!fs.existsSync(ARQUIVO))
    return[];
  return JSON.parse(fs.
  readFileSync(ARQUIVO));
}

function salvarClients(clientes) {
  fs.writeFileSync(ARQUIVO, JSON.
  stringify(clientes, null, 2));
}

function listarClients(clientes, cb) {
  console.log('lista de clientes:');
  clientes.forEach(c => {
    console.log(`ID: ${c.id} | nome: ${c.nome} | email: ${c.email}`);
  });
  cb();
}

function addClient(clientes, rl, cb) {
  rl.question('Nome: ', nome => {
    rl.question('Email: ', email => {
      const novoId = clientes.length ? Math.max(...clientes.map(c => c.id)) + 1 : 1;
      clientes.push({ id: novoId, nome, email});
      salvarClients(clientes);
      console.log('Cliente adicionado.');
      cb();
    });
  });
}

function editarClient(clientes, rl, cb) {
  rl.question('ID do cliente para editar: ', idStr => {
    const id = parseInt(idStr);
    const cliente = clientes.find(c => c.id === id);
    if (!cliente) {
      console.log('Cliente inexistente.');
      return cb()
    }
      rl.question(`Novo nome (${cliente.nome}): `, nome => {
        rl.question(`Novo email (${cliente.email}): `, email => {
          cliente.nome = nome || cliente.nome;
          cliente.email = email || cliente.email;
          salvarClients(clientes);
          console.log('Cliente editado.');
        cb();
        });
      });
  });
}

function removerCliente(clientes, rl, cb) {
  rl.question('ID do cliente para remover: ', idStr => {
    const id = parseInt(idStr);
    const novosClientes = clientes.
    filter(c => c.id !== id);
    if (novosClientes.length === clientes.lenght) {
      console.log('Cliente não encontrado.');
    } else {
      salvarClients(novosClientes);
      console.log('Cliente removido.');
    }
    cb();
  });
}

function menu() {
  const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout
  });

  function loop() {
    const clientes = carregarClients();
    console.log('\n1. Listar\n2. Adicionar\n3. Editar\n4. Remover\n5. Sair');
    rl.question('Escolha: ', op => {
      if (op === '1'){
        listarClients(clientes, loop);
      } else if (op === '2') {
        addClient(clientes, rl, loop);
      } else if (op === '3') {
        editarClient(clientes, rl, loop);
      } else if (op === '4') {
        removerCliente(clientes, rl, loop);
      } else if (op === '5') {
        rl.close();
      } else {
        console.log('Opção inválida');
        loop();
      }
    });
  }
  loop();
}

menu();
