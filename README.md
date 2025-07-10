![image](https://github.com/user-attachments/assets/ac86aeb6-5672-4d1a-8fda-0da478cd706d)

# 📊 API CNAE Processada (Python - FastAPI)

API para buscar e formatar dados da Classificação Nacional de Atividades Econômicas (CNAE) fornecidos pelo IBGE. <br>
A API retorna informações de classe e subclasse com códigos concatenados e dados organizados.

---

## 🚀 Funcionalidades

- ✅ Retorna todos os CNAEs com classe e subclasse.
- ✅ Garante unicidade dos registros (sem duplicatas).
- ✅ Inclui documentação interativa via Swagger (OpenAPI UI).

---

## 🛠️ Tecnologias Utilizadas

- **Python 3.9+** – Linguagem de programação.
- **FastAPI** – Framework web moderno e rápido para construção de APIs.
- **Uvicorn** – Servidor ASGI para rodar aplicações FastAPI.
- **Requests** – Biblioteca HTTP para comunicação com a API do IBGE.
- **Pydantic** – Para validação de dados e serialização.

---

## 📦 Instalação e Execução

1.  Clone o repositório:

    ```bash
    git clone [https://github.com/seu-usuario/seu-repositorio.git](https://github.com/seu-usuario/seu-repositorio.git)
    cd seu-repositorio
    ```

2.  Crie e ative um ambiente virtual (opcional, mas recomendado):

    ```bash
    python -m venv venv
    # No Windows
    .\venv\Scripts\activate
    # No macOS/Linux
    source venv/bin/activate
    ```

3.  Instale as dependências:

    ```bash
    pip install -r requirements.txt
    ```

4.  Inicie o servidor:

    ```bash
    uvicorn main:app --reload --port 1000
    ```
    O servidor estará rodando em `http://127.0.0.1:1000`.

---

## 📚 Documentação da API

Acesse a interface Swagger (OpenAPI UI) em: