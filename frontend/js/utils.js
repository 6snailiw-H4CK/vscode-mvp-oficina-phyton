export function formatarData(data) {
    return new Date(data).toLocaleDateString('pt-BR');
}

export function formatarDataHora(data) {
    return new Date(data).toLocaleString('pt-BR');
}

export function formatarMoeda(valor) {
    return new Intl.NumberFormat('pt-BR', {
        style: 'currency',
        currency: 'BRL',
    }).format(valor || 0);
}

export function mostrarAlerta(mensagem, tipo = 'info') {
    const alertHTML = `
        <div class="alert alert-${tipo} alert-dismissible fade show" role="alert">
            ${mensagem}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        </div>
    `;

    const mainContent = document.querySelector('main');
    if (mainContent) {
        mainContent.insertAdjacentHTML('afterbegin', alertHTML);
    }
}
