# PRIMEIRA FILA


## Descrição do projeto


Imagine um site onde o usuário pode entrar para ver quais filmes estão passando nos cinemas perto de onde ele mora, e poder ver facilmente qual a programação para os filmes em cada um desses cinemas, além de informações de cada filme, como titulo, sinopse, atores, gênero, etc, além de poder comprar ingressos online. Cada cinema tem ferramentas para controlar as sessões de filme, as salas em que vão passar, o filme a ser passado e a disposição de assentos de suas salas.


## Acesso rápido


- [1.0 Visão Geral](#10-visão-geral)
  - [Tecnologias usadas](#tecnologias-usadas)
  - [1.1 URL base da aplicação](#11-url-base-da-aplicação)
- [2.0 Diagrama e relações](#20-diagrama-e-relações)
  - [Link para acesso ao Diagrama](#link-para-acesso-ao-diagrama)
- [3.0 Início Rápido](#30-início-rápido)
- [4.0 Autenticação e rotas](#40-autenticação-e-rotas)
- [5.0 Links:](#50-links)
  - [Documentação detalhada das rotas com swagger:](#documentação-detalhada-das-rotas-com-swagger)
  - [Download do arquivo JSON para usar no Insomnia:](#download-do-arquivo-json-para-usar-no-insomnia)


## 1.0 Visão Geral

### Tecnologias usadas


#### Principais dependências instaladas na aplicação:

- [Django](https://www.djangoproject.com/)
- [djangorestframework](https://www.django-rest-framework.org/)
- [djangorestframework-simplejwt](https://django-rest-framework-simplejwt.readthedocs.io/en/latest/)
- [black](https://pypi.org/project/black/)
- [psycopg2-binary](https://pypi.org/project/psycopg2-binary/)
- [drf-spectacular](https://drf-spectacular.readthedocs.io/en/latest/)
- [ipdb](https://pypi.org/project/ipdb/)
- [python-dotenv](https://pypi.org/project/python-dotenv/)
- [gunicorn](https://gunicorn.org/)
- [coverage](https://coverage.readthedocs.io/en/6.4.2/)
- [boto3](https://pypi.org/project/boto3/)
- [django-storages](https://pypi.org/project/django-storages/)
- [django-qr-code](https://pypi.org/project/django-qr-code/)
- [whitenoise](http://whitenoise.evans.io/en/stable/)

---

#### Principais ferramentas para a aplicação:


- [Sqlite3](https://www.sqlite.org/index.html)
- [Postgres](https://www.postgresql.org/)
- [Python](https://www.python.org/)
- [Docker](https://www.docker.com/)
- [AWS](https://aws.amazon.com/pt/)
- [Railway](https://railway.app/)

---

## 1.1 URL base da aplicação:


### https://primeira-fila-api.up.railway.app/

---

#### [ Voltar para o topo ](#acesso-rápido)


## 2.0 Diagrama e relações

![DER](der.png)

### Link para acesso ao Diagrama


- #### https://dbdiagram.io/d/62c6c926cc1bc14cc572f7ea

---

## 3.0 Início Rápido

Após clonar o projeto em sua máquina, instale as dependências em um ambiente virtual e rode as migrações com o comando:

```shell
python -m venv venv --upgrade-deps && source venv/bin/activate && pip install -r requirements.txt && python manage.py migrate
```

Em seguida, crie um arquivo **.env**, copiando o formato do arquivo **.env.example** e configure as variáveis de ambiente com suas credenciais.

---

#### [ Voltar para o topo ](#acesso-rápido)


## 4.0 Autenticação e rotas

O sistema de autenticação é baseado em _Json Web Token_(JWT). Sendo assim, tome o cuidado de enviar o header de _Authorization_ de acordo com o padrão `Bearer {token}` (note o espaço entre a palavra _Bearer_ e o _token_).

Esta sessão dá uma visão geral dos endpoints da aplicação e resume brevemente o que eles fazem. Para uma explicação mais detalhada sobre os corpos de requisição, query params e retornos esperados, veja a [documentação com swagger](https://primeira-fila.herokuapp.com/docs/).

- ### User:

  - #### `GET - /users/self/`
    - Lista as informações do próprio usuário
    - **Autenticação**:
      - Token do usuario

  - #### `POST - /users/`
    - Registra um novo usuário. **É necessário confirmar a conta por email**. Caso deseje se cadastrar como um gerente de cinema, basta passar a chave `is_staff` com o valor `true` no corpo da requisição.

  - #### `PATCH - /users/self/`
    - Atualiza informações do próprio usuário
    - **Autenticação**:
      - Token do usuario

  - #### `DELETE - /users/self/`
    - Apaga o registro do próprio usuário
    - **Autenticação**:
      - Token do usuario

---

- ### Login:

  - #### `POST - /sessions/token/`
    - Faz login na aplicação. Retorna um par de `access` e `refresh` tokens.

  - #### `POST - /sessions/token/refresh/`
    - Quando o `access token` tiver expirado, você pode usar essa rota para ganhar _um novo par de tokens_.

---

- ### Cinema:

  - #### `GET - /cinemas/`
    - Lista todos os cinemas

  - #### `GET - /cinemas/<cine_id>/movies/<movie_id>/movie-sessions/`
    - Lista todas as sessões de filme de um filme específico em um cinema específico
    - **Autenticação**:
      - Token do(a) gerente/responsável(`"is_staff": true`) do cinema

  - #### `POST - /cinemas/`
    - Registra um novo cinema
    - **Autenticação**:
      - Token do(a) gerente/responsável(`"is_staff": true`) do cinema

  - #### `PATCH - /cinemas/<cine_id>/`
    - Atualiza informações de um cinema
    - **Autenticação**:
      - Token do(a) gerente/responsável(`"is_staff": true`) do cinema

  - #### `DELETE - /cinemas/<cine_id>/movie-sessions/<session_id>/tickets/`
    - Apaga o registro de um cinema
    - **Autenticação**:
      - Token do(a) gerente/responsável(`"is_staff": true`) do cinema

---

- ### Room:

  - #### `GET - /cinemas/<cine_id>/rooms/`
    - Lista todas as salas de um cinema

  - #### `GET - /cinemas/<cine_id>/rooms/<room_id>/`
    - Retorna informações detalhadas sobre uma sala de um cinema

  - #### `POST - /cinemas/<cine_id>/rooms/`
    - Registra uma nova sala para um cinema
    - **Autenticação**:
      - Token do(a) gerente/responsável(`"is_staff": true`) do cinema

  - #### `PATCH - cinemas/<cine_id>/rooms/<room_id>/`
    - Atualiza informações de uma sala em um cinema
    - **Autenticação**:
      - Token do(a) gerente/responsável(`"is_staff": true`) do cinema

  - #### `DELETE - /cinemas/<cine_id>/rooms/<room_id>/`
    - Apaga o registro de uma sala em um cinema
    - **Autenticação**:
      - Token do(a) gerente/responsável(`"is_staff": true`) do cinema

---

- ### Movie:

  - #### `GET - /movies/all/`
    - Lista todos os filmes cadastrados na aplicação

  - #### `GET - /movies/`
    - Lista todos os filmes que estão em cartaz (ou seja, que possuem alguma sessão de filme marcada)

  - #### `GET - /movies/<movie_id>/`
    - Retorna informações detalhadas sobre um filme

  - #### `GET - /cinemas/<cine_id>/movies/`
    - Lista todos os filmes que estão em cartaz (ou seja, que possuem alguma sessão de filme marcada) em um cinema específico

  - #### `POST - /movies/`
    - Registra um novo filme
    - **Autenticação**:
      - Token do(a) **superuser** (ADM)

  - #### `PATCH - /movies/<movie_id>/`
    - Atualiza informações de um filme
    - **Autenticação**:
      - Token do(a) **superuser** (ADM)

  - #### `DELETE - /movies/<movie_id>/`
    - Apaga o registro de um filme
    - **Autenticação**:
      - Token do(a) **superuser** (ADM)

---

- ### Movie Session:

  - #### `GET - /cinemas/<cine_id>/movie-sessions/<session_id>/`
    - Retorna informações detalhadas sobre uma sessão de filme em um cinema

  - #### `GET - /cinemas/<cine_id>/movies/<movie_id>/movie-sessions/`
    - Lista todas as sessões de filme de um filme específico em um cinema específico

  - #### `GET - /cinemas/<cine_id>/movie-sessions/`
    - Lista todas as sessões de filme em um cinema

  - #### `POST - /cinemas/<cine_id>/rooms/<room_id>/movies/<movie_id>/movie-sessions/`
    - Registra uma nova sessão de filme para o filme `movie_id`, na sala `room_id` do cinema `cine_id`
    - **Autenticação**:
      - Token do(a) gerente/responsável(`"is_staff": true`) do cinema

  - #### `PATCH - /cinemas/<cine_id>/movie-sessions/<session_id>/`
    - Atualiza informações de uma sessão de filme em um cinema
    - **Autenticação**:
      - Token do(a) gerente/responsável(`"is_staff": true`) do cinema

  - #### `DELETE - /cinemas/<cine_id>/movie-sessions/<session_id>/`
    - Apaga o registro de uma sessão de filme em um cinema
    - **Autenticação**:
      - Token do(a) gerente/responsável(`"is_staff": true`) do cinema

---

- ### Ticket:

  - #### `GET - /cinemas/<cine_id>/movie-sessions/<session_id>/tickets/<ticket_id>/`
    - Retorna informações detalhadas sobre o ticket `ticket_id`, para a sessão de filme `session_id`, no cinema `cine_id`

  - #### `GET - /users/tickets/<ticket_id>/`
    - Retorna informações detalhadas sobre um ticket comprado por um usuário
    - **Autenticação**:
      - Token do usuario **dono do ticket**

  - #### `GET - /cinemas/<cine_id>/movie-sessions/<session_id>/tickets/`
    - Lista todos os tickets de uma sessão
    - **Autenticação**:
      - Token do(a) gerente/responsável(`"is_staff": true`) do cinema

  - #### `POST - /cinemas/<cine_id>/movie-sessions/<session_id>/tickets/`
    - Compra um novo ticket, para a sessão de filme `session_id` no cinema `cine_id`
    - **Autenticação**:
      - Token do usuario

  - #### `PATCH - /cinemas/<cine_id>/movie-sessions/<session_id>/tickets/<ticket_id>/`
    - Atualiza os assentos escolhidos na compra do ticket `ticket_id`, para a sessão `session_id` no cinema `cine_id`
    - **Autenticação**:
      - Token do usuario **dono do ticket**

---

## 5.0 Links:

### Documentação detalhada das rotas com swagger:

- #### https://primeira-fila-api.up.railway.app/docs/

### Download do arquivo JSON para usar no Insomnia:

- #### https://drive.google.com/file/d/1rV2Tagth1IGDjYe6A6dx75P34wEOOmrU/view?usp=sharing

##### [ Voltar para o topo ](#acesso-rápido)
