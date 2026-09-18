'use client'

import { useEffect, useState } from 'react'
import Link from 'next/link'
import { useRouter } from 'next/navigation'
import { UserPlus, Check, ArrowLeft } from 'lucide-react'
import { authService } from '@/lib/auth'
import { Button } from '@/components/ui/button'

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

type Person = { id: number; email: string; role: string; connection_status?: string }

export default function NetworkPage() {
  const router = useRouter()
  const [people, setPeople] = useState<Person[]>([])
  const [message, setMessage] = useState('')

  useEffect(() => {
    if (!authService.isAuthenticated()) {
      router.push('/login')
      return
    }
    fetch(`${API_URL}/api/network/people`, {
      headers: { Authorization: `Bearer ${authService.getAccessToken()}` },
      cache: 'no-store',
    }).then(async (response) => {
      if (response.ok) setPeople(await response.json())
    })
  }, [router])

  const connect = async (userId: number) => {
    const response = await fetch(`${API_URL}/api/network/connections`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${authService.getAccessToken()}`,
      },
      body: JSON.stringify({ user_id: userId }),
    })
    const data = await response.json()
    if (!response.ok) {
      setMessage(data.detail || 'Unable to send request')
      return
    }
    setMessage('Connection request sent')
    setPeople((current) => current.map((person) => person.id === userId ? { ...person, connection_status: 'pending' } : person))
  }

  return (
    <main className="min-h-screen bg-gray-50">
      <header className="bg-white border-b border-gray-200">
        <div className="container mx-auto flex items-center justify-between px-4 py-4">
          <Link href="/dashboard" className="flex items-center gap-2 text-blue-600 font-bold">
            <ArrowLeft className="h-4 w-4" /> Dashboard
          </Link>
          <h1 className="text-xl font-semibold text-gray-900">Professional Network</h1>
          <span className="w-20" />
        </div>
      </header>
      <div className="container mx-auto max-w-4xl px-4 py-8">
        <h2 className="text-2xl font-bold text-gray-900">Meet candidates and recruiters</h2>
        <p className="mt-2 text-gray-600">Build your network with people working toward their next opportunity.</p>
        {message && <p className="mt-4 rounded bg-blue-50 px-4 py-3 text-blue-700">{message}</p>}
        <div className="mt-6 grid gap-4 md:grid-cols-2">
          {people.map((person) => (
            <div key={person.id} className="flex items-center justify-between rounded-lg bg-white p-5 shadow">
              <div>
                <p className="font-semibold text-gray-900">{person.email.split('@')[0]}</p>
                <p className="text-sm capitalize text-gray-500">{person.role}</p>
              </div>
              {person.connection_status === 'accepted' ? (
                <span className="flex items-center gap-1 text-sm text-green-600"><Check className="h-4 w-4" /> Connected</span>
              ) : person.connection_status === 'pending' ? (
                <span className="text-sm text-gray-500">Request pending</span>
              ) : (
                <Button size="sm" onClick={() => connect(person.id)}><UserPlus className="mr-2 h-4 w-4" /> Connect</Button>
              )}
            </div>
          ))}
        </div>
        {people.length === 0 && <p className="mt-8 text-gray-600">No other members are available yet.</p>}
      </div>
    </main>
  )
}
