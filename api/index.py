"""Aplicação Flask para Agendador de Consultas Web."""
import os
import sys
from flask import Flask, render_template, request, jsonify, redirect, url_for, flash

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT_DIR)

# Debug: print paths
print(f"ROOT_DIR: {ROOT_DIR}")
print(f"sys.path: {sys.path}")
print(f"Current dir: {os.getcwd()}")

from database import Database
from models import Paciente, Profissional, Consulta, StatusConsulta, Notificacao
from utils import (
    validar_cpf, validar_email, validar_telefone, formatar_data_hora,
    formatar_telefone, formatar_cpf, validar_data_hora
)
from datetime import datetime
import json
import math

app = Flask(
    __name__,
    template_folder=os.path.join(ROOT_DIR, 'templates'),
    static_folder=os.path.join(ROOT_DIR, 'static'),
    static_url_path='/static'
)
app.secret_key = 'seu-chave-secreta-aqui'  # Substitua por uma chave segura em produção
db = Database()


# ===== ROTAS PRINCIPAIS =====

@app.route('/')
def index():
    """Página inicial - Dashboard."""
    stats = {
        'total_pacientes': len(db.listar_pacientes()),
        'total_profissionais': len(db.listar_profissionais()),
        'total_consultas': len(db.listar_consultas()),
        'proximas_consultas': len(db.consultas_proximas(dias=7))
    }
    return render_template('index.html', stats=stats)


@app.route('/dashboard')
def dashboard():
    """Dashboard com próximas consultas organizadas por semana."""
    from datetime import datetime, timedelta

    offset = request.args.get('offset', 0, type=int)
    hoje_real = datetime.now().date()
    data_inicio = datetime.combine(hoje_real + timedelta(weeks=offset), datetime.min.time())

    proximas = db.consultas_proximas(dias=7, data_inicio=data_inicio)

    # Organiza consultas por dia da semana
    consultas_por_dia = {}
    hoje = data_inicio.date()

    dias_pt = {
        'Monday': 'Segunda-feira',
        'Tuesday': 'Terça-feira',
        'Wednesday': 'Quarta-feira',
        'Thursday': 'Quinta-feira',
        'Friday': 'Sexta-feira',
        'Saturday': 'Sábado',
        'Sunday': 'Domingo'
    }

    for i in range(7):
        data = hoje + timedelta(days=i)
        dia_en = data.strftime('%A')
        consultas_por_dia[dia_en] = {
            'data': data,
            'data_formatada': data.strftime('%d/%m'),
            'dia_semana': dias_pt.get(dia_en, dia_en),
            'consultas': []
        }
    
    # Preenche com as consultas
    for consulta in proximas:
        paciente = db.obter_paciente(consulta.paciente_id)
        profissional = db.obter_profissional(consulta.profissional_id)
        data_consulta = consulta.data_hora.date() if isinstance(consulta.data_hora, datetime) else consulta.data_hora
        dia_semana = data_consulta.strftime('%A')
        
        esp = profissional.especialidade if profissional else 'N/A'
        esp_curta = f"{esp[:5]}." if len(esp) > 5 else esp
        
        if dia_semana in consultas_por_dia:
            consultas_por_dia[dia_semana]['consultas'].append({
                'id': consulta.id,
                'hora': consulta.data_hora.strftime('%H:%M') if isinstance(consulta.data_hora, datetime) else '14:00',
                'paciente': paciente.nome if paciente else 'N/A',
                'profissional': profissional.nome if profissional else 'N/A',
                'especialidade': esp_curta,
                'motivo': consulta.motivo,
                'status': consulta.status.value
            })
    
    # Ordena os dias por data
    semana = [consultas_por_dia[day] for day in consultas_por_dia.keys()]
    
    stats = {
        'total_pacientes': len(db.listar_pacientes()),
        'total_profissionais': len(db.listar_profissionais()),
        'total_consultas': len(db.listar_consultas()),
        'proximas_consultas': len(proximas)
    }
    
    return render_template('dashboard.html', semana=semana, stats=stats, offset=offset)


# ===== ROTAS DE PACIENTES =====

@app.route('/pacientes')
def listar_pacientes():
    """Lista todos os pacientes."""
    pacientes = db.listar_pacientes()
    pacientes_formatados = []
    
    for p in pacientes:
        pacientes_formatados.append({
            'id': p.id,
            'nome': p.nome,
            'cpf': formatar_cpf(p.cpf),
            'telefone': formatar_telefone(p.telefone),
            'email': p.email or 'N/A'
        })
    
    return render_template('pacientes.html', pacientes=pacientes_formatados)


@app.route('/pacientes/novo', methods=['GET', 'POST'])
def novo_paciente():
    """Formulário para novo paciente."""
    if request.method == 'POST':
        try:
            nome = request.form.get('nome')
            cpf = request.form.get('cpf')
            telefone = request.form.get('telefone')
            email = request.form.get('email')
            
            # Validações
            if not nome or not cpf or not telefone:
                return jsonify({'erro': 'Preencha todos os campos obrigatórios'}), 400
            
            if not validar_cpf(cpf):
                return jsonify({'erro': 'CPF inválido'}), 400
            
            if db.obter_paciente_cpf(cpf):
                return jsonify({'erro': 'CPF já cadastrado'}), 400
            
            if not validar_telefone(telefone):
                return jsonify({'erro': 'Telefone inválido'}), 400
            
            if email and not validar_email(email):
                return jsonify({'erro': 'Email inválido'}), 400
            
            # Criar paciente
            paciente = Paciente(nome, cpf, telefone, email if email else None)
            if db.adicionar_paciente(paciente):
                flash(f'Paciente {nome} adicionado com sucesso!', 'success')
                return redirect(url_for('listar_pacientes'))
            else:
                return jsonify({'erro': 'Erro ao adicionar paciente'}), 500
        
        except Exception as e:
            return jsonify({'erro': str(e)}), 500
    
    return render_template('novo_paciente.html')


@app.route('/pacientes/<paciente_id>')
def detalhe_paciente(paciente_id):
    """Página de detalhes do paciente."""
    paciente = db.obter_paciente(paciente_id)
    if not paciente:
        return "Paciente não encontrado", 404
    
    consultas = db.listar_consultas(paciente_id=paciente_id)
    consultas_formatadas = []
    
    for consulta in consultas:
        profissional = db.obter_profissional(consulta.profissional_id)
        consultas_formatadas.append({
            'id': consulta.id,
            'data_hora': formatar_data_hora(consulta.data_hora),
            'profissional': profissional.nome if profissional else 'N/A',
            'motivo': consulta.motivo,
            'status': consulta.status.value
        })
    
    return render_template('detalhe_paciente.html', 
                         paciente=paciente, 
                         consultas=consultas_formatadas)


# ===== ROTAS DE PROFISSIONAIS =====

@app.route('/profissionais')
def listar_profissionais():
    """Lista todos os profissionais."""
    profissionais = db.listar_profissionais()
    profs_formatados = []
    
    for p in profissionais:
        profs_formatados.append({
            'id': p.id,
            'nome': p.nome,
            'especialidade': p.especialidade,
            'crm': p.crm,
            'telefone': formatar_telefone(p.telefone)
        })
    
    return render_template('profissionais.html', profissionais=profs_formatados)


ESPECIALIDADES = [
    "Cardiologia", "Dermatologia", "Endocrinologia", "Gastroenterologia",
    "Ginecologia", "Neurologia", "Oftalmologia", "Ortopedia", 
    "Otorrinolaringologia", "Pediatria", "Psiquiatria", "Urologia", "Outra"
]

@app.route('/profissionais/novo', methods=['GET', 'POST'])
def novo_profissional():
    """Formulário para novo profissional."""
    if request.method == 'POST':
        try:
            nome = request.form.get('nome')
            especialidade = request.form.get('especialidade')
            crm = request.form.get('crm')
            telefone = request.form.get('telefone')
            
            if not nome or not especialidade or not crm or not telefone:
                return jsonify({'erro': 'Preencha todos os campos'}), 400
            
            if not validar_telefone(telefone):
                return jsonify({'erro': 'Telefone inválido'}), 400
            
            profissional = Profissional(nome, especialidade, crm, telefone)
            if db.adicionar_profissional(profissional):
                flash(f'Profissional {nome} adicionado com sucesso!', 'success')
                return redirect(url_for('listar_profissionais'))
            else:
                return jsonify({'erro': 'CRM já cadastrado'}), 400
        
        except Exception as e:
            return jsonify({'erro': str(e)}), 500
    
    return render_template('novo_profissional.html', especialidades=ESPECIALIDADES)


@app.route('/profissionais/<prof_id>')
def detalhe_profissional(prof_id):
    """Página de detalhes do profissional."""
    profissional = db.obter_profissional(prof_id)
    if not profissional:
        return "Profissional não encontrado", 404
    
    consultas = db.listar_consultas(profissional_id=prof_id)
    consultas_formatadas = []
    
    for consulta in consultas:
        paciente = db.obter_paciente(consulta.paciente_id)
        consultas_formatadas.append({
            'id': consulta.id,
            'data_hora': formatar_data_hora(consulta.data_hora),
            'paciente': paciente.nome if paciente else 'N/A',
            'motivo': consulta.motivo,
            'status': consulta.status.value
        })
    
    return render_template('detalhe_profissional.html',
                         profissional=profissional,
                         consultas=consultas_formatadas)


# ===== ROTAS DE CONSULTAS =====

@app.route('/consultas')
def listar_consultas():
    """Lista todas as consultas com paginação."""
    # Captura os parâmetros da URL
    filtro_status = request.args.get('status')
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 5, type=int)
    
    # 1. Obter a lista base (filtrada ou completa)
    if filtro_status:
        todas_consultas = db.listar_consultas()
        consultas_base = [c for c in todas_consultas if c.status.value == filtro_status]
    else:
        consultas_base = db.listar_consultas()
    
    # 2. Lógica de Paginação
    total_itens = len(consultas_base)
    total_paginas = math.ceil(total_itens / per_page)
    
    # Garante que a página solicitada é válida
    page = max(1, min(page, total_paginas)) if total_paginas > 0 else 1
    
    # Fatiamento da lista (Slicing)
    inicio = (page - 1) * per_page
    fim = inicio + per_page
    consultas_paginadas = consultas_base[inicio:fim]
    
    # 3. Formatação dos dados para o template
    consultas_formatadas = []
    for consulta in consultas_paginadas:
        paciente = db.obter_paciente(consulta.paciente_id)
        profissional = db.obter_profissional(consulta.profissional_id)
        consultas_formatadas.append({
            'id': consulta.id,
            'data_hora': formatar_data_hora(consulta.data_hora),
            'paciente': paciente.nome if paciente else 'N/A',
            'profissional': profissional.nome if profissional else 'N/A',
            'motivo': consulta.motivo,
            'status': consulta.status.value
        })
    
    return render_template('consultas.html', 
                         consultas=consultas_formatadas,
                         page=page,
                         per_page=per_page,
                         total_paginas=total_paginas,
                         total_itens=total_itens,
                         filtro_status=filtro_status)


@app.route('/consultas/nova', methods=['GET', 'POST'])
def nova_consulta():
    """Formulário para nova consulta."""
    if request.method == 'POST':
        try:
            cpf_paciente = request.form.get('cpf_paciente')
            especialidade = request.form.get('especialidade')
            prof_id = request.form.get('profissional_id')
            data_hora_str = request.form.get('data_hora')
            motivo = request.form.get('motivo')
            
            # Validações
            if not all([cpf_paciente, especialidade, prof_id, data_hora_str, motivo]):
                return jsonify({'erro': 'Preencha todos os campos'}), 400
            
            paciente = db.obter_paciente_cpf(cpf_paciente)
            if not paciente:
                return jsonify({'erro': 'Paciente não encontrado'}), 404
            
            profissional = db.obter_profissional(prof_id)
            if not profissional:
                return jsonify({'erro': 'Profissional não encontrado'}), 404
            
            data_hora = validar_data_hora(data_hora_str)
            if not data_hora or data_hora <= datetime.now():
                return jsonify({'erro': 'Data/hora inválida ou no passado'}), 400
            
            if data_hora.minute not in (0, 30) or data_hora.second != 0:
                return jsonify({'erro': 'Consultas devem ser agendadas em blocos de 30 minutos (ex: 14:00, 14:30)'}), 400
            
            # Criar consulta
            consulta = Consulta(paciente.id, profissional.id, data_hora, motivo)
            if db.adicionar_consulta(consulta):
                from datetime import timedelta
                # Agendamentos de Notificações
                def round_to_10_mins(dt):
                    discard = timedelta(minutes=dt.minute % 10, seconds=dt.second, microseconds=dt.microsecond)
                    dt -= discard
                    if discard >= timedelta(minutes=5):
                        dt += timedelta(minutes=10)
                    return dt
                
                agora = datetime.now()
                pref = getattr(paciente, 'preferencia_comunicacao', 'whatsapp')

                # Notificacao 1: 30 min apos agendamento
                t1 = round_to_10_mins(agora + timedelta(minutes=30))
                db.adicionar_notificacao(Notificacao(consulta.id, 'automatica', pref, t1, 'Consulta Agendada', 'Sua consulta foi agendada com sucesso.'))

                # Notificacao 2: 2 dias antes
                t2 = round_to_10_mins(data_hora - timedelta(days=2))
                if t2 > agora:
                    db.adicionar_notificacao(Notificacao(consulta.id, 'automatica', pref, t2, 'Lembrete de Consulta', 'Faltam 2 dias para sua consulta.'))

                # Notificacao 3: 1 dia antes
                t3 = round_to_10_mins(data_hora - timedelta(days=1))
                if t3 > agora:
                    db.adicionar_notificacao(Notificacao(consulta.id, 'automatica', pref, t3, 'Lembrete de Consulta', 'Falta 1 dia para sua consulta.'))

                # Notificacao 4: 2 horas antes
                t4 = round_to_10_mins(data_hora - timedelta(hours=2))
                if t4 > agora:
                    db.adicionar_notificacao(Notificacao(consulta.id, 'automatica', pref, t4, 'Lembrete de Consulta', 'Faltam 2 horas para sua consulta.'))

                flash('Consulta agendada com sucesso!', 'success')
                return redirect(url_for('listar_consultas'))
            else:
                return jsonify({'erro': 'Erro ao agendar consulta'}), 500
        
        except Exception as e:
            return jsonify({'erro': str(e)}), 500
    
    pacientes = db.listar_pacientes()
    profissionais = db.listar_profissionais()
    
    return render_template('nova_consulta.html',
                         pacientes=pacientes,
                         profissionais=profissionais,
                         especialidades=ESPECIALIDADES)


@app.route('/consultas/<consulta_id>')
def detalhe_consulta(consulta_id):
    """Página de detalhes da consulta."""
    consulta = db.obter_consulta(consulta_id)
    if not consulta:
        return "Consulta não encontrada", 404
    
    paciente = db.obter_paciente(consulta.paciente_id)
    profissional = db.obter_profissional(consulta.profissional_id)
    notificacoes = db.listar_notificacoes_por_consulta(consulta_id)
    
    return render_template('detalhe_consulta.html',
                         consulta=consulta,
                         paciente=paciente,
                         profissional=profissional,
                         notificacoes=notificacoes)

@app.route('/consultas/<consulta_id>/confirmacao')
def confirmar_consulta(consulta_id):
    """Página simplificada para confirmar ou cancelar a consulta."""
    consulta = db.obter_consulta(consulta_id)
    if not consulta:
        return "Consulta não encontrada", 404

    paciente = db.obter_paciente(consulta.paciente_id)
    profissional = db.obter_profissional(consulta.profissional_id)

    return render_template('confirmar_consulta.html',
                         consulta=consulta,
                         paciente=paciente,
                         profissional=profissional)

@app.route('/api/notificacoes/<notificacao_id>/cancelar', methods=['POST'])
def api_cancelar_notificacao(notificacao_id):
    """API para cancelar notificação."""
    try:
        db.cancelar_notificacao(notificacao_id)
        return jsonify({'sucesso': True, 'mensagem': 'Notificação cancelada'})
    except Exception as e:
        return jsonify({'erro': str(e)}), 500


@app.route('/api/consultas/<consulta_id>/status', methods=['PUT'])
def atualizar_status(consulta_id):
    """API para atualizar status da consulta."""
    try:
        data = request.get_json()
        novo_status = data.get('status')
        
        if novo_status not in ['agendada', 'confirmada', 'realizada', 'cancelada']:
            return jsonify({'erro': 'Status inválido'}), 400
        
        db.atualizar_status_consulta(consulta_id, novo_status)
        return jsonify({'sucesso': True, 'mensagem': 'Status atualizado'})
    except Exception as e:
        return jsonify({'erro': str(e)}), 500


@app.route('/api/consultas/<consulta_id>/notas', methods=['PUT'])
def atualizar_notas(consulta_id):
    """API para atualizar notas da consulta."""
    try:
        data = request.get_json()
        notas = data.get('notas', '')
        
        db.atualizar_notas_consulta(consulta_id, notas)
        return jsonify({'sucesso': True, 'mensagem': 'Notas atualizadas'})
    except Exception as e:
        return jsonify({'erro': str(e)}), 500


@app.route('/api/consultas/<consulta_id>/deletar', methods=['DELETE'])
def deletar_consulta(consulta_id):
    """API para deletar consulta."""
    try:
        db.deletar_consulta(consulta_id)
        return jsonify({'sucesso': True, 'mensagem': 'Consulta deletada'})
    except Exception as e:
        return jsonify({'erro': str(e)}), 500


# ===== API ENDPOINTS =====

@app.route('/api/profissionais/especialidade/<especialidade>')
def api_profissionais_especialidade(especialidade):
    """API para obter profissionais por especialidade."""
    profissionais = db.listar_profissionais(especialidade=especialidade)
    return jsonify({
        'profissionais': [
            {'id': p.id, 'nome': p.nome, 'crm': p.crm}
            for p in profissionais
        ]
    })


@app.route('/api/paciente/cpf/<cpf>')
def api_obter_paciente(cpf):
    """API para obter paciente pelo CPF."""
    paciente = db.obter_paciente_cpf(cpf)
    if paciente:
        return jsonify({
            'encontrado': True,
            'id': paciente.id,
            'nome': paciente.nome,
            'telefone': paciente.telefone
        })
    return jsonify({'encontrado': False})


@app.route('/api/stats')
def api_stats():
    """API para obter estatísticas."""
    return jsonify({
        'total_pacientes': len(db.listar_pacientes()),
        'total_profissionais': len(db.listar_profissionais()),
        'total_consultas': len(db.listar_consultas()),
        'proximas_consultas': len(db.consultas_proximas(dias=7))
    })


# ===== TRATAMENTO DE ERROS =====

@app.errorhandler(404)
def pagina_nao_encontrada(erro):
    """Página 404."""
    return render_template('404.html'), 404


@app.errorhandler(500)
def erro_interno(erro):
    """Página 500."""
    return render_template('500.html'), 500


# ===== CONTEXT PROCESSORS =====

@app.context_processor
def utility_processor():
    """Funções auxiliares disponíveis em todos os templates."""
    return {
        'formatar_cpf': formatar_cpf,
        'formatar_telefone': formatar_telefone,
        'formatar_data_hora': formatar_data_hora
    }


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
