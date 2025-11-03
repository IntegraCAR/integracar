'use client';

import { useRouter, useSearchParams } from 'next/navigation';
import { useEffect, useState } from 'react';

export default function ProcessoPage() {
    const router = useRouter();
    const searchParams = useSearchParams();
    const cod = searchParams.get('cod');

    const [processo, setProcesso] = useState<any>(null);
    const [usuario, setUsuario] = useState<any>(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        carregarDados();
    }, [cod]);

    const carregarDados = async () => {
        try {
            // Carregar dados do usuário
            const base = process.env.NEXT_PUBLIC_API_URL || "/api"
            const userRes = await fetch(`${base}/bolsista`, {
                credentials: "include",
                headers: { Accept: 'application/json' }
            });
            
            if (userRes.status === 401) {
                try {
                    const j = await userRes.json()
                    if (j && j.redirect) {
                        window.location.href = j.redirect
                        return
                    }
                } catch (e) { }
                throw new Error('Não autenticado')
            }
            
            const userData = await userRes.json();
            setUsuario(userData.usuario);

            // Carregar dados do processo
            if (cod) {
                const response = await fetch(`${base}/processo/${cod}`, {
                    credentials: "include",
                    headers: { Accept: 'application/json' }
                });
                const data = await response.json();

                if (data.analises && data.analises.length > 0) {
                    const proc = data.analises[0];
                    
                    // Verificar se o processo pertence ao bolsista logado
                    if (proc.cod_usuario === userData.usuario.cod_usuario) {
                        setProcesso(proc);
                    } else {
                        setError('Você não tem permissão para acessar este processo');
                    }
                } else {
                    setError('Processo não encontrado');
                }
            }
        } catch (error: any) {
            setError(error.message || 'Erro ao carregar dados');
        } finally {
            setLoading(false);
        }
    };

    const formatarDataExibicao = (dataStr: string) => {
        if (!dataStr) return 'N/A';
        const data = new Date(dataStr);
        return data.toLocaleDateString('pt-BR', {
            day: '2-digit',
            month: '2-digit',
            year: 'numeric'
        });
    };

    const formatarDataHoraCompleta = (dataStr: string) => {
        if (!dataStr) return { data: 'N/A', hora: '' };
        const data = new Date(dataStr);
        const dataFormatada = data.toLocaleDateString('pt-BR', {
            day: '2-digit',
            month: '2-digit',
            year: 'numeric'
        });
        const horaFormatada = data.toLocaleTimeString('pt-BR', {
            hour: '2-digit',
            minute: '2-digit'
        });
        return { data: dataFormatada, hora: horaFormatada };
    };

    const nomeUsuario = usuario?.nome_usuario || "Usuário";
    const primeiraLetra = nomeUsuario.charAt(0).toUpperCase();

    if (loading) {
        return (
            <div className="flex items-center justify-center min-h-screen">
                <div className="text-lg">Carregando...</div>
            </div>
        );
    }

    if (error && !processo) {
        return (
            <div className="flex items-center justify-center min-h-screen">
                <div className="text-lg text-red-600">{error}</div>
            </div>
        );
    }

    if (!processo) {
        return (
            <div className="flex items-center justify-center min-h-screen">
                <div className="text-lg">Processo não encontrado</div>
            </div>
        );
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
                    <div
                        className="px-4 py-2.5 hover:bg-white/10 rounded-md text-sm cursor-pointer flex items-center space-x-2"
                        onClick={() => router.push('/bolsista')}
                    >
                        <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
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
                {/* Header com usuário */}
                <div className="flex items-center justify-between mb-8">
                    <div className="flex items-center space-x-3">
                        <button
                            onClick={() => router.back()}
                            className="text-gray-400 hover:text-gray-600"
                        >
                            <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
                            </svg>
                        </button>
                        <span className="text-sm text-gray-600">Capacidades</span>
                    </div>
                    <div className="flex items-center space-x-4">
                        <span className="text-sm font-medium text-gray-700">{nomeUsuario}</span>
                        <div className="w-8 h-8 bg-yellow-400 rounded-full flex items-center justify-center text-white font-bold text-sm">
                            {primeiraLetra}
                        </div>
                    </div>
                </div>

                {/* Título */}
                <div className="mb-6">
                    <h1 className="text-2xl font-semibold text-gray-900 mb-4">
                        Processo {processo.cod_edocs}
                    </h1>
                </div>

                {/* Data de atualização */}
                <div className="text-sm text-gray-500 mb-6">
                    {processo.data_hora_ultima_atualizacao && (() => {
                        const { data, hora } = formatarDataHoraCompleta(processo.data_hora_ultima_atualizacao);
                        return `Atualizado em dia ${data} às ${hora}`;
                    })()}
                </div>

                {/* Card de conteúdo */}
                <div className="bg-white rounded-lg shadow p-6">
                    <h2 className="text-base font-medium text-gray-700 mb-6 pb-3 border-b">Processo</h2>

                    <div className="space-y-6">
                        {/* Campos de informação */}
                        <div className="grid grid-cols-2 gap-6">
                            <div>
                                <label className="text-sm text-gray-600 mb-2 block">Código E-Docs</label>
                                <div className="bg-gray-100 rounded px-4 py-2 text-sm text-gray-700">
                                    {processo.cod_edocs}
                                </div>
                            </div>

                            <div>
                                <label className="text-sm text-gray-600 mb-2 block">Número do Processo Florestal</label>
                                <div className="bg-gray-100 rounded px-4 py-2 text-sm text-gray-700">
                                    {processo.num_processo_florestal}
                                </div>
                            </div>

                            <div>
                                <label className="text-sm text-gray-600 mb-2 block">Código do Empreendimento</label>
                                <div className="bg-gray-100 rounded px-4 py-2 text-sm text-gray-700">
                                    {processo.cod_empreendimento}
                                </div>
                            </div>

                            <div>
                                <label className="text-sm text-gray-600 mb-2 block">Campus</label>
                                <div className="bg-gray-100 rounded px-4 py-2 text-sm text-gray-700">
                                    {processo.nome_campus || 'Não informado'}
                                </div>
                            </div>

                            <div>
                                <label className="text-sm text-gray-600 mb-2 block">Usuário Cadastrante</label>
                                <div className="bg-gray-100 rounded px-4 py-2 text-sm text-gray-700">
                                    {processo.nome_usuario || 'Não informado'}
                                    {processo.role_usuario && (
                                        <span className="ml-2 text-xs text-gray-500">
                                            ({processo.role_usuario})
                                        </span>
                                    )}
                                </div>
                            </div>

                            {processo.motivo_notificacao && (
                                <div className="col-span-2">
                                    <label className="text-sm text-gray-600 mb-2 block">Notificação</label>
                                    <div className="bg-yellow-50 border border-yellow-200 rounded px-4 py-2 text-sm text-gray-700">
                                        {processo.motivo_notificacao}
                                    </div>
                                </div>
                            )}
                        </div>

                        {/* Seção de Análise */}
                        <div className="pt-6 border-t">
                            <h2 className="text-base font-medium text-gray-700 mb-6 pb-3 border-b">Análise</h2>

                            <div className="space-y-6">
                                <div className="grid grid-cols-2 gap-6">
                                    <div>
                                        <label className="text-sm text-gray-600 mb-2 block">
                                            Data e hora do início de análise
                                        </label>
                                        <div className="bg-gray-100 rounded px-4 py-2 text-sm text-gray-700 flex items-center">
                                            <svg className="w-4 h-4 mr-2 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                                            </svg>
                                            {processo.data_hora_inicio_analise
                                                ? new Date(processo.data_hora_inicio_analise).toLocaleDateString('pt-BR', { day: '2-digit', month: '2-digit', year: 'numeric' })
                                                : 'N/A'}
                                        </div>
                                    </div>

                                    <div>
                                        <label className="text-sm text-gray-600 mb-2 block">
                                            Data prevista do fim da análise
                                        </label>
                                        <div className="bg-gray-100 rounded px-4 py-2 text-sm text-gray-700 flex items-center">
                                            <svg className="w-4 h-4 mr-2 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                                            </svg>
                                            {processo.data_previsao_fim_analise
                                                ? new Date(processo.data_previsao_fim_analise).toLocaleDateString('pt-BR', { day: '2-digit', month: '2-digit', year: 'numeric' })
                                                : 'N/A'}
                                        </div>
                                    </div>
                                </div>

                                <div>
                                    <label className="text-sm text-gray-600 mb-2 block">
                                        Status da análise
                                    </label>
                                    <div className="bg-gray-100 rounded px-4 py-2 text-sm text-gray-400">
                                        {processo.tipo_status || 'N/A'}
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </main>
        </div>
    );
}
