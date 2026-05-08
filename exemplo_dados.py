"""Script para popular o banco de dados com dados de exemplo."""
from models import Paciente, Profissional, Consulta, StatusConsulta
from database import Database
from datetime import datetime, timedelta
import random


def popular_exemplo():
    """Popula o banco de dados com dados de exemplo no PostgreSQL."""
    db = Database()
    db.criar_tabelas()

    # ── Pacientes ─────────────────────────────────────────────────────────────
    pacientes_data = [
        ("João Silva",          "12345678901", "11987654321", "joao.silva@email.com"),
        ("Maria Santos",        "98765432100", "11912345678", "maria.santos@email.com"),
        ("Pedro Oliveira",      "55544433322", "11987654000", "pedro.oliveira@email.com"),
        ("Ana Costa",           "11122233344", "11988776655", None),
        ("Lucas Ferreira",      "22233344455", "11991234567", "lucas.ferreira@email.com"),
        ("Fernanda Rocha",      "33344455566", "11999887766", "fernanda.rocha@email.com"),
        ("Carlos Souza",        "44455566677", "11933445566", None),
        ("Beatriz Lima",        "55566677788", "11944556677", "beatriz.lima@email.com"),
        ("Rafael Alves",        "66677788899", "11955667788", "rafael.alves@email.com"),
        ("Juliana Mendes",      "77788899900", "11966778899", "juliana.mendes@email.com"),
        ("Eduardo Barbosa",     "88899900011", "11977889900", None),
        ("Camila Pereira",      "99900011122", "11988990011", "camila.pereira@email.com"),
        ("Thiago Carvalho",     "10011122233", "11999001122", "thiago.carvalho@email.com"),
        ("Larissa Nunes",       "11122233345", "11900112233", None),
        ("Gustavo Ribeiro",     "12233344456", "11911223344", "gustavo.ribeiro@email.com"),
        ("Patricia Gomes",      "23344455567", "11922334455", "patricia.gomes@email.com"),
        ("Rodrigo Martins",     "34455566678", "11933445567", None),
        ("Amanda Freitas",      "45566677789", "11944556678", "amanda.freitas@email.com"),
        ("Felipe Castro",       "56677788890", "11955667789", "felipe.castro@email.com"),
        ("Vanessa Teixeira",    "67788899901", "11966778890", "vanessa.teixeira@email.com"),
    ]

    pacientes = []
    for nome, cpf, telefone, email in pacientes_data:
        existente = db.obter_paciente_cpf(cpf)
        if existente:
            print(f"- Paciente '{nome}' já existe")
            pacientes.append(existente)
        else:
            p = Paciente(nome, cpf, telefone, email)
            db.adicionar_paciente(p)
            pacientes.append(p)
            print(f"✓ Paciente '{nome}' adicionado")

    # ── Profissionais ─────────────────────────────────────────────────────────
    profissionais_data = [
        ("Dr. Carlos Mendes",      "Cardiologia",      "123456", "1133334444"),
        ("Dra. Patricia Lima",     "Dermatologia",     "234567", "1144445555"),
        ("Dr. Roberto Costa",      "Ortopedia",        "345678", "1155556666"),
        ("Dra. Lucia Barbosa",     "Pediatria",        "456789", "1166667777"),
        ("Dr. André Figueiredo",   "Neurologia",       "567890", "1177778888"),
        ("Dra. Renata Azevedo",    "Ginecologia",      "678901", "1188889999"),
        ("Dr. Marcelo Duarte",     "Oftalmologia",     "789012", "1199990000"),
        ("Dra. Silvia Monteiro",   "Endocrinologia",   "890123", "1100001111"),
        ("Dr. Henrique Vieira",    "Urologia",         "901234", "1111112222"),
        ("Dra. Cristina Campos",   "Psiquiatria",      "012345", "1122223333"),
        ("Dr. Bruno Pinto",        "Gastroenterologia","112233", "1133334445"),
        ("Dra. Mariana Leal",      "Reumatologia",     "223344", "1144445556"),
    ]

    profissionais = []
    crms_existentes = {prof.crm for prof in db.listar_profissionais()}
    for nome, especialidade, crm, telefone in profissionais_data:
        if crm in crms_existentes:
            print(f"- Profissional '{nome}' já existe")
            match = next(p for p in db.listar_profissionais() if p.crm == crm)
            profissionais.append(match)
        else:
            p = Profissional(nome, especialidade, crm, telefone)
            db.adicionar_profissional(p)
            profissionais.append(p)
            print(f"✓ Profissional '{nome}' adicionado")

    # ── Consultas ─────────────────────────────────────────────────────────────
    motivos_por_especialidade = {
        "Cardiologia":        ["Dor no peito", "Controle de hipertensão", "Consulta de rotina cardíaca", "Palpitações"],
        "Dermatologia":       ["Avaliação de acne", "Mancha na pele", "Queda de cabelo", "Consulta de rotina"],
        "Ortopedia":          ["Dor no joelho", "Fratura em acompanhamento", "Dor lombar", "Lesão no ombro"],
        "Pediatria":          ["Consulta de rotina", "Febre persistente", "Acompanhamento de crescimento", "Vacinação"],
        "Neurologia":         ["Enxaqueca frequente", "Tontura", "Formigamento nas mãos", "Avaliação neurológica"],
        "Ginecologia":        ["Consulta de rotina", "Exame preventivo", "Irregularidade menstrual", "Pré-natal"],
        "Oftalmologia":       ["Revisão de óculos", "Visão embaçada", "Consulta de rotina", "Olho seco"],
        "Endocrinologia":     ["Controle de diabetes", "Hipotireoidismo", "Consulta de rotina", "Ganho de peso"],
        "Urologia":           ["Infecção urinária recorrente", "Consulta de rotina", "Dor ao urinar"],
        "Psiquiatria":        ["Ansiedade", "Depressão", "Insônia", "Acompanhamento de medicação"],
        "Gastroenterologia":  ["Refluxo", "Dor abdominal", "Consulta de rotina", "Náuseas frequentes"],
        "Reumatologia":       ["Dor nas articulações", "Suspeita de artrite", "Acompanhamento de lúpus", "Fadiga crônica"],
    }

    status_pesos = [
        (StatusConsulta.AGENDADA,   0.40),
        (StatusConsulta.CONFIRMADA, 0.30),
        (StatusConsulta.REALIZADA,  0.20),
        (StatusConsulta.CANCELADA,  0.10),
    ]
    status_opcoes, status_pesos_vals = zip(*status_pesos)

    agora = datetime.now()
    consultas_adicionadas = 0
    consultas_existentes = db.listar_consultas()

    # Gera ~40 consultas distribuídas nos próximos 14 dias e últimos 7 dias
    slots = []
    for dias_offset in range(-7, 15):
        for hora in [8, 9, 10, 11, 14, 15, 16, 17]:
            slots.append(agora.replace(hour=hora, minute=0, second=0, microsecond=0)
                         + timedelta(days=dias_offset))

    random.shuffle(slots)
    slots_usados = set()

    for slot in slots[:50]:
        paciente    = random.choice(pacientes)
        profissional = random.choice(profissionais)

        chave = (profissional.id, slot.isoformat())
        if chave in slots_usados:
            continue
        slots_usados.add(chave)

        status = random.choices(status_opcoes, weights=status_pesos_vals, k=1)[0]
        # Consultas passadas não ficam como "agendada"
        if slot < agora and status == StatusConsulta.AGENDADA:
            status = StatusConsulta.REALIZADA

        motivos = motivos_por_especialidade.get(profissional.especialidade, ["Consulta de rotina"])
        motivo  = random.choice(motivos)

        ja_existe = any(
            c.paciente_id     == paciente.id and
            c.profissional_id == profissional.id and
            str(c.data_hora)  == slot.isoformat() and
            c.motivo          == motivo
            for c in consultas_existentes
        )

        if not ja_existe:
            consulta = Consulta(paciente.id, profissional.id, slot.isoformat(), motivo, status)
            db.adicionar_consulta(consulta)
            consultas_adicionadas += 1

    print(f"✓ {consultas_adicionadas} consultas adicionadas")

    # ── Resumo ────────────────────────────────────────────────────────────────
    print("\n✓ Dados de exemplo adicionados com sucesso!")
    print(f"\nResumo:")
    print(f"  Pacientes:     {len(db.listar_pacientes())}")
    print(f"  Profissionais: {len(db.listar_profissionais())}")
    print(f"  Consultas:     {len(db.listar_consultas())}")


if __name__ == "__main__":
    print("Populando banco de dados com dados de exemplo...\n")
    popular_exemplo()
