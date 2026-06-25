from datetime import date
from typing import Optional, List
from pydantic import BaseModel, ConfigDict
from app.models import ModalidadeEnum, TipoContratoEnum, PublicoAlvoEnum, StatusVagaEnum, NivelRequisitoEnum, StatusCandidaturaEnum


class EmpresaCreate(BaseModel):
    nome: str
    cnpj: str
    setor: Optional[str] = None
    descricao: Optional[str] = None
    cidade: Optional[str] = None
    estado: Optional[str] = None


class EmpresaResponse(EmpresaCreate):
    model_config = ConfigDict(from_attributes=True)
    id: int


class BeneficioCreate(BaseModel):
    nome: str
    descricao: Optional[str] = None


class BeneficioResponse(BeneficioCreate):
    model_config = ConfigDict(from_attributes=True)
    id: int


class RequisitoCreate(BaseModel):
    descricao: str
    nivel: NivelRequisitoEnum


class RequisitoResponse(RequisitoCreate):
    model_config = ConfigDict(from_attributes=True)
    id: int


class VagaCreate(BaseModel):
    titulo: str
    local: Optional[str] = None
    salario: Optional[float] = None
    modalidade: Optional[ModalidadeEnum] = None
    horario: Optional[str] = None
    tipo_contrato: Optional[TipoContratoEnum] = None
    publico_alvo: Optional[PublicoAlvoEnum] = None
    vaga_pcd: bool = False
    status: StatusVagaEnum = StatusVagaEnum.aberta
    data_publicacao: Optional[date] = None
    empresa_id: int
    beneficio_ids: List[int] = []
    requisito_ids: List[int] = []


class VagaResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    titulo: str
    local: Optional[str] = None
    salario: Optional[float] = None
    modalidade: Optional[ModalidadeEnum] = None
    horario: Optional[str] = None
    tipo_contrato: Optional[TipoContratoEnum] = None
    publico_alvo: Optional[PublicoAlvoEnum] = None
    vaga_pcd: bool
    status: StatusVagaEnum
    data_publicacao: Optional[date] = None
    empresa_id: int
    empresa: Optional[EmpresaResponse] = None
    beneficios: List[BeneficioResponse] = []
    requisitos: List[RequisitoResponse] = []


class CandidatoCreate(BaseModel):
    nome: str
    email: str
    telefone: Optional[str] = None
    cidade: Optional[str] = None
    estado: Optional[str] = None
    data_nascimento: Optional[date] = None


class CandidatoResponse(CandidatoCreate):
    model_config = ConfigDict(from_attributes=True)
    id: int


class CandidaturaCreate(BaseModel):
    candidato_id: int
    vaga_id: int
    data_candidatura: Optional[date] = None
    status: StatusCandidaturaEnum = StatusCandidaturaEnum.pendente


class CandidaturaResponse(CandidaturaCreate):
    model_config = ConfigDict(from_attributes=True)
    id: int
