import React from "react"

export default function OrientadorLayout({ children }: { children: React.ReactNode }) {
    return (
        <div className="min-h-screen bg-white">
            {/* layout do orientador */}
            {children}
        </div>
    )
}
