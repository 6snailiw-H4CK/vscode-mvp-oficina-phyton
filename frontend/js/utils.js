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

// Utilitários reutilizáveis
export function debounce(fn, delay = 300) {
    let timer;
    return (...args) => {
        clearTimeout(timer);
        timer = setTimeout(() => fn.apply(this, args), delay);
    };
}

export function criarStatusBadge(status) {
    const map = {
        ABERTA: 'warning',
        EM_ANDAMENTO: 'info',
        FECHADA: 'success',
        CANCELADA: 'danger',
    };
    const texto = status === 'FECHADA' ? 'Finalizada' : (status || '').replace('_', ' ');
    const classe = map[status] || 'secondary';
    return `<span class="badge bg-${classe}">${texto}</span>`;
}

export function isSameDay(dateA, dateB) {
    const a = new Date(dateA); const b = new Date(dateB);
    return a.getFullYear() === b.getFullYear() && a.getMonth() === b.getMonth() && a.getDate() === b.getDate();
}

export function isSameMonth(dateA, dateB) {
    const a = new Date(dateA); const b = new Date(dateB);
    return a.getFullYear() === b.getFullYear() && a.getMonth() === b.getMonth();
}

export function filtrarOSFinalizadasNoDia(ordens, referencia = new Date()) {
    const ref = new Date(referencia);
    return (ordens || []).filter(o => o.status === 'FECHADA' && o.data_conclusao && isSameDay(o.data_conclusao, ref));
}

export function calcularFaturamentoMes(ordens, referencia = new Date()) {
    return (ordens || [])
        .filter(o => o.status === 'FECHADA' && o.data_conclusao && isSameMonth(o.data_conclusao, referencia))
        .reduce((tot, o) => tot + (Number(o.valor_final) || 0), 0);
}

