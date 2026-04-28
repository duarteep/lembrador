"""Script para limpar todos os dados do banco de dados."""
import os
from database import Database


def limpar_banco():
    """Remove o banco de dados e cria um novo vazio."""
    db_path = "agendador.db"
    
    confirmacao = input("\n⚠️  AVISO: Esta ação é irreversível e deletará todos os dados!\n")
    confirmacao = input("Digite 'SIM' para confirmar: ").upper()
    
    if confirmacao == "SIM":
        try:
            if os.path.exists(db_path):
                os.remove(db_path)
                print(f"✓ Arquivo '{db_path}' removido")
            
            # Criar um novo banco de dados vazio
            db = Database()
            print("✓ Novo banco de dados criado (vazio)")
            print("\n✓ Banco de dados limpo com sucesso!")
        except Exception as e:
            print(f"✗ Erro ao limpar banco de dados: {e}")
    else:
        print("\n✗ Operação cancelada")


if __name__ == "__main__":
    limpar_banco()
