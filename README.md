# FastAPI do Zero
Repositório com o código que está sendo feito para o [Curso de FastAPI](https://fastapidozero.dunossauro.com).

## Como rodar o projeto:
Este projeto usa a versão `3.12.*` do Python. Você pode instalar a versão correta com o [pyenv](https://github.com/pyenv/pyenv):
```bash
pyenv install 3.12.3
pyenv local 3.12.3
```

O projeto usa o [Poetry](https://python-poetry.org/) para gerenciar as dependências. Para instalar as dependências, execute:
```bash
poetry install
```

Para rodar os comando do projeto, você precisa ativar o ambiente virtual do Poetry com o comando:
```bash
poetry shell
```

### Sobre os comandos:
Os comandos para executar funções do projeto são feitos com o [taskipy](https://github.com/taskipy/taskipy):
```bash
task --list           # Lista os comandos disponíveis
task migrate_generate # Gera arquivos de migração do banco de dados
task migrate_upgrade  # Executa as migrações do banco de dados
task migrate          # Gera e executa as migrações do banco de dados
task dev              # Roda o servidor de desenvolvimento
task test             # Roda os testes
task lint             # Roda o linter
task lint --fix       # Roda o linter e tenta corrigir os problemas
task format           # Formata o código
```

### Setup para rodar o projeto:
Crie um arquivo `.env` na raiz do projeto.

Você pode copiar o conteúdo do arquivo `.env.example` e ajustar as variáveis de ambiente:
```bash
DATABASE_URL='sqlite:///database.db'
```

#### Para rodar o projeto:
```bash
task migrate_upgrade # Executa as migrações do banco de dados
task dev             # Roda o servidor de desenvolvimento
```
