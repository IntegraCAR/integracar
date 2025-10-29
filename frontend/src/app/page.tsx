"use client"

import { useState } from "react"
import Image from "next/image"
import { Eye, EyeOff } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Checkbox } from "@/components/ui/checkbox"
import { authService } from "@/lib/auth"

export default function LoginPage() {
    const [email, setEmail] = useState("")
    const [senha, setSenha] = useState("")
    const [mostrarSenha, setMostrarSenha] = useState(false)
    const [manterConectado, setManterConectado] = useState(false)
    const [erro, setErro] = useState("")
    const [carregando, setCarregando] = useState(false)

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault()
        setErro("")
        setCarregando(true)

        try {
            const response = await authService.login({ email, senha })

            if (response.success && response.redirectUrl) {
                // Redireciona para a URL fornecida pelo backend
                window.location.href = response.redirectUrl
            } else {
                setErro(response.message || "Erro ao fazer login")
            }
        } catch (error) {
            setErro("Erro ao conectar com o servidor")
        } finally {
            setCarregando(false)
        }
    }

    return (
        <div className="flex min-h-screen">
            {/* Lado Esquerdo - Branco com Logo */}
            <div className="hidden lg:flex lg:w-1/2 bg-white items-center justify-center p-12">
                <div className="max-w-sm w-full">
                    <div className="space-y-4 mb-8">
                        <h1 className="text-3xl font-bold text-gray-900">IntegraCAR</h1>
                        <p className="text-gray-600 text-sm">Não possui uma conta?</p>
                        <Button
                            variant="outline"
                            className="bg-[#3B82F6] text-white hover:bg-[#2563EB] border-none px-6 py-2 text-sm rounded-md"
                        >
                            Criar uma agora
                        </Button>
                    </div>

                    {/* Logo Ilustração */}
                    <div className="flex justify-center mt-4">
                        <Image
                            src="/logo_login.png"
                            alt="IntegraCAR Logo"
                            width={420}
                            height={420}
                            className="object-contain"
                            priority
                        />
                    </div>
                </div>
            </div>

            {/* Lado Direito - Azul com Formulário */}
            <div className="w-full lg:w-1/2 bg-[#3B7EC2] flex items-center justify-center p-8">
                <div className="max-w-sm w-full space-y-6">
                    <div className="text-center space-y-2">
                        <h2 className="text-2xl font-bold text-white">
                            Bem vindo de volta!
                        </h2>
                        <p className="text-white/90 text-sm">
                            Preencha os dados abaixo e acesse sua conta
                        </p>
                    </div>

                    <form onSubmit={handleSubmit} className="space-y-4">
                        {/* Campo de E-mail */}
                        <div className="space-y-1">
                            <Label htmlFor="email" className="text-white text-xs font-normal">
                                E-mail
                            </Label>
                            <Input
                                id="email"
                                type="email"
                                placeholder="E-mail"
                                value={email}
                                onChange={(e) => setEmail(e.target.value)}
                                required
                                className="bg-white border-none text-gray-900 placeholder:text-gray-400 h-10 text-sm"
                            />
                        </div>

                        {/* Campo de Senha */}
                        <div className="space-y-1">
                            <Label htmlFor="senha" className="text-white text-xs font-normal">
                                Senha
                            </Label>
                            <div className="relative">
                                <Input
                                    id="senha"
                                    type={mostrarSenha ? "text" : "password"}
                                    placeholder="Senha"
                                    value={senha}
                                    onChange={(e) => setSenha(e.target.value)}
                                    required
                                    className="bg-white border-none text-gray-900 placeholder:text-gray-400 h-10 text-sm pr-10"
                                />
                                <button
                                    type="button"
                                    onClick={() => setMostrarSenha(!mostrarSenha)}
                                    className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400 hover:text-gray-600"
                                >
                                    {mostrarSenha ? (
                                        <EyeOff className="h-4 w-4" />
                                    ) : (
                                        <Eye className="h-4 w-4" />
                                    )}
                                </button>
                            </div>
                        </div>

                        {/* Esqueceu a senha */}
                        <div className="flex items-center justify-end">
                            <a
                                href="#"
                                className="text-xs text-white hover:text-white/90 underline"
                            >
                                Esqueceu sua senha?
                            </a>
                        </div>

                        {/* Mensagem de Erro */}
                        {erro && (
                            <div className="bg-red-500/20 border border-red-500/50 text-white px-3 py-2 rounded-md text-xs">
                                {erro}
                            </div>
                        )}

                        {/* Botão de Acessar */}
                        <Button
                            type="submit"
                            disabled={carregando}
                            className="w-full bg-white text-[#3B7EC2] hover:bg-gray-100 font-medium h-10 text-sm"
                        >
                            {carregando ? "Acessando..." : "Acessar"}
                        </Button>

                        {/* Manter Conectado */}
                        <div className="flex items-center space-x-2 pt-2">
                            <Checkbox
                                id="manter-conectado"
                                checked={manterConectado}
                                onCheckedChange={(checked) =>
                                    setManterConectado(checked as boolean)
                                }
                                className="border-white data-[state=checked]:bg-white data-[state=checked]:text-[#3B7EC2] h-4 w-4"
                            />
                            <Label
                                htmlFor="manter-conectado"
                                className="text-xs text-white cursor-pointer font-normal"
                            >
                                Permanecer conectado na plataforma
                            </Label>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    )
}
