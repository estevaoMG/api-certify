from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field


class Status(str, Enum):
    ATIVO = "ativo"
    INATIVO = "inativo"


class Disponibilidade(str, Enum):
    MANHA = "manha"
    TARDE = "tarde"
    NOITE = "noite"


class VoluntarioBase(BaseModel):
    nome: str = Field(..., min_length=3, max_length=100)
    email: EmailStr
    telefone: str = Field(
        ..., regex=r"^\+55\d{10,11}$", description="Telefone no formato +55DDDXXXXXXXX"
    )

    cargo_pretendido: str = Field(..., min_length=2, max_length=50)
    disponibilidade: Disponibilidade


class VoluntarioCreate(VoluntarioBase):
    pass


class VoluntarioUpdate(BaseModel):
    nome: Optional[str] = Field(None, min_length=3, max_length=100)
    email: Optional[EmailStr] = None
    telefone: Optional[str] = Field(None, min_length=8, max_length=15)
    cargo_pretendido: Optional[str] = Field(None, min_length=2, max_length=50)
    disponibilidade: Optional[Disponibilidade] = None


class VoluntarioOut(VoluntarioBase):
    id: UUID
    inscricao_em: datetime
    status: Status
    deleted_at: Optional[datetime] = None
