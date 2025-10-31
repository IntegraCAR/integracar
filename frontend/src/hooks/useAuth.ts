"use client"

import { useEffect, useState } from "react"
import { useRouter } from "next/navigation"

export function useAuth(requiredRole?: string) {
    const [loading, setLoading] = useState(true)
    const [user, setUser] = useState<any>(null)
    const router = useRouter()

    useEffect(() => {
        let mounted = true
        async function load() {
            try {
                const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000"}/api/session`, {
                    credentials: "include",
                })
                if (!res.ok) {
                    router.push("/login")
                    return
                }
                const data = await res.json()
                if (mounted) setUser(data.user)
                if (requiredRole && data.user?.role_usuario !== requiredRole) {
                    router.push("/")
                }
            } catch (err) {
                router.push("/login")
            } finally {
                if (mounted) setLoading(false)
            }
        }
        load()
        return () => { mounted = false }
    }, [requiredRole, router])

    return { user, loading }
}
