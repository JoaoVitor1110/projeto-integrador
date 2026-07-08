from datetime import date
from typing import Optional, List
from pydantic import BaseModel, ConfigDict
from app.models import ModalidadeEnum, TipoContratoEnum, PublicoAlvoEnum, StatusVagaEnum, NivelRequisitoEnum, StatusCandidaturaEnum

# Empresa
class EmpresaCreate(BaseModel):
    nome: str
    cnpj: str
    setor: str
    descricao: Optional[str] = None
    cidade: str
    estado: str

class EmpresaResponse(EmpresaCreate):
    model_config = ConfigDict(from_attributes=True)
    id: int

# Usuario (resumido, para embed em VagaResponse)
class UsuarioResumo(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    nome: str
    email: str

# Beneficio
class BeneficioCreate(BaseModel):
    nome: str
    descricao: Optional[str] = None

class BeneficioResponse(BeneficioCreate):
    model_config = ConfigDict(from_attributes=True)
    id: int

# Requisito
class RequisitoCreate(BaseModel):
    descricao: str
    nivel: NivelRequisitoEnum

class RequisitoResponse(RequisitoCreate):
    model_config = ConfigDict(from_attributes=True)
    id: int

# Vaga
class VagaCreate(BaseModel):
    titulo: str
    local: str
    descricao: Optional[str] = None
    salario: Optional[float] = None
    modalidade: ModalidadeEnum
    horario: Optional[str] = None
    tipo_contrato: TipoContratoEnum
    publico_alvo: PublicoAlvoEnum = PublicoAlvoEnum.ambos
    vaga_pcd: bool = False
    status: StatusVagaEnum = StatusVagaEnum.aberta
    data_publicacao: Optional[date] = None
    data_abertura: Optional[date] = None
    data_fechamento: Optional[date] = None
    quantidade_vagas: int = 1
    empresa_id: int
    beneficios_nomes: List[str] = []
    requisitos_lista: List[dict] = []
    recrutador_id: Optional[int] = None

class VagaResponse(VagaCreate):
    model_config = ConfigDict(from_attributes=True)
    id: int
    empresa: EmpresaResponse
    recrutador: Optional[UsuarioResumo] = None
    beneficios: List[BeneficioResponse] = []
    requisitos: List[RequisitoResponse] = []

# Candidato
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

# Candidatura
class CandidaturaCreate(BaseModel):
    candidato_id: int
    vaga_id: int
    data_candidatura: Optional[date] = None
    status: StatusCandidaturaEnum = StatusCandidaturaEnum.pendente

class CandidaturaResponse(CandidaturaCreate):
    model_config = ConfigDict(from_attributes=True)
    id: int
    candidato: CandidatoResponse
    vaga: VagaResponse
