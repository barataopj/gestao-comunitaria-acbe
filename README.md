# Gestão Comunitária ACBE

MVP acadêmico da disciplina Projeto de Software, do curso de Análise e Desenvolvimento de Sistemas. O sistema auxilia representantes autorizados da Associação Comunitária do Bairro Esplanada (ACBE), em Belo Horizonte/MG, a registrar e acompanhar solicitações comunitárias.

## Funcionalidades implementadas

- Autenticação de usuários pelo mecanismo nativo do Django.
- Cadastro de solicitações com descrição e categoria.
- Geração de protocolo no formato SOL-00001.
- Consulta e filtro por categoria e status.
- Atualização de status (Recebida, Em análise, Encaminhada e Concluída).
- Histórico de movimentações com data, hora e usuário responsável.
- Área administrativa do Django.

## Tecnologias

- Python 3.12
- Django 5.2
- Bootstrap 5.3
- SQLite para desenvolvimento e testes; PostgreSQL configurável por variáveis de ambiente.
- Coverage.py para medir a cobertura dos testes.

## Como executar localmente

1. Instale Python 3.12.
2. Crie e ative um ambiente virtual:
   `python -m venv .venv`
3. Instale as dependências:
   `pip install -r requirements.txt`
4. Aplique as migrações:
   `python manage.py migrate`
5. Crie um usuário administrador:
   `python manage.py createsuperuser`
6. Inicie o servidor:
   `python manage.py runserver`
7. Acesse `http://127.0.0.1:8000/` e entre com o usuário criado.

## Executar testes e cobertura

Execute todos os testes automatizados:

```bash
coverage run --source=solicitacoes manage.py test
coverage report -m
```

A cobertura é calculada pelo Coverage.py sobre o código do aplicativo `solicitacoes`. O valor percentual só deve ser informado no relatório acadêmico após a execução bem-sucedida do comando e a consulta ao resultado apresentado no terminal ou na integração contínua do GitHub Actions.

## Banco de dados

Por padrão, o projeto utiliza SQLite para facilitar a execução local e dos testes. Para utilizar PostgreSQL, configure as variáveis de ambiente `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST` e `DB_PORT`.

## Segurança e escopo

O acesso às telas de solicitações exige autenticação. O Django fornece proteção CSRF, sessões e armazenamento seguro de senhas por meio de seus mecanismos nativos. Em implantação, configure uma chave secreta exclusiva, `DEBUG=0`, hosts permitidos, HTTPS e credenciais do banco fora do código-fonte.

Este MVP é acadêmico e deve utilizar dados fictícios durante o desenvolvimento e os testes. A integração automática com WhatsApp, redes sociais e órgãos públicos não faz parte do escopo atual.
