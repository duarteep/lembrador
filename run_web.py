"""Script para configurar e executar a aplicação web."""
import os
import sys
import subprocess


def verificar_dependencias():
    """Verifica se Flask está instalado."""
    try:
        import flask
        print("✓ Flask já está instalado")
        return True
    except ImportError:
        print("✗ Flask não encontrado")
        return False


def instalar_dependencias():
    """Instala as dependências da aplicação."""
    print("\n📦 Instalando dependências...")
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements-web.txt'])
        print("✓ Dependências instaladas com sucesso!")
        return True
    except subprocess.CalledProcessError:
        print("✗ Erro ao instalar dependências")
        return False


def criar_ambiente_virtual():
    """Cria um ambiente virtual."""
    print("\n🔧 Criando ambiente virtual...")
    try:
        subprocess.check_call([sys.executable, '-m', 'venv', 'venv'])
        print("✓ Ambiente virtual criado!")
        return True
    except Exception as e:
        print(f"✗ Erro ao criar ambiente virtual: {e}")
        return False


def main():
    """Função principal."""
    print("\n" + "="*60)
    print("  AGENDADOR DE CONSULTAS - VERSÃO WEB")
    print("  Setup e Execução")
    print("="*60)
    
    # Banner
    print("\n🌐 Configurando aplicação web...")
    
    # Verificar dependências
    if not verificar_dependencias():
        print("\n⚠️  Dependências não encontradas")
        print("\nOpcões:")
        print("1. Instalar dependências globalmente")
        print("2. Criar ambiente virtual (recomendado)")
        print("3. Sair")
        
        escolha = input("\nEscolha uma opção (1-3): ").strip()
        
        if escolha == '1':
            if not instalar_dependencias():
                print("\n✗ Não foi possível instalar")
                sys.exit(1)
        elif escolha == '2':
            if criar_ambiente_virtual():
                print("\n📌 Ative o ambiente com:")
                if os.name == 'nt':
                    print("   venv\\Scripts\\activate")
                else:
                    print("   source venv/bin/activate")
                print("\nDepois instale as dependências:")
                print("   pip install -r requirements-web.txt")
            sys.exit(0)
        else:
            print("Saindo...")
            sys.exit(0)
    
    # Criar banco de dados se não existir
    print("\n💾 Verificando banco de dados...")
    if not os.path.exists('agendador.db'):
        print("   Banco de dados não encontrado, será criado automaticamente...")
    else:
        print("   Banco de dados já existe")
    
    # Executar aplicação
    print("\n" + "="*60)
    print("  ✓ SISTEMA PRONTO!")
    print("="*60)
    print("\n🌐 Iniciando servidor...")
    print("\n   Acesse em: http://localhost:5000")
    print("   Pressione CTRL+C para parar o servidor")
    print("\n" + "="*60 + "\n")
    
    try:
        from app import app
        app.run(debug=True, host='0.0.0.0', port=5000)
    except ImportError:
        print("✗ Erro ao importar aplicação")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n\n✓ Servidor parado")
        sys.exit(0)


if __name__ == '__main__':
    main()
