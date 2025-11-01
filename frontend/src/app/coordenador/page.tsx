"use client"

import { useEffect, useState } from "react"
import { useRouter } from "next/navigation"
import { Button } from "@/components/ui/button"

type Analise = any

export default function CoordenadorPage() {
    const router = useRouter()
    const [loading, setLoading] = useState(true)
    const [data, setData] = useState<{ usuario?: any; obter_todos?: Analise[]; contagem_por_status?: any[]; ultimas_analises?: Analise[] } | null>(null)
    const [error, setError] = useState<string | null>(null)

    useEffect(() => {
        let mounted = true
        async function load() {
            setLoading(true)
            try {
                const base = process.env.NEXT_PUBLIC_API_URL || "/api"
                const res = await fetch(`${base}/coordenador`, { credentials: "include", headers: { Accept: 'application/json' } })
                if (res.status === 401) {
                    try {
                        const j = await res.json()
                        if (j && j.redirect) {
                            window.location.href = j.redirect
                            return
                        }
                    } catch (e) { }
                    throw new Error('Não autenticado')
                }
                if (!res.ok) {
                    throw new Error(`HTTP ${res.status}`)
                }
                const json = await res.json()
                if (mounted) setData(json)
            } catch (err: any) {
                setError(err.message || "Erro ao carregar dados")
            } finally {
                if (mounted) setLoading(false)
            }
        }
        load()
        return () => { mounted = false }
    }, [])

    if (error) return <div className="p-8 text-red-600">{error}</div>

    const contagem = data?.contagem_por_status || []
    const ultimas = data?.ultimas_analises || []
    const total = contagem.reduce((s: number, item: any) => s + (item.quantidade || 0), 0)

    const usuario = data?.usuario
    const nomeUsuario = usuario?.nome_usuario || "Usuário"
    const primeiraLetra = nomeUsuario.charAt(0).toUpperCase()

    // Log para debug
    console.log('Contagem por status:', contagem)

    // Cores para cada status (baseado nos status reais do sistema)
    const getStatusColor = (status: string): string => {
        const statusLower = status?.toLowerCase() || ""

        // Aprovado – título emitido, mas não entregue (cinza)
        if (statusLower.includes("aprovado") && statusLower.includes("título") && statusLower.includes("não")) {
            return "#73ad4cff"
        }

        // Reprovado – notificação ao proprietário/possuidor realizada (azul claro)
        if (statusLower.includes("reprovado") && statusLower.includes("realizada")) {
            return "#6B7280"
        }

        // Análise iniciada – ainda sem parecer (amarelo)
        if (statusLower.includes("análise") && statusLower.includes("iniciada")) {
            return "#FACC15"
        }

        // Aprovado – título emitido e entregue (verde escuro)
        if (statusLower.includes("aprovado") && statusLower.includes("título") && statusLower.includes("entregue")) {
            return "#057a55ff"
        }

        // Reprovado – notificação ao proprietário/possuidor pendente (azul escuro)
        if (statusLower.includes("reprovado") && statusLower.includes("pendente")) {
            return "#1E3A8A"
        }

        return "#9CA3AF" // Cinza padrão
    }

    const handleVerProcessos = (status: string) => {
        router.push(`/coordenador/processos?status=${encodeURIComponent(status)}`)
    }

    return (
        <div className="flex min-h-screen bg-gray-50">
            {/* Sidebar */}
            <aside className="w-64 bg-[#2563EB] text-white p-6 flex flex-col">
                <div className="flex items-center space-x-3 mb-8">
                    <div className="w-10 h-10 bg-white rounded-lg flex items-center justify-center p-1">
                        <img src="/logo_login.png" alt="IntegraCAR" className="w-full h-full object-contain" />
                    </div>
                    <div className="font-bold text-lg">IntegraCAR</div>
                </div>

                <div className="text-sm text-white/70 mb-2">Dashboard</div>
                <nav className="space-y-1">
                    <div className="px-4 py-2.5 bg-white/10 rounded-md text-sm font-medium flex items-center space-x-2">
                        <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                        </svg>
                        <span>Processos CAR</span>
                    </div>
                    <div className="px-4 py-2.5 hover:bg-white/10 rounded-md text-sm cursor-pointer flex items-center space-x-2">
                        <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
                        </svg>
                        <span>Capacitações</span>
                    </div>
                    <div className="px-4 py-2.5 hover:bg-white/10 rounded-md text-sm cursor-pointer flex items-center space-x-2">
                        <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.75 17L9 20l-1 1h8l-1-1-.75-3M3 13h18M5 17h14a2 2 0 002-2V5a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                        </svg>
                        <span>Produtos TI</span>
                    </div>
                </nav>

                <div className="text-sm text-white/70 mb-2 mt-8">Cadastrar</div>
                <nav className="space-y-1">
                    <div className="px-4 py-2.5 hover:bg-white/10 rounded-md text-sm cursor-pointer flex items-center space-x-2">
                        <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
                        </svg>
                        <span>Cadastrar Processo</span>
                    </div>
                </nav>

                <div className="text-sm text-white/70 mb-2 mt-8">Ajustes</div>
                <nav className="space-y-1">
                    <div className="px-4 py-2.5 hover:bg-white/10 rounded-md text-sm cursor-pointer flex items-center space-x-2">
                        <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                        </svg>
                        <span>Configurações</span>
                    </div>
                    <div className="px-4 py-2.5 hover:bg-white/10 rounded-md text-sm cursor-pointer flex items-center space-x-2">
                        <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
                        </svg>
                        <span>Sair</span>
                    </div>
                </nav>
            </aside>

            {/* Main Content */}
            <main className="flex-1 p-8">
                {/* Header */}
                <div className="flex items-center justify-between mb-8">
                    <div className="flex items-center space-x-6">
                        <div>
                            <h1 className="text-2xl font-semibold text-gray-900">Processos CAR</h1>
                        </div>
                        <div className="flex space-x-4 text-sm">
                            <button className="px-4 py-2 text-gray-700 border-b-2 border-blue-600 font-medium">
                                Número de Processos
                            </button>
                            <button
                                onClick={() => router.push('/coordenador/graficos')}
                                className="px-4 py-2 text-gray-500 hover:text-gray-700"
                            >
                                Gráficos
                            </button>
                        </div>
                    </div>
                    <div className="flex items-center space-x-4">
                        <div className="flex items-center space-x-2">
                            <span className="text-sm font-medium text-gray-700">{nomeUsuario}</span>
                            <div className="w-8 h-8 bg-yellow-400 rounded-full flex items-center justify-center text-white font-bold text-sm">
                                {primeiraLetra}
                            </div>
                        </div>
                        <Button className="bg-[#2563EB] hover:bg-[#1D4ED8] text-white flex items-center space-x-2">
                            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
                            </svg>
                            <span>Cadastrar Processo</span>
                        </Button>
                    </div>
                </div>

                {/* Content Grid */}
                <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                    {/* Left Panel - Chart and Status List */}
                    <div className="bg-white rounded-lg shadow p-6">
                        <h2 className="text-sm font-medium text-gray-900 mb-4">Número de Processos</h2>

                        {/* Donut Chart */}
                        <div className="flex items-center justify-center mb-6">
                            <div className="relative w-64 h-36">
                                <svg viewBox="0 0 120 70" className="w-full h-full">
                                    {contagem.map((item: any, idx: number) => {
                                        const offset = contagem.slice(0, idx).reduce((s: number, c: any) => s + (c.quantidade || 0), 0)
                                        const percent = total > 0 ? ((item.quantidade || 0) / total) * 100 : 0
                                        const offsetPercent = total > 0 ? (offset / total) * 100 : 0
                                        // Para semicírculo, usamos metade da circunferência
                                        const circumference = Math.PI * 51 // metade do círculo (raio 51)
                                        const strokeDasharray = `${(percent / 100) * circumference} ${circumference}`
                                        const strokeDashoffset = -((offsetPercent / 100) * circumference)
                                        const color = getStatusColor(item.tipo_status)

                                        return (
                                            <path
                                                key={idx}
                                                d="M 9 60 A 51 51 0 0 1 111 60"
                                                fill="none"
                                                stroke={color}
                                                strokeWidth="17"
                                                strokeDasharray={strokeDasharray}
                                                strokeDashoffset={strokeDashoffset}
                                                strokeLinecap="butt"
                                            />
                                        )
                                    })}
                                </svg>
                                <div className="absolute inset-0 flex items-end justify-center pb-3">
                                    <div className="text-center">
                                        <div className="text-4xl font-bold text-gray-900">{total}</div>
                                        <div className="text-xs text-gray-400">Total</div>
                                    </div>
                                </div>
                            </div>
                        </div>

                        {/* Status List */}
                        <div className="space-y-3">
                            <div className="flex items-center justify-between text-sm font-medium text-gray-700 pb-2 border-b">
                                <span>Status</span>
                                <span>Quantidade</span>
                            </div>
                            {contagem.map((item: any, idx: number) => (
                                <div key={idx} className="flex items-center justify-between text-sm">
                                    <div className="flex items-center space-x-2">
                                        <div
                                            className="w-3 h-3 rounded-full flex-shrink-0"
                                            style={{ backgroundColor: getStatusColor(item.tipo_status) }}
                                        />
                                        <span className="text-gray-700">{item.tipo_status}</span>
                                    </div>
                                    <span className="font-medium text-gray-900">{item.quantidade}</span>
                                </div>
                            ))}
                        </div>
                    </div>

                    {/* Right Panel - Process List */}
                    <div className="lg:col-span-2 bg-white rounded-lg shadow">
                        <div className="p-6">
                            <div className="grid grid-cols-3 gap-4 text-sm font-medium text-gray-700 pb-4 border-b">
                                <div>Status</div>
                                <div className="text-center">Última Atualização</div>
                                <div className="text-right"></div>
                            </div>

                            <div className="divide-y">
                                {ultimas.map((item: any, idx: number) => (
                                    <div key={idx} className="grid grid-cols-3 gap-4 py-4 items-center">
                                        <div className="flex items-center space-x-3">
                                            <div
                                                className="w-3 h-3 rounded-full flex-shrink-0"
                                                style={{ backgroundColor: getStatusColor(item.tipo_status) }}
                                            />
                                            <div>
                                                <div className="text-sm font-medium text-gray-900">
                                                    {item.tipo_status || 'Status'}
                                                </div>
                                            </div>
                                        </div>
                                        <div className="text-sm text-gray-500 text-center">
                                            {item.ultima_atualizacao
                                                ? new Date(item.ultima_atualizacao).toLocaleDateString('pt-BR', { day: '2-digit', month: '2-digit', year: 'numeric' })
                                                : '-'
                                            }
                                        </div>
                                        <div className="text-right">
                                            <Button
                                                variant="default"
                                                size="sm"
                                                className="bg-[#3B82F6] hover:bg-[#2563EB] text-white"
                                                onClick={() => handleVerProcessos(item.tipo_status)}
                                            >
                                                ▶ Ver Processos
                                            </Button>
                                        </div>
                                    </div>
                                ))}
                            </div>
                        </div>
                    </div>
                </div>
            </main>
        </div>
    )
}
