from datetime import datetime
from typing import List, Optional
from uuid import uuid4

from app.db import find_by_email, find_by_id, insert, list_all, update
from app.models import Status, VoluntarioCreate, VoluntarioOut, VoluntarioUpdate


def create_voluntario(payload: VoluntarioCreate) -> VoluntarioOut:
    # unique email
    existing = find_by_email(payload.email)
    if existing and existing.get("status") == Status.ATIVO:
        raise ValueError("Email already exists")

    record = payload.dict()
    record["id"] = uuid4()
    record["inscricao_em"] = datetime.utcnow()
    record["status"] = Status.ATIVO
    record["deleted_at"] = None
    inserted = insert(record)
    return VoluntarioOut(**inserted)


def list_voluntarios(
    status: Optional[Status] = None,
    cargo: Optional[str] = None,
    disponibilidade: Optional[str] = None,
) -> List[VoluntarioOut]:
    items = list_all()
    results = []
    for it in items:
        if status and it.get("status") != status:
            continue
        if cargo and it.get("cargo_pretendido") != cargo:
            continue
        if disponibilidade and it.get("disponibilidade") != disponibilidade:
            continue
        results.append(VoluntarioOut(**it))
    return results


def get_voluntario(vol_id) -> Optional[VoluntarioOut]:
    v = find_by_id(vol_id)
    if not v:
        return None
    return VoluntarioOut(**v)


def update_voluntario(vol_id, payload: VoluntarioUpdate) -> Optional[VoluntarioOut]:
    v = find_by_id(vol_id)
    if not v:
        return None
    data = payload.dict(exclude_unset=True)
    # if updating email, check uniqueness
    if "email" in data:
        existing = find_by_email(data["email"])
        if (
            existing
            and str(existing["id"]) != str(vol_id)
            and existing.get("status") == Status.ATIVO
        ):
            raise ValueError("Email already exists")
    updated = update(vol_id, data)
    return VoluntarioOut(**updated)


def soft_delete(vol_id) -> Optional[VoluntarioOut]:
    v = find_by_id(vol_id)
    if not v:
        return None
    if v.get("status") == Status.INATIVO:
        return VoluntarioOut(**v)
    updated = update(
        vol_id, {"status": Status.INATIVO, "deleted_at": datetime.utcnow()}
    )
    return VoluntarioOut(**updated)
