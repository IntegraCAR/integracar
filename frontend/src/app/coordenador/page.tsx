"use client"

import { useEffect, useState } from "react"
import { Button } from "@/components/ui/button"
import { apiFetch } from "@/lib/api"

type Analise = any

export default function CoordenadorPage() {
    const [loading, setLoading] = useState(true)
    const [data, setData] = useState<{ usuario?: any; obter_todos?: Analise[]; contagem_por_status?: any[]; ultimas_analises?: Analise[] } | null>(null)
    const [error, setError] = useState<string | null>(null)

    useEffect(() => {
        let mounted = true
        async function load() {
            setLoading(true)
            try {
                const base = process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000"
                const res = await fetch(`${base}/coordenador`, { credentials: "include", headers: { Accept: 'application/json' } })
                if (res.status === 401) {
                    // backend returned JSON indicating not authenticated and a redirect URL
                    try {
                        const j = await res.json()
                        if (j && j.redirect) {
                            // navigate to frontend login (redirect is a relative path)
                            window.location.href = j.redirect
                            return
                        }
                    } catch (e) {
                        // fallthrough to error
                    }
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

    if (loading) return <div className="p-8">Carregando painel do coordenador...</div>
    if (error) return <div className="p-8 text-red-600">{error}</div>

    const contagem = data?.contagem_por_status || []
    const ultimas = data?.ultimas_analises || []

    // compute total
    const total = contagem.reduce((s: number, item: any) => s + (item.quantidade || 0), 0)

    return (
        <div className="flex">
            {/* Sidebar azul */}
            <aside className="w-64 bg-[#1E6FB8] text-white min-h-screen p-6 hidden md:block">
                <div className="flex items-center space-x-3 mb-8">
                    <div className="w-10 h-10 bg-white/10 rounded-full flex items-center justify-center">IC</div>
                    <div>
                        <div className="font-bold">IntegraCAR</div>
                        <div className="text-xs opacity-80">Dashboard</div>
                    </div>
                </div>

                <nav className="space-y-2">
                    <div className="px-3 py-2 bg-[#16639B] rounded-md">Processos CAR</div>
                    <div className="px-3 py-2 hover:bg-white/10 rounded-md">Capacitações</div>
                    <div className="px-3 py-2 hover:bg-white/10 rounded-md">Produtos TI</div>
                    <div className="mt-4 text-xs opacity-80">Cadastrar</div>
                    <div className="px-3 py-2 hover:bg-white/10 rounded-md">Cadastrar Processo</div>
                    <div className="mt-6 text-xs opacity-80">Ajustes</div>
                    <div className="px-3 py-2 hover:bg-white/10 rounded-md">Configurações</div>
                    <div className="px-3 py-2 hover:bg-white/10 rounded-md">Sair</div>
                </nav>
            </aside>

            <main className="flex-1 p-6">
                {/* Top bar */}
                <div className="flex items-center justify-between mb-6">
                    <div className="flex items-center space-x-4">
                        <h1 className="text-xl font-semibold">Processos CAR</h1>
                        <div className="text-sm text-gray-500">Número de Processos</div>
                    </div>
                    <div className="flex items-center space-x-3">
                        <div className="text-sm text-gray-700">{data?.usuario?.nome_usuario || 'Coordenador'}</div>
                        <div className="w-8 h-8 rounded-full bg-green-500 text-white flex items-center justify-center">S</div>
                        <Button variant="outline" className="bg-[#0D6EAF] text-white border-none">Cadastrar Processo</Button>
                    </div>
                </div>

                {/* Content two columns */}
                <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                    {/* Left column: meter + list */}
                    <div className="lg:col-span-1 space-y-4">
                        <div className="bg-white rounded-md p-6 shadow">
                            <div className="flex items-center justify-between">
                                <div>
                                    <div className="text-sm text-gray-500">Número de Processos</div>
                                    <div className="text-3xl font-bold">{total}</div>
                                </div>
                                <div className="w-28 h-28 flex items-center justify-center rounded-full bg-gray-100">
                                    {/* Placeholder for gauge */}
                                    <div className="text-lg font-bold">{total}</div>
                                </div>
                            </div>

                            <div className="mt-6">
                                <ul className="space-y-2 text-sm text-gray-600">
                                    {contagem.map((c: any, idx: number) => (
                                        <li key={idx} className="flex items-center justify-between">
                                            <div className="flex items-center space-x-2">
                                                <span className="w-3 h-3 rounded-full bg-gray-400 block" />
                                                <span>{c.tipo_status || 'Indefinido'}</span>
                                            </div>
                                            <div className="text-gray-800">{c.quantidade}</div>
                                        </li>
                                    ))}
                                </ul>
                            </div>
                        </div>
                    </div>

                    {/* Right column: list and actions */}
                    <div className="lg:col-span-2 bg-white rounded-md p-6 shadow">
                        <div className="flex items-center justify-between mb-4">
                            <h2 className="text-sm font-medium text-gray-700">Status</h2>
                            <h3 className="text-sm text-gray-500">Última Atualização</h3>
                        </div>

                        <div className="space-y-4">
                            {ultimas.map((a: any, idx: number) => (
                                <div key={idx} className="flex items-center justify-between border rounded p-3">
                                    <div className="flex items-center space-x-4">
                                        <div className="w-3 h-3 rounded-full bg-blue-400" />
                                        <div>
                                            <div className="text-sm font-medium">{a.tipo_status || 'Status'}</div>
                                            <div className="text-xs text-gray-500">{a.numero_processo_florestal || `Processo ${a.cod_processo}`}</div>
                                        </div>
                                    </div>

                                    <div className="flex items-center space-x-4">
                                        <div className="text-sm text-gray-500">{a.data_hora_inicio_analise ? new Date(a.data_hora_inicio_analise).toLocaleDateString() : ''}</div>
                                        <Button variant="outline" className="bg-[#3B82F6] text-white border-none px-4 py-1 text-sm">Ver Processos</Button>
                                    </div>
                                </div>
                            ))}

                            {ultimas.length === 0 && (
                                <div className="text-sm text-gray-500">Nenhuma análise encontrada.</div>
                            )}
                        </div>
                    </div>
                </div>
            </main>
        </div>
    )
}
