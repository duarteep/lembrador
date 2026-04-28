"""Aplicação Flask para Agendador de Consultas Web."""
from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from database import Database
from models import Paciente, Profissional, Consulta, StatusConsulta
from utils import (
    validar_cpf, validar_email, validar_telefone, formatar_data_hora,
    formatar_telefone, formatar_cpf, validar_data_hora
)
from datetime import datetime
import json

app = Flask(__name__)
app.secret_key = 'seu-chave-secreta-aqui'  # Mude isso em produção
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
    """Dashboard com próximas consultas."""
    proximas = db.consultas_proximas(dias=7)
    consultas_formatadas = []
    
    for consulta in proximas:
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
    
    stats = {
        'total_pacientes': len(db.listar_pacientes()),
        'total_profissionais': len(db.listar_profissionais()),
        'total_consultas': len(db.listar_consultas()),
        'proximas_consultas': len(proximas)
    }
    
    return render_template('dashboard.html', consultas=consultas_formatadas, stats=stats)


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
    
    return render_template('novo_profissional.html')


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
    """Lista todas as consultas."""
    filtro_status = request.args.get('status')
    
    if filtro_status:
        # Filtrar por status
        todas_consultas = db.listar_consultas()
        consultas = [c for c in todas_consultas if c.status.value == filtro_status]
    else:
        consultas = db.listar_consultas()
    
    consultas_formatadas = []
    
    for consulta in consultas:
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
    
    return render_template('consultas.html', consultas=consultas_formatadas)


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
            
            # Criar consulta
            consulta = Consulta(paciente.id, profissional.id, data_hora, motivo)
            if db.adicionar_consulta(consulta):
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
                         profissionais=profissionais)


@app.route('/consultas/<consulta_id>')
def detalhe_consulta(consulta_id):
    """Página de detalhes da consulta."""
    consulta = db.obter_consulta(consulta_id)
    if not consulta:
        return "Consulta não encontrada", 404
    
    paciente = db.obter_paciente(consulta.paciente_id)
    profissional = db.obter_profissional(consulta.profissional_id)
    
    return render_template('detalhe_consulta.html',
                         consulta=consulta,
                         paciente=paciente,
                         profissional=profissional)


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
