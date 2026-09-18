'use client'

import { useState } from 'react'
import Link from 'next/link'
import { Button } from '@/components/ui/button'

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

export default function ForgotPasswordPage() {
  const [email, setEmail] = useState('')
  const [message, setMessage] = useState('')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  const submit = async (event: React.FormEvent) => {
    event.preventDefault()
    setLoading(true); setMessage(''); setError('')
    try {
      const response = await fetch(`${API_URL}/api/auth/forgot-password`, {
        method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ email }),
      })
      const data = await response.json()
      if (!response.ok) throw new Error(data.detail || 'Unable to request reset')
      setMessage(data.message)
    } catch (requestError) {
      setError(requestError instanceof Error ? requestError.message : 'Unable to request reset')
    } finally { setLoading(false) }
  }

  return <main className="min-h-screen bg-gray-50 px-4 py-16"><div className="mx-auto max-w-md rounded-lg bg-white p-8 shadow"><h1 className="text-2xl font-bold text-gray-900">Reset your password</h1><p className="mt-2 text-gray-600">Enter your email and we will send a secure reset link.</p>{message && <p className="mt-5 rounded bg-green-50 p-3 text-green-700">{message}</p>}{error && <p className="mt-5 rounded bg-red-50 p-3 text-red-700">{error}</p>}<form onSubmit={submit} className="mt-6 space-y-4"><input type="email" required value={email} onChange={(event) => setEmail(event.target.value)} placeholder="you@example.com" className="w-full rounded border px-3 py-2" /><Button type="submit" disabled={loading} className="w-full">{loading ? 'Sending...' : 'Send reset link'}</Button></form><Link href="/login" className="mt-6 block text-center text-blue-600">Back to sign in</Link></div></main>
}