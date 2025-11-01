"use client"

import { useEffect, useState } from "react"
import { useRouter } from "next/navigation"
import { Button } from "@/components/ui/button"

type ContagemItem = {
    nome_campus?: string
    nome_usuario?: string
    quantidade: number
}

export default function GraficosPage() {
    const router = useRouter()
    const [loading, setLoading] = useState(true)
    const [data, setData] = useState<{
        usuario?: any
        contagem_campus?: ContagemItem[]
        contagem_orientador?: ContagemItem[]
        contagem_bolsista?: ContagemItem[]
    } | null>(null)
    const [error, setError] = useState<string | null>(null)
    const [tipoGrafico, setTipoGrafico] = useState<'campus' | 'orientador' | 'bolsista'>('campus')

    useEffect(() => {
        let mounted = true
        async function load() {
            setLoading(true)
            try {
                const base = process.env.NEXT_PUBLIC_API_URL || "/api"
                const res = await fetch(`${base}/graficos`, {
                    credentials: "include",
                    headers: { Accept: 'application/json' }
                })
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

    const usuario = data?.usuario
    const nomeUsuario = usuario?.nome_usuario || "Usuário"
    const primeiraLetra = nomeUsuario.charAt(0).toUpperCase()

    // Selecionar dados baseado no tipo de gráfico
    const dadosGrafico = tipoGrafico === 'campus'
        ? data?.contagem_campus || []
        : tipoGrafico === 'orientador'
            ? data?.contagem_orientador || []
            : data?.contagem_bolsista || []

    const total = dadosGrafico.reduce((s, item) => s + (item.quantidade || 0), 0)

    // Gerar cores para o gráfico de barras
    const getCor = (index: number): string => {
        const cores = [
            '#E8B4D4', '#D4A5C7', '#C096BA', '#AC87AD',
            '#9878A0', '#846993', '#705A86', '#5C4B79',
            '#483C6C', '#342D5F', '#201E52'
        ]
        return cores[index % cores.length]
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
                    <div
                        onClick={() => router.push('/coordenador')}
                        className="px-4 py-2.5 hover:bg-white/10 rounded-md text-sm font-medium flex items-center space-x-2 cursor-pointer"
                    >
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
                            <h1 className="text-2xl font-semibold text-gray-900">Gráficos</h1>
                        </div>
                        <div className="flex space-x-4 text-sm">
                            <button
                                onClick={() => setTipoGrafico('campus')}
                                className={`px-4 py-2 border-b-2 font-medium ${tipoGrafico === 'campus'
                                    ? 'text-gray-700 border-blue-600'
                                    : 'text-gray-500 border-transparent hover:text-gray-700'
                                    }`}
                            >
                                Por Campus
                            </button>
                            <button
                                onClick={() => setTipoGrafico('orientador')}
                                className={`px-4 py-2 border-b-2 font-medium ${tipoGrafico === 'orientador'
                                    ? 'text-gray-700 border-blue-600'
                                    : 'text-gray-500 border-transparent hover:text-gray-700'
                                    }`}
                            >
                                Por Orientador
                            </button>
                            <button
                                onClick={() => setTipoGrafico('bolsista')}
                                className={`px-4 py-2 border-b-2 font-medium ${tipoGrafico === 'bolsista'
                                    ? 'text-gray-700 border-blue-600'
                                    : 'text-gray-500 border-transparent hover:text-gray-700'
                                    }`}
                            >
                                Por Bolsista
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
                    </div>
                </div>

                {/* Content */}
                <div className="bg-white rounded-lg shadow p-8">
                    <div className="mb-6">
                        <h2 className="text-lg font-semibold text-gray-900 mb-2">
                            Número de Processos por {
                                tipoGrafico === 'campus' ? 'Campus' :
                                    tipoGrafico === 'orientador' ? 'Orientador' :
                                        'Bolsista'
                            }
                        </h2>
                    </div>

                    {/* Gráfico de Barras */}
                    <div className="space-y-6">
                        {dadosGrafico.length === 0 ? (
                            <div className="text-center text-gray-500 py-12">
                                Nenhum dado disponível
                            </div>
                        ) : (
                            <>
                                {/* Calcular valor máximo para escala dinâmica */}
                                {(() => {
                                    const maxQuantidade = Math.max(...dadosGrafico.map(item => item.quantidade))
                                    const maxEscala = Math.ceil(maxQuantidade / 5) * 5 // Arredonda para o próximo múltiplo de 5
                                    const step = maxEscala / 10 // Divide em 10 partes
                                    const labels = Array.from({ length: 11 }, (_, i) => Math.round(i * step))

                                    return (
                                        <>
                                            {/* Escala do eixo Y */}
                                            <div className="flex">
                                                <div className="w-12 flex flex-col-reverse justify-between text-xs text-gray-500 mr-4" style={{ height: '300px' }}>
                                                    {labels.map(value => (
                                                        <div key={value} className="text-right">{value}</div>
                                                    ))}
                                                </div>

                                                {/* Barras */}
                                                <div className="flex-1 flex items-end space-x-3" style={{ height: '300px' }}>
                                                    {dadosGrafico.map((item, index) => {
                                                        const altura = (item.quantidade / maxEscala) * 100
                                                        const nome = item.nome_campus || item.nome_usuario || 'N/A'
                                                        // Usar as 3 primeiras letras para evitar duplicatas
                                                        const sigla = nome.substring(0, 3).toUpperCase()

                                                        return (
                                                            <div key={index} className="flex-1 flex flex-col items-center">
                                                                <div className="w-full flex items-end justify-center" style={{ height: '280px' }}>
                                                                    <div
                                                                        className="w-full rounded-t transition-all hover:opacity-80"
                                                                        style={{
                                                                            backgroundColor: getCor(index),
                                                                            height: `${altura}%`,
                                                                            minHeight: item.quantidade > 0 ? '20px' : '0'
                                                                        }}
                                                                        title={`${nome}: ${item.quantidade}`}
                                                                    />
                                                                </div>
                                                                <div className="text-xs text-gray-600 mt-2 text-center font-medium">
                                                                    {sigla}
                                                                </div>
                                                            </div>
                                                        )
                                                    })}
                                                </div>
                                            </div>
                                        </>
                                    )
                                })()}

                                {/* Legenda */}
                                <div className="border-t pt-6 mt-6">
                                    <h3 className="text-sm font-semibold text-gray-700 mb-4">Legenda:</h3>
                                    <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
                                        {dadosGrafico.map((item, index) => {
                                            const nome = item.nome_campus || item.nome_usuario || 'N/A'
                                            const sigla = nome.substring(0, 3).toUpperCase()

                                            return (
                                                <div key={index} className="flex items-center space-x-2">
                                                    <div
                                                        className="w-4 h-4 rounded flex-shrink-0"
                                                        style={{ backgroundColor: getCor(index) }}
                                                    />
                                                    <span className="text-sm text-gray-700">
                                                        <span className="font-medium">{sigla}:</span> {nome} ({item.quantidade})
                                                    </span>
                                                </div>
                                            )
                                        })}
                                    </div>
                                </div>
                            </>
                        )}
                    </div>
                </div>
            </main>
        </div>
    )
}
