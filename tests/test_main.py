from fastapi.testclient import TestClient

from app.db import list_all, reset_db
from main import app

client = TestClient(app)


def setup_function():
    reset_db()


def test_criar_voluntario_valido():
    payload = {
        "nome": "João Silva",
        "email": "joao@example.com",
        "telefone": "21999998888",
        "cargo_pretendido": "Apoio",
        "disponibilidade": "manha",
    }
    r = client.post("/voluntarios/", json=payload)
    assert r.status_code == 201
    data = r.json()
    assert data["email"] == payload["email"]
    assert data["status"] == "ativo"
    assert len(list_all()) == 1


def test_nao_permitir_email_duplicado():
    payload = {
        "nome": "Maria",
        "email": "maria@example.com",
        "telefone": "21911112222",
        "cargo_pretendido": "Coordenador",
        "disponibilidade": "tarde",
    }
    r1 = client.post("/voluntarios/", json=payload)
    assert r1.status_code == 201
    r2 = client.post("/voluntarios/", json=payload)
    assert r2.status_code == 409
