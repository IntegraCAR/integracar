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
                credentials: 'include', // Para incluir cookies na requisição
            });

            // Trata redirecionamento manualmente
            if (response.status === 303) {
                const location = response.headers.get("Location");
                if (location) {
                    window.location.href = location;
                    return {
                        success: true,
                        redirectUrl: location,
                    };
                }
            }

            if (response.redirected) {
                return {
                    success: true,
                    redirectUrl: response.url,
                };
            }

            if (!response.ok) {
                const text = await response.text();
                return {
                    success: false,
                    message: 'Email ou senha inválidos',
                };
            }

            return {
                success: true,
                redirectUrl: response.url,
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
