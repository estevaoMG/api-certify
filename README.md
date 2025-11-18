# api-certify

Projeto de exemplo para o **Desafio Técnico - Sistema de Gerenciamento de Voluntários**.

## Como usar (com Poetry)

1. Instale o Poetry (se necessário):
   ```bash
   curl -sSL https://install.python-poetry.org | python3 -
   ```

2. Instale dependências:
   ```bash
   poetry install
   ```

3. Para entrar no shell do poetry (opcional):
   ```bash
   poetry shell
   ```

4. Executar a aplicação:
   ```bash
   poetry run task run
   # ou
   poetry run uvicorn main:app --reload
   ```

5. Testes:
   ```bash
   poetry run task test
   ```

## Endpoints

- `POST   /voluntarios` - Cadastrar novo voluntário
- `GET    /voluntarios` - Listar voluntários (com filtros)
- `GET    /voluntarios/<built-in function id>` - Buscar voluntário específico
- `PUT    /voluntarios/<built-in function id>` - Atualizar voluntário
- `DELETE /voluntarios/<built-in function id>` - Excluir voluntário (soft delete)

## Decisões técnicas

- Uso de **Poetry** para gerenciar dependências (obrigatório).
- Banco de dados fake (lista em memória) para facilitar correção.
- `email` é único (verificado em criação/atualização).
- `soft delete` implementado marcando `status = "inativo"` e `deleted_at`.
- Testes básicos com `pytest` incluídos.

## Observações

- Para persistência real, substitua o arquivo `app/db.py` por conexões a um banco (SQLAlchemy, etc).