# PoliBot (Chatbot do Poliedro)

Backend da aplicação PoliBot, desenvolvido com Django e Python. Esta API é responsável por toda a lógica de negócio, gerenciamento de usuários e persistência de dados, sendo consumida por um frontend em React Expo.

O ambiente de desenvolvimento é totalmente containerizado com Docker para garantir consistência e facilidade na execução.

## ✨ Tecnologias

* Python 3.11
* Django & Django REST Framework
* SQLite3
* Docker & Docker Compose

## 🚀 Como Executar o Projeto

Você precisará ter o **Docker** e o **Docker Compose** instalados em sua máquina.

1.  **Clone o repositório:**
    ```bash
    git clone [https://github.com/Poliedro-Chatbot-Polibot/backend_django](https://github.com/Poliedro-Chatbot-Polibot/backend_django)
    ```

2.  **Navegue até a pasta do projeto:**
    ```bash
    cd backend_django
    ```

3.  **Crie e configure as variáveis de ambiente:**
    Copie o arquivo de exemplo `.env.example` para criar seu próprio arquivo `.env`.
    ```bash
    cp .env.example .env
    ```
    Depois, abra o arquivo `.env` e defina os valores necessários para `SECRET_KEY`, `DEBUG`, etc.

4.  **Suba os containers com Docker Compose:**
    Este comando irá construir a imagem da aplicação (instalando as dependências do `requirements.txt` automaticamente), aplicar as migrações do banco de dados e iniciar o servidor da API.
    ```bash
    docker-compose up -d --build
    ```

**Pronto!** A API estará disponível em `http://localhost:8000`.

O banco de dados SQLite é persistido usando um volume Docker, então seus dados estarão seguros mesmo que o container seja reiniciado.

## 🔗 Conexão com o Frontend

O repositório do frontend (React Expo) pode ser encontrado em: [Poliedro-Chatbot-Polibot/polibot_v1](https://github.com/Poliedro-Chatbot-Polibot/polibot_v1).

Para que o frontend se conecte a esta API, configure a URL base das chamadas para `http://localhost:8000`.

## 📖 Endpoints da API

| Método | Endpoint                    | Descrição                                 |
| :----- | :-------------------------- | :---------------------------------------- |
| `GET`  | `/admin/`                   | Acesso à área administrativa do Django.   |
| `GET`  | `/api/`                     | Acesso às APIs de pedidos.                |
| `GET`  | `/auth/`                    | Acesso às APIs de Usuários e Registros.   |

## 🛑 Como Parar a Aplicação

Para parar o container da aplicação, use o comando:
```bash
docker-compose down
```

## 👨‍💻 Autores

* Victhor Castro
* Pedro Canova
* Robert Kevyn
