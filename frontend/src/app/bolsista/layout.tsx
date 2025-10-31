import React from "react"

export default function BolsistaLayout({ children }: { children: React.ReactNode }) {
    return (
        <div className="min-h-screen bg-white">
            {/* aqui você pode importar Sidebar/Topbar específicos do bolsista */}
            {children}
        </div>
    )
}
