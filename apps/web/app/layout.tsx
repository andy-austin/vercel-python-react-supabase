import type { Metadata } from 'next'

export const metadata: Metadata = {
  title: 'Vercel Python React Supabase',
  description: 'Full-stack application with Next.js, Python FastAPI, and Supabase',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  )
}