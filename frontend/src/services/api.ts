import axios from 'axios'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

export const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json'
  }
})

// Interceptor para adicionar token
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('bi_token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

// Interceptor para tratar erros
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('bi_token')
      localStorage.removeItem('bi_user')
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

// Serviços de Dashboard
export const dashboardService = {
  getSelosFaltantes: (params?: {
    data_inicio?: string
    data_fim?: string
    contrato_id?: string
    page?: number
    limit?: number
  }) => api.get('/dashboard/selos-faltantes', { params }),

  exportSelosFaltantes: (params?: {
    data_inicio?: string
    data_fim?: string
    contrato_id?: string
  }) => api.get('/dashboard/selos-faltantes/export', { 
    params,
    responseType: 'blob'
  }),

  getEvolucaoMensal: (contrato_id?: string) => 
    api.get('/dashboard/evolucao-mensal', { params: { contrato_id } }),

  getResumo: (contrato_id?: string) => 
    api.get('/dashboard/resumo', { params: { contrato_id } })
}

// Serviços de Importação
export const importService = {
  importarArquivo: (tipo: string, arquivo: File) => {
    const formData = new FormData()
    formData.append('arquivo', arquivo)
    return api.post(`/import/pr/${tipo}`, formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })
  },

  listarImportacoes: () => api.get('/importacoes')
}

// Serviços de Usuários
export const usuariosService = {
  listar: () => api.get('/usuarios'),
  criar: (dados: {
    email: string
    senha: string
    nome: string
    role: string
    contrato_id: string
  }) => api.post('/usuarios', dados),
  atualizar: (id: number, dados: {
    nome?: string
    role?: string
    ativo?: boolean
  }) => api.put(`/usuarios/${id}`, dados)
}

// Serviços de Contratos
export const contratosService = {
  listar: () => api.get('/contratos'),
  criar: (dados: {
    contrato_id: string
    nome: string
    nome_fantasia?: string
    cidade?: string
    uf?: string
    vertical?: string
  }) => api.post('/contratos', dados)
}
