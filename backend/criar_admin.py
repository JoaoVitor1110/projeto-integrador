"""
Cria o primeiro usuário admin no banco.
Uso: python criar_admin.py
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.database import SessionLocal, engine, Base
from app import models
from app.auth import hash_senha

Base.metadata.create_all(bind=engine)

def main():
    db = SessionLocal()
    try:
        email = input("Email do admin: ").strip()
        if db.query(models.Usuario).filter(models.Usuario.email == email).first():
            print(f"Usuário '{email}' já existe.")
            return
        nome = input("Nome: ").strip()
        senha = input("Senha: ").strip()
        usuario = models.Usuario(
            nome=nome,
            email=email,
            senha_hash=hash_senha(senha),
            perfil=models.PerfilEnum.admin,
        )
        db.add(usuario)
        db.commit()
        print(f"\n✓ Admin '{email}' criado com sucesso!")
    finally:
        db.close()

if __name__ == "__main__":
    main()
