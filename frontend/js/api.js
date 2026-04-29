/* API Helper Functions */

const API_BASE_URL = 'http://localhost:8000/api/v1';

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

// GET
function apiGet(endpoint) {
    return apiCall(endpoint, { method: 'GET' });
}

// POST
function apiPost(endpoint, data) {
    return apiCall(endpoint, {
        method: 'POST',
        body: JSON.stringify(data),
    });
}

// PUT
function apiPut(endpoint, data) {
    return apiCall(endpoint, {
        method: 'PUT',
        body: JSON.stringify(data),
    });
}

// DELETE
function apiDelete(endpoint) {
    return apiCall(endpoint, { method: 'DELETE' });
}

// Funções específicas por módulo

// CLIENTES
function getClientes(skip = 0, limit = 100) {
    return apiGet(`/clientes?skip=${skip}&limit=${limit}`);
}

function getCliente(id) {
    return apiGet(`/clientes/${id}`);
}

function createCliente(data) {
    return apiPost('/clientes', data);
}

function updateCliente(id, data) {
    return apiPut(`/clientes/${id}`, data);
}

function deleteCliente(id) {
    return apiDelete(`/clientes/${id}`);
}

// FORNECEDORES
function getFornecedores(skip = 0, limit = 100) {
    return apiGet(`/fornecedores?skip=${skip}&limit=${limit}`);
}

function getFornecedor(id) {
    return apiGet(`/fornecedores/${id}`);
}

function createFornecedor(data) {
    return apiPost('/fornecedores', data);
}

function updateFornecedor(id, data) {
    return apiPut(`/fornecedores/${id}`, data);
}

function deleteFornecedor(id) {
    return apiDelete(`/fornecedores/${id}`);
}

// PRODUTOS
function getProdutos(skip = 0, limit = 100) {
    return apiGet(`/produtos?skip=${skip}&limit=${limit}`);
}

function getProduto(id) {
    return apiGet(`/produtos/${id}`);
}

function createProduto(data) {
    return apiPost('/produtos', data);
}

function updateProduto(id, data) {
    return apiPut(`/produtos/${id}`, data);
}

function deleteProduto(id) {
    return apiDelete(`/produtos/${id}`);
}

function getProdutosEstoqueBaixo() {
    return apiGet('/produtos/estoque-baixo');
}

// ESTOQUE
function movimentarEstoque(data) {
    return apiPost('/estoque/movimentar', data);
}

function getMovimentacoesProduto(produtoId) {
    return apiGet(`/estoque/movimentacoes/${produtoId}`);
}

function getRelatorioEstoque() {
    return apiGet('/estoque/relatorio/resumo');
}

// ORDENS DE SERVIÇO
function getOrdensServico(skip = 0, limit = 100, status = null) {
    let url = `/ordens-servico?skip=${skip}&limit=${limit}`;
    if (status) url += `&status=${status}`;
    return apiGet(url);
}

function getOrdemServico(id) {
    return apiGet(`/ordens-servico/${id}`);
}

function createOrdemServico(data) {
    return apiPost('/ordens-servico', data);
}

function updateOrdemServico(id, data) {
    return apiPut(`/ordens-servico/${id}`, data);
}

function deleteOrdemServico(id) {
    return apiDelete(`/ordens-servico/${id}`);
}

function adicionarItemOS(osId, itemData) {
    return apiPost(`/ordens-servico/${osId}/itens`, itemData);
}

function listarItensOS(osId) {
    return apiGet(`/ordens-servico/${osId}/itens`);
}

// Utilitários

function formatarData(data) {
    return new Date(data).toLocaleDateString('pt-BR');
}

function formatarDataHora(data) {
    return new Date(data).toLocaleString('pt-BR');
}

function formatarMoeda(valor) {
    return new Intl.NumberFormat('pt-BR', {
        style: 'currency',
        currency: 'BRL',
    }).format(valor);
}

function mostrarAlerta(mensagem, tipo = 'info') {
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

function carregarDadosTabela(endpoint, tabelaId, colunas) {
    apiGet(endpoint)
        .then(dados => {
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
        })
        .catch(erro => {
            mostrarAlerta('Erro ao carregar dados: ' + erro.message, 'danger');
        });
}

// Expor funções no escopo global para compatibilidade com o frontend atual
window.apiGet = apiGet;
window.apiPost = apiPost;
window.apiPut = apiPut;
window.apiDelete = apiDelete;
window.getClientes = getClientes;
window.getCliente = getCliente;
window.createCliente = createCliente;
window.updateCliente = updateCliente;
window.deleteCliente = deleteCliente;
window.getFornecedores = getFornecedores;
window.getFornecedor = getFornecedor;
window.createFornecedor = createFornecedor;
window.updateFornecedor = updateFornecedor;
window.deleteFornecedor = deleteFornecedor;
window.getProdutos = getProdutos;
window.getProduto = getProduto;
window.createProduto = createProduto;
window.updateProduto = updateProduto;
window.deleteProduto = deleteProduto;
window.getProdutosEstoqueBaixo = getProdutosEstoqueBaixo;
window.movimentarEstoque = movimentarEstoque;
window.getMovimentacoesProduto = getMovimentacoesProduto;
window.getRelatorioEstoque = getRelatorioEstoque;
window.getOrdensServico = getOrdensServico;
window.getOrdemServico = getOrdemServico;
window.createOrdemServico = createOrdemServico;
window.updateOrdemServico = updateOrdemServico;
window.deleteOrdemServico = deleteOrdemServico;
window.adicionarItemOS = adicionarItemOS;
window.listarItensOS = listarItensOS;
window.formatarData = formatarData;
window.formatarDataHora = formatarDataHora;
window.formatarMoeda = formatarMoeda;
window.mostrarAlerta = mostrarAlerta;
window.carregarDadosTabela = carregarDadosTabela;
