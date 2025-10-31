import { redirect } from "next/navigation"

export default function RootPage() {
    // redirect root to login route
    redirect("/login")
}
