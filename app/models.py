from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class Disponibilidade(str, Enum):
    MANHA = "manha"
    TARDE = "tarde"
    NOITE = "noite"
    FIM_DE_SEMANA = "fim_de_semana"
    INDEFINIDO = "indefinido"


class Status(str, Enum):
    ATIVO = "ativo"
    INATIVO = "inativo"


class VoluntarioBase(BaseModel):
    nome: str = Field(..., min_length=2)
    email: EmailStr
    telefone: str = Field(..., min_length=6)
    cargo_pretendido: str
    disponibilidade: Disponibilidade = Disponibilidade.INDEFINIDO


class VoluntarioCreate(VoluntarioBase):
    pass


class VoluntarioUpdate(BaseModel):
    nome: Optional[str] = None
    email: Optional[EmailStr] = None
    telefone: Optional[str] = None
    cargo_pretendido: Optional[str] = None
    disponibilidade: Optional[Disponibilidade] = None
    status: Optional[Status] = None


class VoluntarioOut(VoluntarioBase):
    id: UUID
    status: Status
    inscricao_em: datetime
    deleted_at: Optional[datetime] = None

    # Configuração correta para Pydantic v2
    model_config = ConfigDict(from_attributes=True)
