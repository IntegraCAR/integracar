import { NextRequest, NextResponse } from 'next/server';
import { cookies } from 'next/headers';

export async function DELETE(
    request: NextRequest,
    { params }: { params: { cod: string } }
) {
    try {
        const cookieStore = cookies();
        const sessionId = cookieStore.get('session_id');

        if (!sessionId) {
            return NextResponse.json(
                { success: false, message: 'Não autenticado' },
                { status: 401 }
            );
        }

        const response = await fetch(`http://localhost:8000/processo/${params.cod}`, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json',
                'Cookie': `session_id=${sessionId.value}`
            }
        });

        const data = await response.json();

        if (!response.ok) {
            return NextResponse.json(data, { status: response.status });
        }

        return NextResponse.json(data);
    } catch (error) {
        console.error('Erro ao excluir processo:', error);
        return NextResponse.json(
            { success: false, message: 'Erro ao excluir processo' },
            { status: 500 }
        );
    }
}
