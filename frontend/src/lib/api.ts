export async function apiFetch(path: string, opts: RequestInit = {}) {
    const base = process.env.NEXT_PUBLIC_API_URL || "/api"
    const res = await fetch(`${base}${path}`, {
        credentials: "include",
        headers: { "Content-Type": "application/json" },
        ...opts,
    })
    if (!res.ok) throw new Error(`API error ${res.status}`)
    return res.json()
}
