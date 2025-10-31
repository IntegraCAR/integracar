import React from "react"

export default function CoordenadorLayout({ children }: { children: React.ReactNode }) {
    return (
        <div className="min-h-screen bg-gray-50">
            {children}
        </div>
    )
}
