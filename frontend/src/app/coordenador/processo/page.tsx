'use client';

import { useRouter, useSearchParams } from 'next/navigation';
import { useEffect, useState } from 'react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';

const STATUS_LIST = [
    { cod_status: 1, tipo_status: 'Análise iniciada – ainda sem parecer' },
    { cod_status: 2, tipo_status: 'Aprovado – título emitido, mas não entregue' },
    { cod_status: 3, tipo_status: 'Aprovado – título emitido e entregue' },
    { cod_status: 4, tipo_status: 'Reprovado – notificação ao proprietário/possuidor pendente' },
    { cod_status: 5, tipo_status: 'Reprovado – notificação ao proprietário/possuidor realizada' }
];

export default function ProcessoPage() {
    const router = useRouter();
    const searchParams = useSearchParams();
    const cod = searchParams.get('cod');

    const [processo, setProcesso] = useState<any>(null);
    const [usuario, setUsuario] = useState<any>(null);
    const [loading, setLoading] = useState(true);
    const [editando, setEditando] = useState(false);
    const [mostrarNotificacao, setMostrarNotificacao] = useState(false);
    const [motivoNotificacao, setMotivoNotificacao] = useState('');
    const [showSuccessModal, setShowSuccessModal] = useState(false);
    const [showErrorModal, setShowErrorModal] = useState(false);
    const [showDeleteModal, setShowDeleteModal] = useState(false);
    const [errorMessage, setErrorMessage] = useState('');
    const [formData, setFormData] = useState({
        data_hora_inicio_analise: '',
        data_previsao_fim_analise: '',
        cod_status: 0
    });

    useEffect(() => {
        carregarDados();
    }, [cod]);

    const carregarDados = async () => {
        try {
            // Carregar dados do usuário
            const userRes = await fetch('/api/coordenador');
            const userData = await userRes.json();
            setUsuario(userData.usuario);

            // Carregar dados do processo
            if (cod) {
                const response = await fetch(`/api/processo/${cod}`);
                const data = await response.json();

                if (data.analises && data.analises.length > 0) {
                    const proc = data.analises[0];
                    setProcesso(proc);

                    // Formatar as datas para datetime-local input
                    const formatarData = (dataStr: string) => {
                        if (!dataStr) return '';
                        const data = new Date(dataStr);
                        const ano = data.getFullYear();
                        const mes = String(data.getMonth() + 1).padStart(2, '0');
                        const dia = String(data.getDate()).padStart(2, '0');
                        const horas = String(data.getHours()).padStart(2, '0');
                        const minutos = String(data.getMinutes()).padStart(2, '0');
                        return `${ano}-${mes}-${dia}T${horas}:${minutos}`;
                    };

                    setFormData({
                        data_hora_inicio_analise: formatarData(proc.data_hora_inicio_analise),
                        data_previsao_fim_analise: formatarData(proc.data_previsao_fim_analise),
                        cod_status: proc.cod_status || 1
                    });
                }
            }
        } catch (error) {
            console.error('Erro ao carregar dados:', error);
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

    const handleSalvar = async () => {
        try {
            const response = await fetch(`/api/processo/${cod}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(formData)
            });

            const data = await response.json();

            if (response.ok && data.success) {
                setShowSuccessModal(true);
                setEditando(false);
                await carregarDados();
            } else {
                setErrorMessage(data.message || 'Erro ao salvar alterações');
                setShowErrorModal(true);
            }
        } catch (error) {
            setErrorMessage('Erro ao salvar alterações');
            setShowErrorModal(true);
        }
    };

    const handleCancelar = () => {
        setEditando(false);
        if (processo) {
            const formatarData = (dataStr: string) => {
                if (!dataStr) return '';
                const data = new Date(dataStr);
                const ano = data.getFullYear();
                const mes = String(data.getMonth() + 1).padStart(2, '0');
                const dia = String(data.getDate()).padStart(2, '0');
                const horas = String(data.getHours()).padStart(2, '0');
                const minutos = String(data.getMinutes()).padStart(2, '0');
                return `${ano}-${mes}-${dia}T${horas}:${minutos}`;
            };

            setFormData({
                data_hora_inicio_analise: formatarData(processo.data_hora_inicio_analise),
                data_previsao_fim_analise: formatarData(processo.data_previsao_fim_analise),
                cod_status: processo.cod_status || 1
            });
        }
    };

    const handleAdicionarNotificacao = async () => {
        if (!motivoNotificacao.trim()) {
            setErrorMessage('Por favor, informe o motivo da notificação');
            setShowErrorModal(true);
            return;
        }

        try {
            const response = await fetch(`/api/processo/${cod}/notificacao`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ motivo_notificacao: motivoNotificacao })
            });

            const data = await response.json();

            if (response.ok && data.success) {
                setShowSuccessModal(true);
                setMostrarNotificacao(false);
                setMotivoNotificacao('');
                await carregarDados();
            } else {
                setErrorMessage(data.message || 'Erro ao adicionar notificação');
                setShowErrorModal(true);
            }
        } catch (error) {
            setErrorMessage('Erro ao adicionar notificação');
            setShowErrorModal(true);
        }
    };

    const handleExcluirProcesso = async () => {
        try {
            const response = await fetch(`/api/processo/${cod}`, {
                method: 'DELETE',
                headers: {
                    'Content-Type': 'application/json',
                }
            });

            const data = await response.json();

            if (response.ok && data.success) {
                setShowDeleteModal(false);
                setShowSuccessModal(true);
                // Redirecionar para a lista de processos após 2 segundos
                setTimeout(() => {
                    router.push('/coordenador');
                }, 2000);
            } else {
                setShowDeleteModal(false);
                setErrorMessage(data.message || 'Erro ao excluir processo');
                setShowErrorModal(true);
            }
        } catch (error) {
            setShowDeleteModal(false);
            setErrorMessage('Erro ao excluir processo');
            setShowErrorModal(true);
        }
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
                        onClick={() => router.push('/coordenador')}
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
                        <div className="w-8 h-8 bg-green-400 rounded-full flex items-center justify-center text-white font-bold text-sm">
                            {primeiraLetra}
                        </div>
                    </div>
                </div>

                {/* Título e botões */}
                <div className="mb-6">
                    <h1 className="text-2xl font-semibold text-gray-900 mb-4">
                        Processo {processo.cod_edocs}
                    </h1>
                    <div className="flex gap-3">
                        <Button
                            onClick={() => setEditando(true)}
                            disabled={editando}
                            className="bg-[#2563EB] hover:bg-[#1D4ED8] text-white px-6"
                        >
                            Atualizar Status
                        </Button>
                        <Button
                            onClick={() => setMostrarNotificacao(!mostrarNotificacao)}
                            variant="outline"
                            className="border-[#2563EB] text-[#2563EB] hover:bg-blue-50 px-6"
                        >
                            {mostrarNotificacao ? 'Cancelar' : 'Adicionar Notificação'}
                        </Button>
                        <Button
                            onClick={() => setShowDeleteModal(true)}
                            variant="outline"
                            className="border-red-600 text-red-600 hover:bg-red-50 px-6"
                        >
                            Excluir Processo
                        </Button>
                    </div>
                </div>

                {/* Formulário de Notificação */}
                {mostrarNotificacao && (
                    <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-6 mb-6">
                        <h3 className="text-lg font-semibold text-gray-900 mb-4">Nova Notificação</h3>
                        <div className="space-y-4">
                            <div>
                                <Label className="text-sm text-gray-600 mb-2 block">
                                    Motivo da Notificação
                                </Label>
                                <textarea
                                    value={motivoNotificacao}
                                    onChange={(e) => setMotivoNotificacao(e.target.value)}
                                    className="w-full px-4 py-2 text-sm border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                                    rows={4}
                                    placeholder="Descreva o motivo da notificação..."
                                />
                            </div>
                            <div className="flex gap-3">
                                <Button
                                    onClick={handleAdicionarNotificacao}
                                    className="bg-[#2563EB] hover:bg-[#1D4ED8] text-white px-6"
                                >
                                    Salvar Notificação
                                </Button>
                                <Button
                                    onClick={() => {
                                        setMostrarNotificacao(false);
                                        setMotivoNotificacao('');
                                    }}
                                    variant="outline"
                                    className="px-6"
                                >
                                    Cancelar
                                </Button>
                            </div>
                        </div>
                    </div>
                )}

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
                                <Label className="text-sm text-gray-600 mb-2 block">Código E-Docs</Label>
                                <div className="bg-gray-100 rounded px-4 py-2 text-sm text-gray-700">
                                    {processo.cod_edocs}
                                </div>
                            </div>

                            <div>
                                <Label className="text-sm text-gray-600 mb-2 block">Número do Processo Florestal</Label>
                                <div className="bg-gray-100 rounded px-4 py-2 text-sm text-gray-700">
                                    {processo.num_processo_florestal}
                                </div>
                            </div>

                            <div>
                                <Label className="text-sm text-gray-600 mb-2 block">Código do Empreendimento</Label>
                                <div className="bg-gray-100 rounded px-4 py-2 text-sm text-gray-700">
                                    {processo.cod_empreendimento}
                                </div>
                            </div>

                            <div>
                                <Label className="text-sm text-gray-600 mb-2 block">Campus</Label>
                                <div className="bg-gray-100 rounded px-4 py-2 text-sm text-gray-700">
                                    {processo.nome_campus || 'Não informado'}
                                </div>
                            </div>

                            <div>
                                <Label className="text-sm text-gray-600 mb-2 block">Usuário Cadastrante</Label>
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
                                    <Label className="text-sm text-gray-600 mb-2 block">Notificação</Label>
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
                                        <Label className="text-sm text-gray-600 mb-2 block">
                                            Data e hora do início de análise
                                        </Label>
                                        {editando ? (
                                            <Input
                                                type="date"
                                                value={formData.data_hora_inicio_analise.split('T')[0]}
                                                onChange={(e) => setFormData({ ...formData, data_hora_inicio_analise: e.target.value + 'T00:00' })}
                                                className="text-sm"
                                            />
                                        ) : (
                                            <div className="bg-gray-100 rounded px-4 py-2 text-sm text-gray-700 flex items-center">
                                                <svg className="w-4 h-4 mr-2 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                                                </svg>
                                                {processo.data_hora_inicio_analise
                                                    ? new Date(processo.data_hora_inicio_analise).toLocaleDateString('pt-BR', { day: '2-digit', month: '2-digit', year: 'numeric' })
                                                    : '10/06/2025'}
                                            </div>
                                        )}
                                    </div>

                                    <div>
                                        <Label className="text-sm text-gray-600 mb-2 block">
                                            Data prevista do fim da análise
                                        </Label>
                                        {editando ? (
                                            <Input
                                                type="date"
                                                value={formData.data_previsao_fim_analise.split('T')[0]}
                                                onChange={(e) => setFormData({ ...formData, data_previsao_fim_analise: e.target.value + 'T00:00' })}
                                                className="text-sm"
                                            />
                                        ) : (
                                            <div className="bg-gray-100 rounded px-4 py-2 text-sm text-gray-700 flex items-center">
                                                <svg className="w-4 h-4 mr-2 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                                                </svg>
                                                {processo.data_previsao_fim_analise
                                                    ? new Date(processo.data_previsao_fim_analise).toLocaleDateString('pt-BR', { day: '2-digit', month: '2-digit', year: 'numeric' })
                                                    : '20/07/2025'}
                                            </div>
                                        )}
                                    </div>
                                </div>

                                <div>
                                    <Label className="text-sm text-gray-600 mb-2 block">
                                        Status da análise
                                    </Label>
                                    {editando ? (
                                        <select
                                            value={formData.cod_status}
                                            onChange={(e) => setFormData({ ...formData, cod_status: parseInt(e.target.value) })}
                                            className="w-full px-4 py-2 text-sm border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                                        >
                                            <option value={0}>Selecione um status</option>
                                            {STATUS_LIST.map((status) => (
                                                <option key={status.cod_status} value={status.cod_status}>
                                                    {status.tipo_status}
                                                </option>
                                            ))}
                                        </select>
                                    ) : (
                                        <div className="bg-gray-100 rounded px-4 py-2 text-sm text-gray-400">
                                            {processo.tipo_status}
                                        </div>
                                    )}
                                </div>
                            </div>
                        </div>

                        {/* Botões de ação */}
                        {editando && (
                            <div className="flex gap-3 pt-6">
                                <Button
                                    onClick={handleSalvar}
                                    className="bg-[#06B6D4] hover:bg-[#0891B2] text-white px-8"
                                >
                                    Atualizar
                                </Button>
                                <Button
                                    onClick={handleCancelar}
                                    variant="outline"
                                    className="px-8"
                                >
                                    Cancelar
                                </Button>
                            </div>
                        )}
                    </div>
                </div>
            </main>

            {/* Modal de Confirmação de Exclusão */}
            {showDeleteModal && (
                <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
                    <div className="bg-white rounded-lg shadow-xl p-8 max-w-md w-full mx-4">
                        <div className="flex flex-col items-center text-center">
                            <div className="w-16 h-16 bg-red-100 rounded-full flex items-center justify-center mb-4">
                                <svg className="w-8 h-8 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
                                </svg>
                            </div>
                            <h3 className="text-xl font-semibold text-gray-900 mb-2">
                                Confirmar Exclusão
                            </h3>
                            <p className="text-gray-600 mb-6">
                                Tem certeza que deseja excluir este processo? Esta ação não pode ser desfeita.
                            </p>
                            <div className="flex gap-3 w-full">
                                <Button
                                    onClick={handleExcluirProcesso}
                                    className="flex-1 bg-red-600 hover:bg-red-700 text-white"
                                >
                                    Sim, Excluir
                                </Button>
                                <Button
                                    onClick={() => setShowDeleteModal(false)}
                                    variant="outline"
                                    className="flex-1"
                                >
                                    Cancelar
                                </Button>
                            </div>
                        </div>
                    </div>
                </div>
            )}

            {/* Modal de Sucesso */}
            {showSuccessModal && (
                <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
                    <div className="bg-white rounded-lg shadow-xl p-8 max-w-md w-full mx-4 animate-in fade-in zoom-in duration-200">
                        <div className="flex flex-col items-center text-center">
                            <div className="w-16 h-16 bg-green-100 rounded-full flex items-center justify-center mb-4">
                                <svg className="w-8 h-8 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                                </svg>
                            </div>
                            <h3 className="text-xl font-semibold text-gray-900 mb-2">
                                Sucesso!
                            </h3>
                            <p className="text-gray-600 mb-6">
                                As alterações foram salvas com sucesso.
                            </p>
                            <Button
                                onClick={() => setShowSuccessModal(false)}
                                className="bg-green-600 hover:bg-green-700 text-white px-8"
                            >
                                OK
                            </Button>
                        </div>
                    </div>
                </div>
            )}

            {/* Modal de Erro */}
            {showErrorModal && (
                <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
                    <div className="bg-white rounded-lg shadow-xl p-8 max-w-md w-full mx-4 animate-in fade-in zoom-in duration-200">
                        <div className="flex flex-col items-center text-center">
                            <div className="w-16 h-16 bg-red-100 rounded-full flex items-center justify-center mb-4">
                                <svg className="w-8 h-8 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                                </svg>
                            </div>
                            <h3 className="text-xl font-semibold text-gray-900 mb-2">
                                Erro
                            </h3>
                            <p className="text-gray-600 mb-6">
                                {errorMessage}
                            </p>
                            <Button
                                onClick={() => setShowErrorModal(false)}
                                className="bg-red-600 hover:bg-red-700 text-white px-8"
                            >
                                Fechar
                            </Button>
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
}
