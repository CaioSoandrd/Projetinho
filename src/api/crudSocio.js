const fs = require('fs');
const readline = require('readline');

const ARQUIVO = 'socios.json';

function carregarSocio() {
  if (!fs.existsSync(ARQUIVO))
    return[];
  return JSON.parse(fs.
  readFileSync(ARQUIVO));
}

function salvarSocio(socios) {
  fs.writeFileSync(ARQUIVO, JSON.
  stringify(socios, null, 2));
}

function listarSocio(socios, cb) {
  console.log('lista de socios:');
  socios.forEach(c => {
    console.log(`ID: ${c.id} | nome: ${c.nome} | email: ${c.email}`);
  });
  cb();
}

function addSocio(socios, rl, cb) {
  rl.question('Nome: ', nome => {
    rl.question('Email: ', email => {
      rl.question('Senha: ', senha => {
        const novoId = socios.length ? Math.max(...socios.map(c => c.id)) + 1 : 1;
        socios.push({ id: novoId, nome, email, senha});
        salvarSocio(socios);
        console.log('Socio adicionado.');
        cb();
      });
    });
  });
}

function editarSocio(socios, rl, cb) {
  rl.question('ID do socio para editar: ', idStr => {
    const id = parseInt(idStr);
    const socio = socios.find(c => c.id === id);
    if (!socio) {
      console.log('Socio inexistente.');
      return cb()
    }
      rl.question(`Novo nome (${socio.nome}): `, nome => {
        rl.question(`Novo email (${socio.email}): `, email => {
          rl.question(`Nova senha: `, senha =>{
            socio.nome = nome || socio.nome;
            socio.email = email || socio.email;
            socio.senha = senha || socio.senha;
            salvarSocio(socios);
            console.log('Socio editado.');
            cb();
          });
        });
      });
  });
}

function removerSocio(socios, rl, cb) {
  rl.question('ID do socio para remover: ', idStr => {
    const id = parseInt(idStr);
    const novosSocios = socios.
    filter(c => c.id !== id);
    if (novosSocios.length === socios.lenght) {
      console.log('Socio não encontrado.');
    } else {
      salvarSocio(novosSocios);
      console.log('Socio removido.');
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
    const socios = carregarSocio();
    console.log('\n1. Listar\n2. Adicionar\n3. Editar\n4. Remover\n5. Sair');
    rl.question('Escolha: ', op => {
      if (op === '1'){
      listarSocio(socios, loop);
      } else if (op === '2') {
        addSocio(socios, rl, loop);
      } else if (op === '3') {
        editarSocio(socios, rl, loop);
      } else if (op === '4') {
        removerSocio(socios, rl, loop);
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
