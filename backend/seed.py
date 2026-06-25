import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from datetime import date
from app.database import SessionLocal, engine
from app import models
from app.database import Base

Base.metadata.create_all(bind=engine)

def seed():
    db = SessionLocal()
    try:
        # Check if already seeded
        if db.query(models.Empresa).count() > 0:
            print("Banco de dados já populado. Nenhuma ação necessária.")
            return

        # Empresas
        empresas = [
            models.Empresa(nome="TechBrasil Soluções", cnpj="12.345.678/0001-90", setor="Tecnologia", descricao="Empresa de desenvolvimento de software", cidade="São Paulo", estado="SP"),
            models.Empresa(nome="Financeira Nordeste", cnpj="23.456.789/0001-01", setor="Financeiro", descricao="Banco regional com foco no nordeste brasileiro", cidade="Recife", estado="PE"),
            models.Empresa(nome="Saúde & Vida", cnpj="34.567.890/0001-12", setor="Saúde", descricao="Rede de clínicas e hospitais", cidade="Belo Horizonte", estado="MG"),
            models.Empresa(nome="LogiBrasil", cnpj="45.678.901/0001-23", setor="Logística", descricao="Empresa de transporte e logística nacional", cidade="Curitiba", estado="PR"),
            models.Empresa(nome="EduFuturo", cnpj="56.789.012/0001-34", setor="Educação", descricao="Plataforma de ensino online e presencial", cidade="Porto Alegre", estado="RS"),
        ]
        db.add_all(empresas)
        db.commit()
        print(f"✓ {len(empresas)} empresas inseridas")

        # Beneficios
        beneficios = [
            models.Beneficio(nome="Vale Refeição", descricao="R$ 35 por dia útil"),
            models.Beneficio(nome="Plano de Saúde", descricao="Plano médico Unimed nacional"),
            models.Beneficio(nome="Vale Transporte", descricao="Cobertura integral do transporte"),
            models.Beneficio(nome="Home Office", descricao="Flexibilidade para trabalho remoto"),
            models.Beneficio(nome="Gympass", descricao="Acesso a academias parceiras"),
        ]
        db.add_all(beneficios)
        db.commit()
        print(f"✓ {len(beneficios)} benefícios inseridos")

        # Requisitos
        requisitos = [
            models.Requisito(descricao="Graduação em Ciência da Computação ou áreas afins", nivel=models.NivelRequisitoEnum.obrigatorio),
            models.Requisito(descricao="Experiência com Python e FastAPI", nivel=models.NivelRequisitoEnum.obrigatorio),
            models.Requisito(descricao="Conhecimento em SQL e bancos de dados relacionais", nivel=models.NivelRequisitoEnum.obrigatorio),
            models.Requisito(descricao="Inglês técnico (leitura)", nivel=models.NivelRequisitoEnum.desejavel),
            models.Requisito(descricao="Experiência com metodologias ágeis", nivel=models.NivelRequisitoEnum.desejavel),
            models.Requisito(descricao="Formação em Administração, Economia ou Contabilidade", nivel=models.NivelRequisitoEnum.obrigatorio),
        ]
        db.add_all(requisitos)
        db.commit()
        print(f"✓ {len(requisitos)} requisitos inseridos")

        # Vagas
        vagas = [
            models.Vaga(titulo="Desenvolvedor Python Sênior", local="São Paulo, SP", salario=12000.0, modalidade=models.ModalidadeEnum.hibrido, horario="Segunda a Sexta, 9h-18h", tipo_contrato=models.TipoContratoEnum.CLT, publico_alvo=models.PublicoAlvoEnum.ambos, vaga_pcd=False, status=models.StatusVagaEnum.aberta, data_publicacao=date(2026, 6, 1), empresa_id=1),
            models.Vaga(titulo="Analista Financeiro", local="Recife, PE", salario=6500.0, modalidade=models.ModalidadeEnum.presencial, horario="Segunda a Sexta, 8h-17h", tipo_contrato=models.TipoContratoEnum.CLT, publico_alvo=models.PublicoAlvoEnum.ambos, vaga_pcd=True, status=models.StatusVagaEnum.aberta, data_publicacao=date(2026, 6, 5), empresa_id=2),
            models.Vaga(titulo="Enfermeiro(a) UTI", local="Belo Horizonte, MG", salario=5800.0, modalidade=models.ModalidadeEnum.presencial, horario="Plantão 12x36", tipo_contrato=models.TipoContratoEnum.CLT, publico_alvo=models.PublicoAlvoEnum.ambos, vaga_pcd=False, status=models.StatusVagaEnum.aberta, data_publicacao=date(2026, 6, 3), empresa_id=3),
            models.Vaga(titulo="Motorista de Carga", local="Curitiba, PR", salario=4200.0, modalidade=models.ModalidadeEnum.presencial, horario="Variável", tipo_contrato=models.TipoContratoEnum.CLT, publico_alvo=models.PublicoAlvoEnum.masculino, vaga_pcd=False, status=models.StatusVagaEnum.aberta, data_publicacao=date(2026, 6, 10), empresa_id=4),
            models.Vaga(titulo="Professor de Matemática", local="Porto Alegre, RS", salario=3500.0, modalidade=models.ModalidadeEnum.remoto, horario="Flexível", tipo_contrato=models.TipoContratoEnum.PJ, publico_alvo=models.PublicoAlvoEnum.ambos, vaga_pcd=False, status=models.StatusVagaEnum.aberta, data_publicacao=date(2026, 6, 8), empresa_id=5),
            models.Vaga(titulo="Estágio em Desenvolvimento Web", local="São Paulo, SP", salario=1500.0, modalidade=models.ModalidadeEnum.hibrido, horario="Segunda a Sexta, 6h/dia", tipo_contrato=models.TipoContratoEnum.estagio, publico_alvo=models.PublicoAlvoEnum.ambos, vaga_pcd=True, status=models.StatusVagaEnum.aberta, data_publicacao=date(2026, 6, 12), empresa_id=1),
            models.Vaga(titulo="Gerente de Projetos", local="São Paulo, SP", salario=15000.0, modalidade=models.ModalidadeEnum.hibrido, horario="Segunda a Sexta, 9h-18h", tipo_contrato=models.TipoContratoEnum.CLT, publico_alvo=models.PublicoAlvoEnum.ambos, vaga_pcd=False, status=models.StatusVagaEnum.aberta, data_publicacao=date(2026, 5, 28), empresa_id=1),
            models.Vaga(titulo="Assistente Administrativo", local="Recife, PE", salario=2800.0, modalidade=models.ModalidadeEnum.presencial, horario="Segunda a Sexta, 8h-17h", tipo_contrato=models.TipoContratoEnum.temporario, publico_alvo=models.PublicoAlvoEnum.ambos, vaga_pcd=True, status=models.StatusVagaEnum.aberta, data_publicacao=date(2026, 6, 15), empresa_id=2),
            models.Vaga(titulo="Técnico em Enfermagem", local="Belo Horizonte, MG", salario=3200.0, modalidade=models.ModalidadeEnum.presencial, horario="Plantão 12x36", tipo_contrato=models.TipoContratoEnum.CLT, publico_alvo=models.PublicoAlvoEnum.ambos, vaga_pcd=False, status=models.StatusVagaEnum.encerrada, data_publicacao=date(2026, 5, 20), empresa_id=3),
            models.Vaga(titulo="Analista de Logística", local="Curitiba, PR", salario=5500.0, modalidade=models.ModalidadeEnum.hibrido, horario="Segunda a Sexta, 8h-17h", tipo_contrato=models.TipoContratoEnum.CLT, publico_alvo=models.PublicoAlvoEnum.ambos, vaga_pcd=False, status=models.StatusVagaEnum.aberta, data_publicacao=date(2026, 6, 18), empresa_id=4),
        ]
        db.add_all(vagas)
        db.commit()

        # Associate beneficios and requisitos to vagas
        vagas[0].beneficios = [beneficios[0], beneficios[1], beneficios[2], beneficios[3]]
        vagas[0].requisitos = [requisitos[0], requisitos[1], requisitos[2], requisitos[3]]
        vagas[1].beneficios = [beneficios[0], beneficios[1], beneficios[2]]
        vagas[1].requisitos = [requisitos[5], requisitos[4]]
        vagas[5].beneficios = [beneficios[0], beneficios[2], beneficios[4]]
        vagas[5].requisitos = [requisitos[1], requisitos[3]]
        db.commit()
        print(f"✓ {len(vagas)} vagas inseridas")

        # Candidatos
        candidatos = [
            models.Candidato(nome="Ana Lima", email="ana.lima@email.com", telefone="(81) 99999-1111", cidade="Recife", estado="PE", data_nascimento=date(1995, 3, 15)),
            models.Candidato(nome="Carlos Souza", email="carlos.souza@email.com", telefone="(11) 99999-2222", cidade="São Paulo", estado="SP", data_nascimento=date(1990, 7, 22)),
            models.Candidato(nome="Beatriz Santos", email="beatriz.santos@email.com", telefone="(31) 99999-3333", cidade="Belo Horizonte", estado="MG", data_nascimento=date(1998, 11, 5)),
        ]
        db.add_all(candidatos)
        db.commit()
        print(f"✓ {len(candidatos)} candidatos inseridos")

        # Candidaturas
        candidaturas = [
            models.Candidatura(candidato_id=1, vaga_id=2, data_candidatura=date(2026, 6, 10), status=models.StatusCandidaturaEnum.em_analise),
            models.Candidatura(candidato_id=2, vaga_id=1, data_candidatura=date(2026, 6, 12), status=models.StatusCandidaturaEnum.pendente),
        ]
        db.add_all(candidaturas)
        db.commit()
        print(f"✓ {len(candidaturas)} candidaturas inseridas")

        print("\nSeed concluído com sucesso!")
    finally:
        db.close()

if __name__ == "__main__":
    seed()
