import { apiFetch } from "@/lib/api"

export async function getContagemStatus() {
    return apiFetch(`/api/analises/counts`)
        .then((data) => data.contagem)
}

export async function getUltimas(limit = 10) {
    return apiFetch(`/api/analises/recent?limit=${limit}`)
        .then((data) => data.ultimas)
}
