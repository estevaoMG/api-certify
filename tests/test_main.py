from fastapi.testclient import TestClient

from app.db import list_all, reset_db
from main import app

client = TestClient(app)


def setup_function():
    reset_db()


# =========================
# CREATE
# =========================


def test_criar_voluntario_valido():
    payload = {
        "nome": "João Silva",
        "email": "joao@example.com",
        "telefone": "+5521999998888",
        "cargo_pretendido": "Apoio",
        "disponibilidade": "manha",
    }

    r = client.post("/voluntarios/", json=payload)

    assert r.status_code == 201
    data = r.json()
    assert data["email"] == "joao@example.com"
    assert data["status"] == "ativo"
    assert len(list_all()) == 1


def test_nao_permitir_email_duplicado():
    payload = {
        "nome": "Maria",
        "email": "maria@example.com",
        "telefone": "+5521911112222",
        "cargo_pretendido": "Coordenador",
        "disponibilidade": "tarde",
    }

    r1 = client.post("/voluntarios/", json=payload)
    assert r1.status_code == 201

    r2 = client.post("/voluntarios/", json=payload)
    assert r2.status_code == 409


def test_email_normalizado_case_e_espacos():
    r = client.post(
        "/voluntarios/",
        json={
            "nome": "Alpha",
            "email": "  ALPHA@EXAMPLE.COM ",
            "telefone": "+5511999999999",
            "cargo_pretendido": "Apoio",
            "disponibilidade": "manha",
        },
    )

    assert r.status_code == 201
    assert r.json()["email"] == "alpha@example.com"

    r2 = client.post(
        "/voluntarios/",
        json={
            "nome": "Beta",
            "email": "alpha@example.com",
            "telefone": "+5511888888888",
            "cargo_pretendido": "Apoio",
            "disponibilidade": "manha",
        },
    )

    assert r2.status_code == 409


def test_nao_permitir_telefone_invalido():
    r = client.post(
        "/voluntarios/",
        json={
            "nome": "Telefone Ruim",
            "email": "telefone@exemplo.com",
            "telefone": "21999998888",  # inválido
            "cargo_pretendido": "Apoio",
            "disponibilidade": "manha",
        },
    )

    assert r.status_code == 422


# =========================
# UPDATE
# =========================


def test_atualizar_voluntario():
    r = client.post(
        "/voluntarios/",
        json={
            "nome": "João",
            "email": "joao@update.com",
            "telefone": "+5521999990000",
            "cargo_pretendido": "Apoio",
            "disponibilidade": "manha",
        },
    )

    vid = r.json()["id"]

    upd = client.put(f"/voluntarios/{vid}", json={"nome": "João Atualizado"})

    assert upd.status_code == 200
    assert upd.json()["nome"] == "João Atualizado"


def test_update_nao_permite_email_existente():
    # Cria o primeiro voluntário (v1)
    r1 = client.post(
        "/voluntarios/",
        json={
            "nome": "Ana",
            "email": "a@exemplo.com",
            "telefone": "+5521999991111",
            "cargo_pretendido": "Apoio",
            "disponibilidade": "manha",
        },
    )
    assert r1.status_code == 201, f"Falha ao criar v1: {r1.json()}"
    v1 = r1.json()

    # Cria o segundo voluntário (v2)
    r2 = client.post(
        "/voluntarios/",
        json={
            "nome": "Bob",
            "email": "b@exemplo.com",
            "telefone": "+5521999992222",
            "cargo_pretendido": "Apoio",
            "disponibilidade": "manha",
        },
    )
    assert r2.status_code == 201, f"Falha ao criar v2: {r2.json()}"
    v2 = r2.json()

    # Tenta atualizar o email de v2 para o email de v1 (diferente case)
    r_update = client.put(
        f"/voluntarios/{v2['id']}",
        json={"email": "A@EXEMPLO.COM"},  # maiúsculo para testar normalização
    )

    # Deve retornar 409 Conflict
    assert r_update.status_code == 409, f"Update inesperado: {r_update.json()}"


# =========================
# DELETE (SOFT)
# =========================


def test_soft_delete():
    r = client.post(
        "/voluntarios/",
        json={
            "nome": "Delete Me",
            "email": "delete@exemplo.com",
            "telefone": "+5511993333333",
            "cargo_pretendido": "Apoio",
            "disponibilidade": "manha",
        },
    )

    vid = r.json()["id"]

    d = client.delete(f"/voluntarios/{vid}")
    assert d.status_code in (200, 204)

    g = client.get(f"/voluntarios/{vid}")
    assert g.status_code == 404


# =========================
# LIST
# =========================


def test_listar_apenas_ativos():
    client.post(
        "/voluntarios/",
        json={
            "nome": "Ativo",
            "email": "ativo@exemplo.com",
            "telefone": "+5511994444444",
            "cargo_pretendido": "Apoio",
            "disponibilidade": "manha",
        },
    )

    v = client.post(
        "/voluntarios/",
        json={
            "nome": "Inativo",
            "email": "inativo@exemplo.com",
            "telefone": "+5511995555555",
            "cargo_pretendido": "Apoio",
            "disponibilidade": "manha",
        },
    ).json()

    client.delete(f"/voluntarios/{v['id']}")

    r = client.get("/voluntarios/")
    emails = [v["email"] for v in r.json()]

    assert "ativo@exemplo.com" in emails
    assert "inativo@exemplo.com" not in emails
