const fs = require('fs');
const readline = require('readline');

const ARQUIVO = 'estagiarios.json';

function carregarEstagiario() {
  if (!fs.existsSync(ARQUIVO))
    return[];
  return JSON.parse(fs.
  readFileSync(ARQUIVO));
}

function salvarEstagiario(estagiarios) {
  fs.writeFileSync(ARQUIVO, JSON.
  stringify(estagiarios, null, 2));
}

function listarEstagiario(estagiarios, cb) {
  console.log('lista de estagiarios:');
  estagiarios.forEach(c => {
    console.log(`ID: ${c.id} | nome: ${c.nome} | email: ${c.email}`);
  });
  cb();
}

function addEstagiario(estagiarios, rl, cb) {
  rl.question('Nome: ', nome => {
    rl.question('Email: ', email => {
      rl.question('Senha: ', senha => {
        const novoId = estagiarios.length ? Math.max(...estagiarios.map(c => c.id)) + 1 : 1;
        estagiarios.push({ id: novoId, nome, email, senha});
        salvarEstagiario(estagiarios);
        console.log('Estagiario adicionado.');
        cb();
      });
    });
  });
}

function editarEstagiario(estagiarios, rl, cb) {
  rl.question('ID do estagiario para editar: ', idStr => {
    const id = parseInt(idStr);
    const estagiario = estagiarios.find(c => c.id === id);
    if (!estagiario) {
      console.log('Estagiario inexistente.');
      return cb()
    }
      rl.question(`Novo nome (${estagiario.nome}): `, nome => {
        rl.question(`Novo email (${estagiario.email}): `, email => {
          rl.question(`Nova senha: `, senha =>{
            estagiario.nome = nome || estagiario.nome;
            estagiario.email = email || estagiario.email;
            estagiario.senha = senha || estagiario.senha;
            salvarEstagiario(estagiarios);
            console.log('Estagiario editado.');
            cb();
          });
        });
      });
  });
}

function removerEstagiario(estagiarios, rl, cb) {
  rl.question('ID do estagiario para remover: ', idStr => {
    const id = parseInt(idStr);
    const novosEstagiarios = estagiarios.
    filter(c => c.id !== id);
    if (novosEstagiarios.length === estagiarios.lenght) {
      console.log('Estagiario não encontrado.');
    } else {
      salvarEstagiario(novosEstagiarios);
      console.log('Estagiario removido.');
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
    const estagiarios = carregarEstagiario();
    console.log('\n1. Listar\n2. Adicionar\n3. Editar\n4. Remover\n5. Sair');
    rl.question('Escolha: ', op => {
      if (op === '1'){
      listarEstagiario(estagiarios, loop);
      } else if (op === '2') {
        addEstagiario(estagiarios, rl, loop);
      } else if (op === '3') {
        editarEstagiario(estagiarios, rl, loop);
      } else if (op === '4') {
        removerEstagiario(estagiarios, rl, loop);
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
