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


def _get_voluntario_or_404(vol_id: UUID) -> VoluntarioOut:
    """Retorna o voluntário ou dispara 404 se não encontrado."""
    voluntario = crud.get_voluntario(vol_id)
    if not voluntario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Voluntário não encontrado"
        )
    return voluntario


@router.post(
    "/",
    response_model=VoluntarioOut,
    status_code=status.HTTP_201_CREATED,
    summary="Criar um novo voluntário",
    response_description="Os dados do voluntário criado",
)
def create_voluntario(payload: VoluntarioCreate) -> VoluntarioOut:
    """Cria um voluntário novo. Retorna 409 se o email já existir."""
    try:
        return crud.create_voluntario(payload)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))


@router.get(
    "/",
    response_model=List[VoluntarioOut],
    summary="Listar voluntários",
    response_description="Lista de voluntários filtrados",
)
def list_voluntarios(
    status: Optional[Status] = Query(None, description="Filtrar por status"),
    cargo: Optional[str] = Query(None, description="Filtrar por cargo pretendido"),
    disponibilidade: Optional[Disponibilidade] = Query(
        None, description="Filtrar por disponibilidade"
    ),
) -> List[VoluntarioOut]:
    """Lista todos os voluntários com filtros opcionais."""
    return crud.list_voluntarios(
        status=status, cargo=cargo, disponibilidade=disponibilidade
    )


@router.get(
    "/{vol_id}",
    response_model=VoluntarioOut,
    summary="Obter um voluntário",
    response_description="Dados do voluntário específico",
)
def get_voluntario(vol_id: UUID) -> VoluntarioOut:
    """Retorna os dados de um voluntário pelo ID."""
    return _get_voluntario_or_404(vol_id)


@router.put(
    "/{vol_id}",
    response_model=VoluntarioOut,
    summary="Atualizar um voluntário",
    response_description="Dados do voluntário atualizado",
)
def update_voluntario(vol_id: UUID, payload: VoluntarioUpdate) -> VoluntarioOut:
    """Atualiza os dados de um voluntário. Retorna 404 se não existir ou 409 se houver conflito."""
    try:
        updated = crud.update_voluntario(vol_id, payload)
        if not updated:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Voluntário não encontrado",
            )
        return updated
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))


@router.delete(
    "/{vol_id}",
    response_model=VoluntarioOut,
    summary="Deletar um voluntário",
    response_description="Dados do voluntário deletado",
)
def delete_voluntario(vol_id: UUID) -> VoluntarioOut:
    """Realiza exclusão lógica de um voluntário pelo ID."""
    voluntario = crud.soft_delete(vol_id)
    if not voluntario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Voluntário não encontrado"
        )
    return voluntario
