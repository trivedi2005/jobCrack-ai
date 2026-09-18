'use client'

import { useState } from 'react'
import { useRouter } from 'next/navigation'
import Link from 'next/link'
import { authService } from '@/lib/auth'
import { Button } from '@/components/ui/button'

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

export default function PostJobPage() {
  const router = useRouter()
  const [form, setForm] = useState({ company_name: '', title: '', description: '', location: '', work_mode: 'remote', job_type: 'full-time', experience_level: 'entry' })
  const [error, setError] = useState('')
  const [saving, setSaving] = useState(false)
  const update = (event: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>) => setForm({ ...form, [event.target.name]: event.target.value })
  const submit = async (event: React.FormEvent) => {
    event.preventDefault(); setSaving(true); setError('')
    const response = await fetch(`${API_URL}/api/jobs/post`, { method: 'POST', headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${authService.getAccessToken()}` }, body: JSON.stringify(form) })
    if (!response.ok) { const data = await response.json(); setError(data.detail || 'Unable to post job'); setSaving(false); return }
    router.push('/jobs')
  }
  return <main className="min-h-screen bg-gray-50 px-4 py-10"><div className="mx-auto max-w-2xl rounded-lg bg-white p-8 shadow"><Link href="/jobs" className="text-blue-600">Back to jobs</Link><h1 className="mt-4 text-2xl font-bold">Post a daily hiring opportunity</h1><p className="mt-2 text-gray-600">Recruiters can publish up to five jobs per day.</p>{error && <p className="mt-4 rounded bg-red-50 p-3 text-red-700">{error}</p>}<form onSubmit={submit} className="mt-6 space-y-4">{[['company_name','Company name'],['title','Job title'],['location','Location']].map(([name,label]) => <input key={name} name={name} value={form[name as keyof typeof form]} onChange={update} placeholder={label} required className="w-full rounded border px-3 py-2" />)}<textarea name="description" value={form.description} onChange={update} placeholder="Describe the role, responsibilities, and requirements" required className="min-h-32 w-full rounded border px-3 py-2" /><select name="work_mode" value={form.work_mode} onChange={update} className="w-full rounded border px-3 py-2"><option value="remote">Remote</option><option value="hybrid">Hybrid</option><option value="onsite">On-site</option></select><Button type="submit" disabled={saving}>{saving ? 'Posting...' : 'Post job'}</Button></form></div></main>
}