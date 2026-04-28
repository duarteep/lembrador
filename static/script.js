// Remover alertas automaticamente após 5 segundos
document.addEventListener('DOMContentLoaded', function() {
    const alerts = document.querySelectorAll('.alert');
    
    alerts.forEach(alert => {
        const closeBtn = alert.querySelector('.close-alert');
        const removeAlert = () => {
            alert.style.animation = 'slideOut 0.3s ease';
            setTimeout(() => alert.remove(), 300);
        };

        // Remover ao clicar no botão X
        if (closeBtn) {
            closeBtn.addEventListener('click', removeAlert);
        }

        // Remover automaticamente após 5 segundos
        setTimeout(removeAlert, 5000);
    });
});

// Animação slide out
const style = document.createElement('style');
style.textContent = `
    @keyframes slideOut {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(-100%);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);

// Validar formulário antes de enviar
document.addEventListener('submit', function(e) {
    const form = e.target;
    const inputs = form.querySelectorAll('[required]');
    let valido = true;

    inputs.forEach(input => {
        if (!input.value.trim()) {
            input.style.borderColor = '#e74c3c';
            valido = false;
        } else {
            input.style.borderColor = '';
        }
    });

    if (!valido) {
        e.preventDefault();
        alert('Por favor, preencha todos os campos obrigatórios');
    }
}, true);

// Permite apenas números em campos de CPF
document.querySelectorAll('input[name="cpf"], input[name="cpf_paciente"]').forEach(input => {
    input.addEventListener('input', function() {
        this.value = this.value.replace(/[^0-9]/g, '');
    });
});

// Formatar telefone
document.querySelectorAll('input[type="tel"]').forEach(input => {
    input.addEventListener('input', function() {
        let valor = this.value.replace(/[^0-9]/g, '');
        if (valor.length > 11) {
            valor = valor.slice(0, 11);
        }
        this.value = valor;
    });
});
