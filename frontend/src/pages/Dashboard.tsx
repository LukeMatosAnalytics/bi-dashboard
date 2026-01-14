import { useState, useEffect } from 'react'
import { useAuth } from '../contexts/AuthContext'
import { dashboardService, contratosService } from '../services/api'
import { Card, CardHeader, CardContent } from '../components/ui/Card'
import { KPICard } from '../components/ui/KPICard'
import { Button } from '../components/ui/Button'
import { Input } from '../components/ui/Input'
import { Select } from '../components/ui/Select'
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer
} from 'recharts'
import {
  AlertTriangle,
  FileSpreadsheet,
  Download,
  RefreshCw,
  Filter,
  ChevronLeft,
  ChevronRight
} from 'lucide-react'
import { format } from 'date-fns'
import { ptBR } from 'date-fns/locale'

interface SeloFaltante {
  codigo_selo: string
  cod_tipo_ato: number | null
  descricao_tipo_ato: string | null
  livro: string | null
  folha: string | null
  capa: string | null
  data_ato: string | null
  os: string | null
}

interface Contrato {
  contrato_id: string
  nome: string
}

export default function Dashboard() {
  const { user } = useAuth()
  const [loading, setLoading] = useState(true)
  const [resumo, setResumo] = useState({ selos_faltantes: 0, total_os: 0, total_selos_os_selo: 0 })
  const [selosFaltantes, setSelosFaltantes] = useState<SeloFaltante[]>([])
  const [evolucao, setEvolucao] = useState<{ mes: string; quantidade: number }[]>([])
  const [contratos, setContratos] = useState<Contrato[]>([])
  const [pagination, setPagination] = useState({ total: 0, page: 1, totalPages: 1 })
  
  const [filters, setFilters] = useState({
    data_inicio: '',
    data_fim: '',
    contrato_id: ''
  })

  const isMaster = user?.role === 'MASTER'

  const fetchData = async () => {
    setLoading(true)
    try {
      const contratoId = isMaster ? filters.contrato_id : undefined
      
      const [resumoRes, selosRes, evolucaoRes] = await Promise.all([
        dashboardService.getResumo(contratoId),
        dashboardService.getSelosFaltantes({
          ...filters,
          contrato_id: contratoId,
          page: pagination.page,
          limit: 20
        }),
        dashboardService.getEvolucaoMensal(contratoId)
      ])

      setResumo(resumoRes.data)
      setSelosFaltantes(selosRes.data.data)
      setPagination({
        total: selosRes.data.total,
        page: selosRes.data.page,
        totalPages: selosRes.data.total_pages
      })
      setEvolucao(evolucaoRes.data)
    } catch (error) {
      console.error('Erro ao carregar dados:', error)
    } finally {
      setLoading(false)
    }
  }

  const fetchContratos = async () => {
    if (isMaster) {
      try {
        const res = await contratosService.listar()
        setContratos(res.data)
      } catch (error) {
        console.error('Erro ao carregar contratos:', error)
      }
    }
  }

  useEffect(() => {
    fetchContratos()
  }, [])

  useEffect(() => {
    fetchData()
  }, [pagination.page, filters.contrato_id])

  const handleFilter = () => {
    setPagination(prev => ({ ...prev, page: 1 }))
    fetchData()
  }

  const handleExport = async () => {
    try {
      const res = await dashboardService.exportSelosFaltantes({
        ...filters,
        contrato_id: isMaster ? filters.contrato_id : undefined
      })
      
      const blob = new Blob([res.data], { type: 'text/csv' })
      const url = window.URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = `selos_faltantes_${format(new Date(), 'yyyy-MM-dd')}.csv`
      a.click()
      window.URL.revokeObjectURL(url)
    } catch (error) {
      console.error('Erro ao exportar:', error)
    }
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Dashboard</h1>
          <p className="text-gray-500">Monitoramento de selos faltantes</p>
        </div>
        <Button onClick={fetchData} variant="secondary">
          <RefreshCw size={16} className="mr-2" />
          Atualizar
        </Button>
      </div>

      {/* KPIs */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <KPICard
          title="Selos Faltantes"
          value={resumo.selos_faltantes}
          subtitle="Não enviados ao FNC"
          icon={AlertTriangle}
          color="red"
        />
        <KPICard
          title="Total de OS"
          value={resumo.total_os}
          subtitle="Ordens de serviço"
          icon={FileSpreadsheet}
          color="blue"
        />
        <KPICard
          title="Selos em OS"
          value={resumo.total_selos_os_selo}
          subtitle="Selos vinculados"
          icon={FileSpreadsheet}
          color="green"
        />
      </div>

      {/* Filters */}
      <Card>
        <CardHeader>
          <div className="flex items-center gap-2">
            <Filter size={20} className="text-gray-500" />
            <span className="font-medium">Filtros</span>
          </div>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
            {isMaster && (
              <Select
                label="Contrato"
                value={filters.contrato_id}
                onChange={(e) => setFilters(prev => ({ ...prev, contrato_id: e.target.value }))}
                options={[
                  { value: '', label: 'Todos os contratos' },
                  ...contratos.map(c => ({ value: c.contrato_id, label: c.nome }))
                ]}
              />
            )}
            <Input
              type="date"
              label="Data Início"
              value={filters.data_inicio}
              onChange={(e) => setFilters(prev => ({ ...prev, data_inicio: e.target.value }))}
            />
            <Input
              type="date"
              label="Data Fim"
              value={filters.data_fim}
              onChange={(e) => setFilters(prev => ({ ...prev, data_fim: e.target.value }))}
            />
            <div className="flex items-end gap-2">
              <Button onClick={handleFilter}>Filtrar</Button>
              <Button onClick={handleExport} variant="secondary">
                <Download size={16} className="mr-2" />
                Exportar
              </Button>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Chart */}
      <Card>
        <CardHeader>
          <span className="font-medium">Evolução Mensal de Selos Faltantes</span>
        </CardHeader>
        <CardContent>
          <div className="h-80">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={evolucao}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="mes" />
                <YAxis />
                <Tooltip />
                <Line
                  type="monotone"
                  dataKey="quantidade"
                  stroke="#2563eb"
                  strokeWidth={2}
                  dot={{ fill: '#2563eb' }}
                />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </CardContent>
      </Card>

      {/* Table */}
      <Card>
        <CardHeader>
          <div className="flex items-center justify-between">
            <span className="font-medium">Selos Faltantes ({pagination.total} registros)</span>
          </div>
        </CardHeader>
        <CardContent className="p-0">
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Código do Selo</th>
                  <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Cód. Tipo Ato</th>
                  <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Descrição do Ato</th>
                  <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Livro</th>
                  <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Folha</th>
                  <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Capa</th>
                  <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Data</th>
                  <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">OS</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-100">
                {loading ? (
                  <tr>
                    <td colSpan={8} className="px-4 py-8 text-center text-gray-500">
                      Carregando...
                    </td>
                  </tr>
                ) : selosFaltantes.length === 0 ? (
                  <tr>
                    <td colSpan={8} className="px-4 py-8 text-center text-gray-500">
                      Nenhum selo faltante encontrado
                    </td>
                  </tr>
                ) : (
                  selosFaltantes.map((selo, idx) => (
                    <tr key={idx} className="hover:bg-gray-50">
                      <td className="px-4 py-3 text-sm font-medium text-gray-900">{selo.codigo_selo}</td>
                      <td className="px-4 py-3 text-sm text-gray-600">{selo.cod_tipo_ato || '-'}</td>
                      <td className="px-4 py-3 text-sm text-gray-600">{selo.descricao_tipo_ato || '-'}</td>
                      <td className="px-4 py-3 text-sm text-gray-600">{selo.livro || '-'}</td>
                      <td className="px-4 py-3 text-sm text-gray-600">{selo.folha || '-'}</td>
                      <td className="px-4 py-3 text-sm text-gray-600">{selo.capa || '-'}</td>
                      <td className="px-4 py-3 text-sm text-gray-600">
                        {selo.data_ato ? format(new Date(selo.data_ato), 'dd/MM/yyyy', { locale: ptBR }) : '-'}
                      </td>
                      <td className="px-4 py-3 text-sm text-gray-600">{selo.os || '-'}</td>
                    </tr>
                  ))
                )}
              </tbody>
            </table>
          </div>

          {/* Pagination */}
          {pagination.totalPages > 1 && (
            <div className="flex items-center justify-between px-4 py-3 border-t border-gray-100">
              <span className="text-sm text-gray-500">
                Página {pagination.page} de {pagination.totalPages}
              </span>
              <div className="flex gap-2">
                <Button
                  variant="ghost"
                  size="sm"
                  onClick={() => setPagination(prev => ({ ...prev, page: prev.page - 1 }))}
                  disabled={pagination.page === 1}
                >
                  <ChevronLeft size={16} />
                </Button>
                <Button
                  variant="ghost"
                  size="sm"
                  onClick={() => setPagination(prev => ({ ...prev, page: prev.page + 1 }))}
                  disabled={pagination.page === pagination.totalPages}
                >
                  <ChevronRight size={16} />
                </Button>
              </div>
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  )
}
