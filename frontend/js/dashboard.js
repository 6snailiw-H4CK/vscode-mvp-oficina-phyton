import {
    getClientes,
    getOrdensServico,
    getRelatorioEstoque,
} from './api.module.js';
import { formatarMoeda, mostrarAlerta, filtrarOSFinalizadasNoDia, calcularFaturamentoMes } from './utils.js';

const API_HEALTH_URL = new URL('/health', window.location.href).href;

function obterInicioDoMes() {
    const hoje = new Date();
    return new Date(hoje.getFullYear(), hoje.getMonth(), 1, 0, 0, 0, 0);
}


function criarLinhaCliente(cliente) {
    return `
        <div class="list-group-item list-group-item-action d-flex justify-content-between align-items-start">
            <div class="ms-2 me-auto">
                <div class="fw-bold">${cliente.nome}</div>
                <small class="text-muted">${cliente.email || 'Sem e-mail'} • ${cliente.telefone || 'Sem telefone'}</small>
            </div>
            <span class="badge bg-primary rounded-pill">ID ${cliente.id}</span>
        </div>
    `;
}

export async function carregarDashboard() {
    const statusCard = document.getElementById('dashboard-api-status');
    const osAbertas = document.getElementById('dashboard-open-os');
    const faturamento = document.getElementById('dashboard-month-revenue');
    const estoqueBaixo = document.getElementById('dashboard-low-stock');
    const servicosHoje = document.getElementById('dashboard-services-today');
    const clientesRecentes = document.getElementById('dashboard-clients-list');

        try {
        const [healthResponse, ordensAbertasData, ordensFechadasData, clientesData, estoqueData] =
            await Promise.all([
                fetch(API_HEALTH_URL),
                getOrdensServico(0, 1000, 'ABERTA'),
                getOrdensServico(0, 1000, 'FECHADA'),
                getClientes(0, 5),
                getRelatorioEstoque(),
            ]);


        statusCard.innerHTML = healthResponse.ok
            ? '<span class="badge bg-success">✓ API conectada</span>'
            : '<span class="badge bg-danger">✗ API indisponível</span>';

                osAbertas.textContent = ordensAbertasData.length;
        estoqueBaixo.textContent = estoqueData.produtos_com_estoque_baixo || 0;

        // Ordens finalizadas hoje (status FECHADA com data_conclusao hoje)
        const finalizadasHoje = filtrarOSFinalizadasNoDia(ordensFechadasData, new Date());
        servicosHoje.textContent = finalizadasHoje.length;

        // Faturamento do mês: soma de valor_final das OS FECHADA concluídas no mês corrente
        const faturamentoTotal = calcularFaturamentoMes(ordensFechadasData, new Date());
        faturamento.textContent = formatarMoeda(faturamentoTotal);


        clientesRecentes.innerHTML = clientesData.length
            ? clientesData.map(criarLinhaCliente).join('')
            : '<div class="list-group-item">Nenhum cliente recente encontrado.</div>';
    } catch (error) {
        console.error('Erro ao carregar dashboard:', error);
        statusCard.innerHTML = '<span class="badge bg-danger">✗ Falha ao carregar</span>';
        mostrarAlerta(`Não foi possível carregar os dados do dashboard. Verifique a conexão com o servidor. (${error.message})`, 'danger');
    }
}
