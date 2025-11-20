from datetime import datetime, timezone
from typing import List, Optional
from uuid import UUID, uuid4

from app.db import find_by_email, find_by_id, insert, list_all, update
from app.models import Status, VoluntarioCreate, VoluntarioOut, VoluntarioUpdate


def create_voluntario(payload: VoluntarioCreate) -> VoluntarioOut:
    """Cria um voluntário novo. Verifica email único."""
    existing = find_by_email(payload.email)
    if existing and existing.get("status") == Status.ATIVO:
        raise ValueError("Email already exists")

    record = payload.model_dump()
    record["id"] = uuid4()
    record["inscricao_em"] = datetime.now(timezone.utc)
    record["status"] = Status.ATIVO
    record["deleted_at"] = None

    inserted = insert(record)
    return VoluntarioOut(**inserted)


def list_voluntarios(
    status: Optional[Status] = None,
    cargo: Optional[str] = None,
    disponibilidade: Optional[str] = None,
) -> List[VoluntarioOut]:
    """Lista voluntários com filtros opcionais."""
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


def get_voluntario(vol_id: UUID) -> Optional[VoluntarioOut]:
    """Retorna um voluntário pelo ID, ou None se não existir."""
    v = find_by_id(vol_id)
    if not v:
        return None
    return VoluntarioOut(**v)


def update_voluntario(
    vol_id: UUID, payload: VoluntarioUpdate
) -> Optional[VoluntarioOut]:
    """Atualiza um voluntário. Verifica unicidade de email."""
    v = find_by_id(vol_id)
    if not v:
        return None

    data = payload.model_dump(exclude_unset=True)

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


def soft_delete(vol_id: UUID) -> Optional[VoluntarioOut]:
    """Exclusão lógica de um voluntário pelo ID."""
    v = find_by_id(vol_id)
    if not v:
        return None
    if v.get("status") == Status.INATIVO:
        return VoluntarioOut(**v)

    updated = update(
        vol_id, {"status": Status.INATIVO, "deleted_at": datetime.now(timezone.utc)}
    )
    return VoluntarioOut(**updated)
