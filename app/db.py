# DB fake: lista em memória
from datetime import datetime
from typing import Dict, List, Optional
from uuid import UUID, uuid4

from app.models import Status

_DB: List[Dict] = []


def _normalize_email(email: str) -> str:
    return email.strip().lower()


def reset_db():
    _DB.clear()


def list_all():
    return _DB


def find_by_id(vol_id):
    for item in _DB:
        if str(item["id"]) == str(vol_id):
            return item
    return None


def find_by_email(email: str):
    email = _normalize_email(email)
    for item in _DB:
        if item["email"] == email:
            return item
    return None


def insert(data: Dict):
    # Normaliza email
    if "email" in data and data["email"]:
        data["email"] = _normalize_email(data["email"])

    # Garante ID único se não existir
    if "id" not in data:
        data["id"] = uuid4()

    # Garante status ativo se não existir
    if "status" not in data:
        data["status"] = Status.ATIVO

    _DB.append(data)
    return data


def update(vol_id, data: Dict):
    v = find_by_id(vol_id)
    if not v:
        return None

    if "email" in data and data["email"]:
        normalized_email = _normalize_email(data["email"])
        existing = find_by_email(normalized_email)
        if existing and existing["id"] != v["id"]:
            raise ValueError("Email já cadastrado")

        data["email"] = normalized_email

    v.update(data)
    return v


def soft_delete(vol_id):
    v = find_by_id(vol_id)
    if not v:
        return None

    v["status"] = Status.INATIVO
    v["deleted_at"] = datetime.utcnow()
    return v
