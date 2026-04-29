import {
    getClientes,
    getOrdensServico,
    getOrdensServicoRange,
    getRelatorioEstoque,
} from './api.module.js';
import { formatarMoeda, mostrarAlerta } from './utils.js';

const API_HEALTH_URL = 'http://localhost:8000/health';

function criarDataISO(data) {
    return data.toISOString();
}

function obterInicioDoMes() {
    const hoje = new Date();
    return new Date(hoje.getFullYear(), hoje.getMonth(), 1, 0, 0, 0, 0);
}

function obterFinalDoDia(data) {
    const fim = new Date(data);
    fim.setHours(23, 59, 59, 999);
    return fim;
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
        const hoje = new Date();
        const inicioMes = criarDataISO(obterInicioDoMes());
        const fimMes = criarDataISO(obterFinalDoDia(new Date(hoje.getFullYear(), hoje.getMonth() + 1, 0)));
        const inicioHoje = criarDataISO(new Date(hoje.setHours(0, 0, 0, 0)));
        const fimHoje = criarDataISO(obterFinalDoDia(new Date()));

        const [healthResponse, ordensAbertasData, clientesData, estoqueData, ordensHojeData, faturamentoData] =
            await Promise.all([
                fetch(API_HEALTH_URL),
                getOrdensServico(0, 1000, 'ABERTA'),
                getClientes(0, 5),
                getRelatorioEstoque(),
                getOrdensServicoRange({ skip: 0, limit: 1000, dataInicio: inicioHoje, dataFim: fimHoje }),
                getOrdensServicoRange({ skip: 0, limit: 1000, dataInicio: inicioMes, dataFim: fimMes }),
            ]);

        statusCard.innerHTML = healthResponse.ok
            ? '<span class="badge bg-success">✓ API conectada</span>'
            : '<span class="badge bg-danger">✗ API indisponível</span>';

        osAbertas.textContent = ordensAbertasData.length;
        estoqueBaixo.textContent = estoqueData.produtos_com_estoque_baixo || 0;
        servicosHoje.textContent = ordensHojeData.length;

        const faturamentoTotal = (faturamentoData || []).reduce((total, ordem) => {
            return total + (ordem.valor_final || 0);
        }, 0);
        faturamento.textContent = formatarMoeda(faturamentoTotal);

        clientesRecentes.innerHTML = clientesData.length
            ? clientesData.map(criarLinhaCliente).join('')
            : '<div class="list-group-item">Nenhum cliente recente encontrado.</div>';
    } catch (error) {
        console.error('Erro ao carregar dashboard:', error);
        statusCard.innerHTML = '<span class="badge bg-danger">✗ Falha ao carregar</span>';
        mostrarAlerta('Não foi possível carregar os dados do dashboard. Verifique a conexão com o servidor.', 'danger');
    }
}
