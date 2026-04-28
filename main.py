"""Aplicação de Agendador de Consultas - Interface Principal."""
from database import Database
from models import Paciente, Profissional, Consulta, StatusConsulta
from utils import (
    validar_cpf, validar_email, validar_telefone, formatar_data_hora,
    formatar_telefone, formatar_cpf, validar_data_hora, limpar_tela,
    exibir_menu, entrada_segura
)
from datetime import datetime


class AgendadorConsultas:
    """Classe principal da aplicação de agendamento."""
    
    def __init__(self):
        self.db = Database()
    
    def menu_principal(self):
        """Exibe o menu principal da aplicação."""
        while True:
            limpar_tela()
            print("\n" + "="*50)
            print("  AGENDADOR DE CONSULTAS")
            print("="*50)
            
            opcoes = [
                "Gerenciar Pacientes",
                "Gerenciar Profissionais",
                "Agendar Consulta",
                "Consultas Próximas",
                "Gerenciar Consultas Existentes",
                "Sair"
            ]
            
            escolha = exibir_menu(opcoes)
            
            if escolha == 1:
                self.menu_pacientes()
            elif escolha == 2:
                self.menu_profissionais()
            elif escolha == 3:
                self.agendar_consulta()
            elif escolha == 4:
                self.listar_proximas_consultas()
            elif escolha == 5:
                self.gerenciar_consultas()
            elif escolha == 6:
                print("\nAté logo!")
                break
    
    # ===== GERENCIAMENTO DE PACIENTES =====
    
    def menu_pacientes(self):
        """Menu de gerenciamento de pacientes."""
        while True:
            limpar_tela()
            print("\n" + "="*50)
            print("  GERENCIAR PACIENTES")
            print("="*50)
            
            opcoes = [
                "Adicionar Paciente",
                "Listar Pacientes",
                "Consultar Paciente por CPF",
                "Voltar"
            ]
            
            escolha = exibir_menu(opcoes)
            
            if escolha == 1:
                self.adicionar_paciente()
            elif escolha == 2:
                self.listar_pacientes()
            elif escolha == 3:
                self.consultar_paciente_cpf()
            elif escolha == 4:
                break
    
    def adicionar_paciente(self):
        """Adiciona um novo paciente."""
        limpar_tela()
        print("\n" + "="*50)
        print("  ADICIONAR PACIENTE")
        print("="*50)
        
        nome = entrada_segura("Nome completo")
        
        while True:
            cpf = entrada_segura("CPF (apenas números)")
            if validar_cpf(cpf):
                # Verifica se CPF já existe
                if self.db.obter_paciente_cpf(cpf):
                    print("CPF já cadastrado!")
                    continue
                break
            print("CPF inválido!")
        
        while True:
            telefone = entrada_segura("Telefone")
            if validar_telefone(telefone):
                break
            print("Telefone inválido!")
        
        email = entrada_segura("Email (opcional)")
        if email:
            while not validar_email(email):
                email = entrada_segura("Email (formato inválido, tente novamente)")
        else:
            email = None
        
        paciente = Paciente(nome, cpf, telefone, email)
        
        if self.db.adicionar_paciente(paciente):
            print(f"\n✓ Paciente '{nome}' cadastrado com sucesso!")
        else:
            print("\n✗ Erro ao cadastrar paciente!")
        
        input("\nPressione ENTER para continuar...")
    
    def listar_pacientes(self):
        """Lista todos os pacientes."""
        limpar_tela()
        print("\n" + "="*50)
        print("  LISTA DE PACIENTES")
        print("="*50)
        
        pacientes = self.db.listar_pacientes()
        
        if not pacientes:
            print("\nNenhum paciente cadastrado.")
        else:
            print(f"\nTotal de pacientes: {len(pacientes)}\n")
            for i, paciente in enumerate(pacientes, 1):
                print(f"{i}. {paciente.nome}")
                print(f"   CPF: {formatar_cpf(paciente.cpf)}")
                print(f"   Telefone: {formatar_telefone(paciente.telefone)}")
                if paciente.email:
                    print(f"   Email: {paciente.email}")
                print()
        
        input("Pressione ENTER para continuar...")
    
    def consultar_paciente_cpf(self):
        """Consulta um paciente pelo CPF."""
        limpar_tela()
        print("\n" + "="*50)
        print("  CONSULTAR PACIENTE")
        print("="*50)
        
        cpf = entrada_segura("\nCPF (apenas números)", validador=validar_cpf)
        paciente = self.db.obter_paciente_cpf(cpf)
        
        if paciente:
            print(f"\nPaciente encontrado:")
            print(f"Nome: {paciente.nome}")
            print(f"CPF: {formatar_cpf(paciente.cpf)}")
            print(f"Telefone: {formatar_telefone(paciente.telefone)}")
            if paciente.email:
                print(f"Email: {paciente.email}")
            
            # Mostra consultas do paciente
            consultas = self.db.listar_consultas(paciente_id=paciente.id)
            if consultas:
                print(f"\nConsultas agendadas: {len(consultas)}")
                for consulta in consultas:
                    profissional = self.db.obter_profissional(consulta.profissional_id)
                    print(f"  - {formatar_data_hora(consulta.data_hora)} com {profissional.nome} ({consulta.status.value})")
        else:
            print("\n✗ Paciente não encontrado!")
        
        input("\nPressione ENTER para continuar...")
    
    # ===== GERENCIAMENTO DE PROFISSIONAIS =====
    
    def menu_profissionais(self):
        """Menu de gerenciamento de profissionais."""
        while True:
            limpar_tela()
            print("\n" + "="*50)
            print("  GERENCIAR PROFISSIONAIS")
            print("="*50)
            
            opcoes = [
                "Adicionar Profissional",
                "Listar Profissionais",
                "Listar por Especialidade",
                "Voltar"
            ]
            
            escolha = exibir_menu(opcoes)
            
            if escolha == 1:
                self.adicionar_profissional()
            elif escolha == 2:
                self.listar_profissionais()
            elif escolha == 3:
                self.listar_por_especialidade()
            elif escolha == 4:
                break
    
    def adicionar_profissional(self):
        """Adiciona um novo profissional."""
        limpar_tela()
        print("\n" + "="*50)
        print("  ADICIONAR PROFISSIONAL")
        print("="*50)
        
        nome = entrada_segura("\nNome completo")
        especialidade = entrada_segura("Especialidade (ex: Cardiologista, Dentista)")
        crm = entrada_segura("CRM/CREA")
        
        while True:
            telefone = entrada_segura("Telefone")
            if validar_telefone(telefone):
                break
            print("Telefone inválido!")
        
        profissional = Profissional(nome, especialidade, crm, telefone)
        
        if self.db.adicionar_profissional(profissional):
            print(f"\n✓ Profissional '{nome}' cadastrado com sucesso!")
        else:
            print("\n✗ Erro ao cadastrar profissional!")
        
        input("\nPressione ENTER para continuar...")
    
    def listar_profissionais(self):
        """Lista todos os profissionais."""
        limpar_tela()
        print("\n" + "="*50)
        print("  LISTA DE PROFISSIONAIS")
        print("="*50)
        
        profissionais = self.db.listar_profissionais()
        
        if not profissionais:
            print("\nNenhum profissional cadastrado.")
        else:
            print(f"\nTotal de profissionais: {len(profissionais)}\n")
            for i, prof in enumerate(profissionais, 1):
                print(f"{i}. {prof.nome}")
                print(f"   Especialidade: {prof.especialidade}")
                print(f"   CRM: {prof.crm}")
                print(f"   Telefone: {formatar_telefone(prof.telefone)}")
                print()
        
        input("Pressione ENTER para continuar...")
    
    def listar_por_especialidade(self):
        """Lista profissionais por especialidade."""
        limpar_tela()
        print("\n" + "="*50)
        print("  PROFISSIONAIS POR ESPECIALIDADE")
        print("="*50)
        
        especialidade = entrada_segura("\nEspecialidade")
        profissionais = self.db.listar_profissionais(especialidade=especialidade)
        
        if not profissionais:
            print(f"\nNenhum profissional de '{especialidade}' cadastrado.")
        else:
            print(f"\nProfissionais de {especialidade}: {len(profissionais)}\n")
            for i, prof in enumerate(profissionais, 1):
                print(f"{i}. {prof.nome}")
                print(f"   CRM: {prof.crm}")
                print(f"   Telefone: {formatar_telefone(prof.telefone)}")
                print()
        
        input("Pressione ENTER para continuar...")
    
    # ===== AGENDAMENTO DE CONSULTAS =====
    
    def agendar_consulta(self):
        """Agenda uma nova consulta."""
        limpar_tela()
        print("\n" + "="*50)
        print("  AGENDAR CONSULTA")
        print("="*50)
        
        # Seleciona paciente
        print("\n--- Selecionar Paciente ---")
        cpf_paciente = entrada_segura("\nCPF do paciente", validador=validar_cpf)
        paciente = self.db.obter_paciente_cpf(cpf_paciente)
        
        if not paciente:
            print("\n✗ Paciente não encontrado!")
            input("Pressione ENTER para continuar...")
            return
        
        print(f"✓ Paciente selecionado: {paciente.nome}")
        
        # Seleciona profissional
        print("\n--- Selecionar Profissional ---")
        especialidade = entrada_segura("Especialidade desejada")
        profissionais = self.db.listar_profissionais(especialidade=especialidade)
        
        if not profissionais:
            print(f"\n✗ Nenhum profissional de '{especialidade}' disponível!")
            input("Pressione ENTER para continuar...")
            return
        
        print(f"\nProfissionais disponíveis:")
        for i, prof in enumerate(profissionais, 1):
            print(f"{i}. {prof.nome} - CRM: {prof.crm}")
        
        escolha = entrada_segura("\nEscolha um profissional", tipo=int)
        if not (1 <= escolha <= len(profissionais)):
            print("Opção inválida!")
            input("Pressione ENTER para continuar...")
            return
        
        profissional = profissionais[escolha - 1]
        print(f"✓ Profissional selecionado: {profissional.nome}")
        
        # Data e hora
        print("\n--- Data e Hora da Consulta ---")
        print("Formatos aceitos: DD/MM/YYYY HH:MM ou DD/MM/YYYY")
        while True:
            data_str = entrada_segura("Data e hora (ex: 25/12/2024 14:30)")
            data_hora = validar_data_hora(data_str)
            if data_hora and data_hora > datetime.now():
                break
            print("Data/hora inválida ou no passado!")
        
        # Motivo
        motivo = entrada_segura("Motivo da consulta")
        
        # Cria e agenda a consulta
        consulta = Consulta(paciente.id, profissional.id, data_hora, motivo)
        
        if self.db.adicionar_consulta(consulta):
            print(f"\n✓ Consulta agendada com sucesso!")
            print(f"  Paciente: {paciente.nome}")
            print(f"  Profissional: {profissional.nome}")
            print(f"  Data/Hora: {formatar_data_hora(data_hora)}")
            print(f"  Motivo: {motivo}")
        else:
            print("\n✗ Erro ao agendar consulta!")
        
        input("\nPressione ENTER para continuar...")
    
    def listar_proximas_consultas(self):
        """Lista as próximas consultas."""
        limpar_tela()
        print("\n" + "="*50)
        print("  PRÓXIMAS CONSULTAS (7 dias)")
        print("="*50)
        
        consultas = self.db.consultas_proximas(dias=7)
        
        if not consultas:
            print("\nNenhuma consulta agendada para os próximos 7 dias.")
        else:
            print(f"\nTotal de consultas: {len(consultas)}\n")
            for i, consulta in enumerate(consultas, 1):
                paciente = self.db.obter_paciente(consulta.paciente_id)
                profissional = self.db.obter_profissional(consulta.profissional_id)
                
                print(f"{i}. {formatar_data_hora(consulta.data_hora)}")
                print(f"   Paciente: {paciente.nome}")
                print(f"   Profissional: {profissional.nome} ({profissional.especialidade})")
                print(f"   Motivo: {consulta.motivo}")
                print(f"   Status: {consulta.status.value}")
                print()
        
        input("Pressione ENTER para continuar...")
    
    def gerenciar_consultas(self):
        """Menu para gerenciar consultas existentes."""
        while True:
            limpar_tela()
            print("\n" + "="*50)
            print("  GERENCIAR CONSULTAS")
            print("="*50)
            
            opcoes = [
                "Listar Todas as Consultas",
                "Listar Consultas de um Paciente",
                "Listar Consultas de um Profissional",
                "Atualizar Status de Consulta",
                "Cancelar Consulta",
                "Adicionar Notas à Consulta",
                "Voltar"
            ]
            
            escolha = exibir_menu(opcoes)
            
            if escolha == 1:
                self.listar_todas_consultas()
            elif escolha == 2:
                self.listar_consultas_paciente()
            elif escolha == 3:
                self.listar_consultas_profissional()
            elif escolha == 4:
                self.atualizar_status_consulta()
            elif escolha == 5:
                self.cancelar_consulta()
            elif escolha == 6:
                self.adicionar_notas_consulta()
            elif escolha == 7:
                break
    
    def listar_todas_consultas(self):
        """Lista todas as consultas."""
        limpar_tela()
        print("\n" + "="*50)
        print("  TODAS AS CONSULTAS")
        print("="*50)
        
        consultas = self.db.listar_consultas()
        
        if not consultas:
            print("\nNenhuma consulta cadastrada.")
        else:
            print(f"\nTotal de consultas: {len(consultas)}\n")
            for i, consulta in enumerate(consultas, 1):
                paciente = self.db.obter_paciente(consulta.paciente_id)
                profissional = self.db.obter_profissional(consulta.profissional_id)
                
                print(f"{i}. {formatar_data_hora(consulta.data_hora)}")
                print(f"   Paciente: {paciente.nome}")
                print(f"   Profissional: {profissional.nome}")
                print(f"   Motivo: {consulta.motivo}")
                print(f"   Status: {consulta.status.value}")
                print(f"   ID: {consulta.id}")
                print()
        
        input("Pressione ENTER para continuar...")
    
    def listar_consultas_paciente(self):
        """Lista consultas de um paciente."""
        limpar_tela()
        print("\n" + "="*50)
        print("  CONSULTAS DE UM PACIENTE")
        print("="*50)
        
        cpf = entrada_segura("\nCPF do paciente", validador=validar_cpf)
        paciente = self.db.obter_paciente_cpf(cpf)
        
        if not paciente:
            print("\n✗ Paciente não encontrado!")
            input("Pressione ENTER para continuar...")
            return
        
        consultas = self.db.listar_consultas(paciente_id=paciente.id)
        
        if not consultas:
            print(f"\nNenhuma consulta para {paciente.nome}.")
        else:
            print(f"\nConsultas de {paciente.nome}: {len(consultas)}\n")
            for i, consulta in enumerate(consultas, 1):
                profissional = self.db.obter_profissional(consulta.profissional_id)
                print(f"{i}. {formatar_data_hora(consulta.data_hora)}")
                print(f"   Profissional: {profissional.nome} ({profissional.especialidade})")
                print(f"   Motivo: {consulta.motivo}")
                print(f"   Status: {consulta.status.value}")
                print()
        
        input("Pressione ENTER para continuar...")
    
    def listar_consultas_profissional(self):
        """Lista consultas de um profissional."""
        limpar_tela()
        print("\n" + "="*50)
        print("  CONSULTAS DE UM PROFISSIONAL")
        print("="*50)
        
        crm = entrada_segura("\nCRM do profissional")
        profissionais = [p for p in self.db.listar_profissionais() if p.crm == crm]
        
        if not profissionais:
            print("\n✗ Profissional não encontrado!")
            input("Pressione ENTER para continuar...")
            return
        
        profissional = profissionais[0]
        consultas = self.db.listar_consultas(profissional_id=profissional.id)
        
        if not consultas:
            print(f"\nNenhuma consulta para {profissional.nome}.")
        else:
            print(f"\nConsultas de {profissional.nome}: {len(consultas)}\n")
            for i, consulta in enumerate(consultas, 1):
                paciente = self.db.obter_paciente(consulta.paciente_id)
                print(f"{i}. {formatar_data_hora(consulta.data_hora)}")
                print(f"   Paciente: {paciente.nome}")
                print(f"   Motivo: {consulta.motivo}")
                print(f"   Status: {consulta.status.value}")
                print()
        
        input("Pressione ENTER para continuar...")
    
    def atualizar_status_consulta(self):
        """Atualiza o status de uma consulta."""
        limpar_tela()
        print("\n" + "="*50)
        print("  ATUALIZAR STATUS DE CONSULTA")
        print("="*50)
        
        consulta_id = entrada_segura("\nID da consulta")
        consulta = self.db.obter_consulta(consulta_id)
        
        if not consulta:
            print("\n✗ Consulta não encontrada!")
            input("Pressione ENTER para continuar...")
            return
        
        paciente = self.db.obter_paciente(consulta.paciente_id)
        profissional = self.db.obter_profissional(consulta.profissional_id)
        
        print(f"\nConsulta encontrada:")
        print(f"Paciente: {paciente.nome}")
        print(f"Profissional: {profissional.nome}")
        print(f"Data/Hora: {formatar_data_hora(consulta.data_hora)}")
        print(f"Status atual: {consulta.status.value}")
        
        opcoes = ["Agendada", "Confirmada", "Realizada", "Cancelada"]
        print("\nNovos status disponíveis:")
        for i, status in enumerate(opcoes, 1):
            print(f"{i}. {status}")
        
        escolha = entrada_segura("Escolha o novo status", tipo=int)
        if not (1 <= escolha <= len(opcoes)):
            print("Opção inválida!")
            input("Pressione ENTER para continuar...")
            return
        
        novo_status = opcoes[escolha - 1].lower()
        self.db.atualizar_status_consulta(consulta_id, novo_status)
        print(f"\n✓ Status atualizado para '{novo_status}'!")
        
        input("Pressione ENTER para continuar...")
    
    def cancelar_consulta(self):
        """Cancela uma consulta."""
        limpar_tela()
        print("\n" + "="*50)
        print("  CANCELAR CONSULTA")
        print("="*50)
        
        consulta_id = entrada_segura("\nID da consulta a cancelar")
        consulta = self.db.obter_consulta(consulta_id)
        
        if not consulta:
            print("\n✗ Consulta não encontrada!")
            input("Pressione ENTER para continuar...")
            return
        
        if consulta.status.value == "cancelada":
            print("\n✗ Esta consulta já foi cancelada!")
            input("Pressione ENTER para continuar...")
            return
        
        paciente = self.db.obter_paciente(consulta.paciente_id)
        profissional = self.db.obter_profissional(consulta.profissional_id)
        
        print(f"\nConsulta a cancelar:")
        print(f"Paciente: {paciente.nome}")
        print(f"Profissional: {profissional.nome}")
        print(f"Data/Hora: {formatar_data_hora(consulta.data_hora)}")
        
        confirmacao = input("\nDeseja realmente cancelar? (S/N): ").upper()
        if confirmacao == "S":
            self.db.atualizar_status_consulta(consulta_id, "cancelada")
            print("\n✓ Consulta cancelada com sucesso!")
        else:
            print("\n✗ Operação cancelada!")
        
        input("Pressione ENTER para continuar...")
    
    def adicionar_notas_consulta(self):
        """Adiciona notas a uma consulta."""
        limpar_tela()
        print("\n" + "="*50)
        print("  ADICIONAR NOTAS À CONSULTA")
        print("="*50)
        
        consulta_id = entrada_segura("\nID da consulta")
        consulta = self.db.obter_consulta(consulta_id)
        
        if not consulta:
            print("\n✗ Consulta não encontrada!")
            input("Pressione ENTER para continuar...")
            return
        
        print(f"\nNotas atuais: {consulta.notas if consulta.notas else 'Nenhuma'}")
        notas = entrada_segura("Novas notas (ou deixe em branco para manter)")
        
        if notas:
            self.db.atualizar_notas_consulta(consulta_id, notas)
            print("\n✓ Notas atualizadas!")
        else:
            print("\n✓ Notas mantidas!")
        
        input("Pressione ENTER para continuar...")


def main():
    """Função principal."""
    app = AgendadorConsultas()
    app.menu_principal()


if __name__ == "__main__":
    main()
