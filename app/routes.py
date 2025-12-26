from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, HTTPException, Query, status

from app import crud
from app.models import (
    Disponibilidade,
    Status,
    VoluntarioCreate,
    VoluntarioOut,
    VoluntarioUpdate,
)

router = APIRouter()


@router.post("/", response_model=VoluntarioOut, status_code=status.HTTP_201_CREATED)
def create_voluntario(payload: VoluntarioCreate):
    try:
        return crud.create_voluntario(payload)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))


@router.get("/", response_model=List[VoluntarioOut])
def list_voluntarios(
    status: Optional[Status] = Query(None),
    cargo: Optional[str] = Query(None),
    disponibilidade: Optional[Disponibilidade] = Query(None),
):
    return crud.list_voluntarios(
        status=status, cargo=cargo, disponibilidade=disponibilidade
    )


@router.get("/{vol_id}", response_model=VoluntarioOut)
def get_voluntario(vol_id: UUID):
    v = crud.get_voluntario(vol_id)
    if not v:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Voluntário não encontrado"
        )
    return v


@router.put("/{vol_id}", response_model=VoluntarioOut)
def put_voluntario(vol_id: UUID, payload: VoluntarioUpdate):
    v = crud.update_voluntario(vol_id, payload)

    if not v:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Voluntário não encontrado",
        )

    return v


@router.delete("/{vol_id}", response_model=VoluntarioOut)
def delete_voluntario(vol_id: UUID):
    v = crud.soft_delete(vol_id)
    if not v:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Voluntário não encontrado"
        )
    return v
