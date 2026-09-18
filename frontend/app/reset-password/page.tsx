'use client'

import { useState } from 'react'
import Link from 'next/link'
import { useSearchParams } from 'next/navigation'
import { Button } from '@/components/ui/button'

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

export default function ResetPasswordPage() {
  const searchParams = useSearchParams()
  const token = searchParams.get('token') || ''
  const [password, setPassword] = useState('')
  const [confirm, setConfirm] = useState('')
  const [message, setMessage] = useState('')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  const submit = async (event: React.FormEvent) => {
    event.preventDefault(); setError(''); setMessage('')
    if (password !== confirm) { setError('Passwords do not match'); return }
    setLoading(true)
    try {
      const response = await fetch(`${API_URL}/api/auth/reset-password`, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ token, password }) })
      const data = await response.json()
      if (!response.ok) throw new Error(data.detail || 'Reset link is invalid or expired')
      setMessage('Password changed successfully. You can now sign in.')
    } catch (requestError) { setError(requestError instanceof Error ? requestError.message : 'Unable to reset password') } finally { setLoading(false) }
  }

  return <main className="min-h-screen bg-gray-50 px-4 py-16"><div className="mx-auto max-w-md rounded-lg bg-white p-8 shadow"><h1 className="text-2xl font-bold text-gray-900">Choose a new password</h1>{message && <p className="mt-5 rounded bg-green-50 p-3 text-green-700">{message}</p>}{error && <p className="mt-5 rounded bg-red-50 p-3 text-red-700">{error}</p>}<form onSubmit={submit} className="mt-6 space-y-4"><input type="password" required minLength={12} maxLength={72} value={password} onChange={(event) => setPassword(event.target.value)} placeholder="New password (12+ characters)" className="w-full rounded border px-3 py-2" /><input type="password" required minLength={12} maxLength={72} value={confirm} onChange={(event) => setConfirm(event.target.value)} placeholder="Confirm new password" className="w-full rounded border px-3 py-2" /><Button type="submit" disabled={loading || !token} className="w-full">{loading ? 'Updating...' : 'Change password'}</Button></form><Link href="/login" className="mt-6 block text-center text-blue-600">Back to sign in</Link></div></main>
}