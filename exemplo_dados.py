"""Script para popular o banco de dados com dados de exemplo."""
from models import Paciente, Profissional, Consulta, StatusConsulta
from database import Database
from datetime import datetime, timedelta


def popular_exemplo():
    """Popula o banco de dados com dados de exemplo."""
    db = Database()
    
    # Pacientes
    pacientes = [
        Paciente("João Silva", "12345678901", "11987654321", "joao.silva@email.com"),
        Paciente("Maria Santos", "98765432100", "11912345678", "maria.santos@email.com"),
        Paciente("Pedro Oliveira", "55544433322", "11987654000", "pedro.oliveira@email.com"),
        Paciente("Ana Costa", "11122233344", "11988776655", None),
    ]
    
    for p in pacientes:
        if not db.obter_paciente_cpf(p.cpf):
            db.adicionar_paciente(p)
            print(f"✓ Paciente '{p.nome}' adicionado")
        else:
            print(f"- Paciente '{p.nome}' já existe")
    
    # Profissionais
    profissionais = [
        Profissional("Dr. Carlos Mendes", "Cardiologia", "123456", "1133334444"),
        Profissional("Dra. Patricia Lima", "Dermatologia", "234567", "1144445555"),
        Profissional("Dr. Roberto Costa", "Ortopedia", "345678", "1155556666"),
        Profissional("Dra. Lucia Barbosa", "Pediatria", "456789", "1166667777"),
    ]
    
    for p in profissionais:
        # Verifica se já existe
        lista = db.listar_profissionais()
        if not any(prof.crm == p.crm for prof in lista):
            db.adicionar_profissional(p)
            print(f"✓ Profissional '{p.nome}' adicionado")
        else:
            print(f"- Profissional '{p.nome}' já existe")
    
    # Consultas
    agora = datetime.now()
    consultas_exemplo = [
        Consulta(
            pacientes[0].id, 
            profissionais[0].id,
            (agora + timedelta(days=2, hours=3)).isoformat(),
            "Consulta de rotina",
            StatusConsulta.AGENDADA
        ),
        Consulta(
            pacientes[1].id,
            profissionais[1].id,
            (agora + timedelta(days=4, hours=5)).isoformat(),
            "Avaliação de acne",
            StatusConsulta.CONFIRMADA
        ),
        Consulta(
            pacientes[2].id,
            profissionais[2].id,
            (agora + timedelta(days=1, hours=2)).isoformat(),
            "Avaliação de joelho",
            StatusConsulta.AGENDADA
        ),
    ]
    
    for consulta in consultas_exemplo:
        if not db.obter_consulta(consulta.id):
            db.adicionar_consulta(consulta)
            print(f"✓ Consulta adicionada para {agora}")
        else:
            print(f"- Consulta já existe")
    
    print("\n✓ Dados de exemplo adicionados com sucesso!")
    print(f"\nResumo:")
    print(f"  Pacientes: {len(db.listar_pacientes())}")
    print(f"  Profissionais: {len(db.listar_profissionais())}")
    print(f"  Consultas: {len(db.listar_consultas())}")


if __name__ == "__main__":
    print("Populando banco de dados com dados de exemplo...\n")
    popular_exemplo()
