const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://127.0.0.1:8000';

export interface LoginData {
    email: string;
    senha: string;
    redirect?: string;
}

export interface LoginResponse {
    success: boolean;
    message?: string;
    redirectUrl?: string;
}

export const authService = {
    async login(data: LoginData): Promise<LoginResponse> {
        try {
            const formData = new FormData();
            formData.append('email', data.email);
            formData.append('senha', data.senha);
            if (data.redirect) {
                formData.append('redirect', data.redirect);
            }

            const response = await fetch(`${API_URL}/login`, {
                method: 'POST',
                body: formData,
                credentials: 'include',
            });

            if (!response.ok) {
                const json = await response.json();
                return {
                    success: false,
                    message: json.erro || 'Email ou senha inválidos',
                };
            }

            const json = await response.json();
            const usuario = json.usuario;
            let redirectUrl = '/';
            switch (usuario.role_usuario?.toLowerCase()) {
                case 'bolsista':
                    redirectUrl = '/bolsista';
                    break;
                case 'orientador':
                    redirectUrl = '/orientador';
                    break;
                case 'consultor':
                    redirectUrl = '/consultor';
                    break;
                case 'coordenador':
                    redirectUrl = '/coordenador';
                    break;
                case 'gestor_tecnico':
                    redirectUrl = '/gestor_tecnico';
                    break;
                case 'gestor_administrativo':
                    redirectUrl = '/gestor_administrativo';
                    break;
                default:
                    redirectUrl = '/';
            }
            return {
                success: true,
                redirectUrl,
            };
        } catch (error) {
            console.error('Erro ao fazer login:', error);
            return {
                success: false,
                message: 'Erro ao conectar com o servidor',
            };
        }
    },
};
