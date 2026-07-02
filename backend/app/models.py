import enum
from datetime import date
from sqlalchemy import Column, Integer, String, Float, Boolean, Date, Enum, ForeignKey, Table, Text
from sqlalchemy.orm import relationship
from app.database import Base


class PerfilEnum(str, enum.Enum):
    admin = "admin"
    recrutador = "recrutador"
    visualizador = "visualizador"


class Usuario(Base):
    __tablename__ = "usuarios"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False, index=True)
    senha_hash = Column(String, nullable=False)
    perfil = Column(Enum(PerfilEnum), nullable=False, default=PerfilEnum.visualizador)

class ModalidadeEnum(str, enum.Enum):
    presencial = "presencial"
    remoto = "remoto"
    hibrido = "hibrido"

class TipoContratoEnum(str, enum.Enum):
    CLT = "CLT"
    PJ = "PJ"
    temporario = "temporario"
    estagio = "estagio"

class PublicoAlvoEnum(str, enum.Enum):
    masculino = "masculino"
    feminino = "feminino"
    ambos = "ambos"

class StatusVagaEnum(str, enum.Enum):
    aberta = "aberta"
    encerrada = "encerrada"

class NivelRequisitoEnum(str, enum.Enum):
    obrigatorio = "obrigatorio"
    desejavel = "desejavel"

class StatusCandidaturaEnum(str, enum.Enum):
    pendente = "pendente"
    em_analise = "em_analise"
    aprovado = "aprovado"
    reprovado = "reprovado"

vaga_beneficio = Table(
    "vaga_beneficio",
    Base.metadata,
    Column("vaga_id", Integer, ForeignKey("vagas.id"), primary_key=True),
    Column("beneficio_id", Integer, ForeignKey("beneficios.id"), primary_key=True),
)

vaga_requisito = Table(
    "vaga_requisito",
    Base.metadata,
    Column("vaga_id", Integer, ForeignKey("vagas.id"), primary_key=True),
    Column("requisito_id", Integer, ForeignKey("requisitos.id"), primary_key=True),
)

class Empresa(Base):
    __tablename__ = "empresas"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    cnpj = Column(String, unique=True, nullable=False)
    setor = Column(String, nullable=False)
    descricao = Column(Text)
    cidade = Column(String, nullable=False)
    estado = Column(String(2), nullable=False)
    vagas = relationship("Vaga", back_populates="empresa")

class Beneficio(Base):
    __tablename__ = "beneficios"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    descricao = Column(Text)
    vagas = relationship("Vaga", secondary=vaga_beneficio, back_populates="beneficios")

class Requisito(Base):
    __tablename__ = "requisitos"
    id = Column(Integer, primary_key=True, index=True)
    descricao = Column(Text, nullable=False)
    nivel = Column(Enum(NivelRequisitoEnum), nullable=False)
    vagas = relationship("Vaga", secondary=vaga_requisito, back_populates="requisitos")

class Vaga(Base):
    __tablename__ = "vagas"
    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String, nullable=False)
    local = Column(String, nullable=False)
    salario = Column(Float)
    modalidade = Column(Enum(ModalidadeEnum), nullable=False)
    horario = Column(String)
    tipo_contrato = Column(Enum(TipoContratoEnum), nullable=False)
    publico_alvo = Column(Enum(PublicoAlvoEnum), default=PublicoAlvoEnum.ambos)
    vaga_pcd = Column(Boolean, default=False)
    status = Column(Enum(StatusVagaEnum), default=StatusVagaEnum.aberta)
    data_publicacao = Column(Date, default=date.today)
    data_abertura = Column(Date, default=date.today)
    data_fechamento = Column(Date, nullable=True)
    quantidade_vagas = Column(Integer, default=1)
    empresa_id = Column(Integer, ForeignKey("empresas.id"), nullable=False)
    empresa = relationship("Empresa", back_populates="vagas")
    beneficios = relationship("Beneficio", secondary=vaga_beneficio, back_populates="vagas")
    requisitos = relationship("Requisito", secondary=vaga_requisito, back_populates="vagas")
    candidaturas = relationship("Candidatura", back_populates="vaga")

class Candidato(Base):
    __tablename__ = "candidatos"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    telefone = Column(String)
    cidade = Column(String)
    estado = Column(String(2))
    data_nascimento = Column(Date)
    candidaturas = relationship("Candidatura", back_populates="candidato")

class Candidatura(Base):
    __tablename__ = "candidaturas"
    id = Column(Integer, primary_key=True, index=True)
    candidato_id = Column(Integer, ForeignKey("candidatos.id"), nullable=False)
    vaga_id = Column(Integer, ForeignKey("vagas.id"), nullable=False)
    data_candidatura = Column(Date, default=date.today)
    status = Column(Enum(StatusCandidaturaEnum), default=StatusCandidaturaEnum.pendente)
    candidato = relationship("Candidato", back_populates="candidaturas")
    vaga = relationship("Vaga", back_populates="candidaturas")
