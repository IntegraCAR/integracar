import { NextRequest, NextResponse } from 'next/server';

export async function GET(request: NextRequest) {
    try {
        const sessionCookie = request.cookies.get('session');

        if (!sessionCookie) {
            return NextResponse.json(
                { redirect: '/login' },
                { status: 401 }
            );
        }

        const response = await fetch('http://localhost:8000/coordenador/graficos', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Cookie': `session=${sessionCookie.value}`
            }
        });

        const data = await response.json();

        if (!response.ok) {
            return NextResponse.json(data, { status: response.status });
        }

        return NextResponse.json(data);
    } catch (error) {
        console.error('Erro ao buscar dados dos gráficos:', error);
        return NextResponse.json(
            { error: 'Erro ao buscar dados dos gráficos' },
            { status: 500 }
        );
    }
}