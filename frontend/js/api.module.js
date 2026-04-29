export const API_BASE_URL = 'http://localhost:8000/api/v1';

async function apiCall(endpoint, options = {}) {
    const url = `${API_BASE_URL}${endpoint}`;
    const defaultOptions = {
        headers: {
            'Content-Type': 'application/json',
        },
    };

    const mergedOptions = { ...defaultOptions, ...options };

    try {
        const response = await fetch(url, mergedOptions);

        if (!response.ok) {
            const errorText = await response.text();
            let message = `HTTP error! status: ${response.status}`;
            try {
                const errorJson = JSON.parse(errorText);
                if (errorJson.detail) {
                    message += ` - ${errorJson.detail}`;
                }
            } catch (parseError) {
                if (errorText) {
                    message += ` - ${errorText}`;
                }
            }
            throw new Error(message);
        }

        if (response.status === 204) {
            return null;
        }

        const text = await response.text();
        return text ? JSON.parse(text) : null;
    } catch (error) {
        console.error(`Erro na chamada à API (${endpoint}):`, error);
        throw error;
    }
}

export async function apiGet(endpoint) {
    return apiCall(endpoint, { method: 'GET' });
}

export async function apiPost(endpoint, data) {
    return apiCall(endpoint, {
        method: 'POST',
        body: JSON.stringify(data),
    });
}

export async function apiPut(endpoint, data) {
    return apiCall(endpoint, {
        method: 'PUT',
        body: JSON.stringify(data),
    });
}

export async function apiDelete(endpoint) {
    return apiCall(endpoint, { method: 'DELETE' });
}

export function getClientes(skip = 0, limit = 100) {
    return apiGet(`/clientes?skip=${skip}&limit=${limit}`);
}

export function getCliente(id) {
    return apiGet(`/clientes/${id}`);
}

export function createCliente(data) {
    return apiPost('/clientes', data);
}

export function updateCliente(id, data) {
    return apiPut(`/clientes/${id}`, data);
}

export function deleteCliente(id) {
    return apiDelete(`/clientes/${id}`);
}

export function getFornecedores(skip = 0, limit = 100) {
    return apiGet(`/fornecedores?skip=${skip}&limit=${limit}`);
}

export function getFornecedor(id) {
    return apiGet(`/fornecedores/${id}`);
}

export function createFornecedor(data) {
    return apiPost('/fornecedores', data);
}

export function updateFornecedor(id, data) {
    return apiPut(`/fornecedores/${id}`, data);
}

export function deleteFornecedor(id) {
    return apiDelete(`/fornecedores/${id}`);
}

export function getProdutos(skip = 0, limit = 100) {
    return apiGet(`/produtos?skip=${skip}&limit=${limit}`);
}

export function getProduto(id) {
    return apiGet(`/produtos/${id}`);
}

export function createProduto(data) {
    return apiPost('/produtos', data);
}

export function updateProduto(id, data) {
    return apiPut(`/produtos/${id}`, data);
}

export function deleteProduto(id) {
    return apiDelete(`/produtos/${id}`);
}

export function getProdutosEstoqueBaixo() {
    return apiGet('/produtos/estoque-baixo');
}

export function movimentarEstoque(data) {
    return apiPost('/estoque/movimentar', data);
}

export function getMovimentacoesProduto(produtoId) {
    return apiGet(`/estoque/movimentacoes/${produtoId}`);
}

export function getRelatorioEstoque() {
    return apiGet('/estoque/relatorio/resumo');
}

export function getOrdensServico(skip = 0, limit = 100, status = null) {
    let url = `/ordens-servico?skip=${skip}&limit=${limit}`;
    if (status) url += `&status=${status}`;
    return apiGet(url);
}

export function getOrdensServicoRange({ skip = 0, limit = 100, status = null, dataInicio = null, dataFim = null } = {}) {
    let url = `/ordens-servico?skip=${skip}&limit=${limit}`;
    if (status) url += `&status=${status}`;
    if (dataInicio) url += `&data_inicio=${encodeURIComponent(dataInicio)}`;
    if (dataFim) url += `&data_fim=${encodeURIComponent(dataFim)}`;
    return apiGet(url);
}

export function getOrdemServico(id) {
    return apiGet(`/ordens-servico/${id}`);
}

export function createOrdemServico(data) {
    return apiPost('/ordens-servico', data);
}

export function updateOrdemServico(id, data) {
    return apiPut(`/ordens-servico/${id}`, data);
}

export function deleteOrdemServico(id) {
    return apiDelete(`/ordens-servico/${id}`);
}

export function adicionarItemOS(osId, itemData) {
    return apiPost(`/ordens-servico/${osId}/itens`, itemData);
}

export function listarItensOS(osId) {
    return apiGet(`/ordens-servico/${osId}/itens`);
}

export function carregarDadosTabela(endpoint, tabelaId, colunas) {
    return apiGet(endpoint).then(dados => {
        const tabela = document.getElementById(tabelaId);
        tabela.innerHTML = '';
        dados.forEach(item => {
            const linha = document.createElement('tr');
            colunas.forEach(coluna => {
                const td = document.createElement('td');
                td.textContent = item[coluna] || '-';
                linha.appendChild(td);
            });
            tabela.appendChild(linha);
        });
    });
}
