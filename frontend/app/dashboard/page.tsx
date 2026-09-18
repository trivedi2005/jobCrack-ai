'use client'

import { useEffect, useState } from 'react'
import { useRouter } from 'next/navigation'
import Link from 'next/link'
import { authService } from '@/lib/auth'
import { Briefcase, Target, BookOpen, FileText, Calendar, Users, LogOut } from 'lucide-react'
import { Button } from '@/components/ui/button'

export default function DashboardPage() {
  const router = useRouter()
  const [user, setUser] = useState<any>(null)
  const [summary, setSummary] = useState({
    career_readiness: 0,
    applications: 0,
    interviews: 0,
    practice_score: 0,
    resume_count: 0,
    tasks: [] as Array<{ id: number; title: string; status: string; estimated_hours?: number }>,
  })
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    if (!authService.isAuthenticated()) {
      router.push('/login')
      return
    }

    // Fetch user data
    fetchUserData()
  }, [router])

  const fetchUserData = async () => {
    const headers = {
      'Authorization': `Bearer ${authService.getAccessToken()}`,
      'Cache-Control': 'no-cache',
    }
    try {
      setSummary({
        career_readiness: 0,
        applications: 0,
        interviews: 0,
        practice_score: 0,
        resume_count: 0,
        tasks: [],
      })
      const response = await fetch('http://localhost:8000/api/users/me', {
        headers,
        cache: 'no-store',
      })
      if (response.status === 401) {
        authService.clearTokens()
        router.push('/login')
        return
      }
      if (!response.ok) throw new Error('Unable to load account')
      const userData = await response.json()
      setUser(userData)
      const summaryResponse = await fetch('http://localhost:8000/api/users/me/dashboard-summary', {
        headers,
        cache: 'no-store',
      })
      if (summaryResponse.status === 401) {
        authService.clearTokens()
        router.push('/login')
        return
      }
      if (!summaryResponse.ok) throw new Error('Unable to load dashboard summary')
      setSummary(await summaryResponse.json())
    } catch (error) {
      console.error('Failed to fetch user data:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleLogout = () => {
    authService.clearTokens()
    router.push('/')
  }

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-gray-600">Loading...</div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white border-b border-gray-200">
        <div className="container mx-auto px-4 py-4 flex justify-between items-center">
          <div className="flex items-center space-x-4">
            <Link href="/" className="text-2xl font-bold text-blue-600">
              JobCrack AI
            </Link>
            <span className="text-gray-600">|</span>
            <span className="text-gray-900 font-medium">Dashboard</span>
          </div>
          <div className="flex items-center space-x-4">
            <span className="text-gray-600">
              {user?.email}
            </span>
            <Button
              variant="ghost"
              size="icon"
              onClick={handleLogout}
            >
              <LogOut className="w-5 h-5" />
            </Button>
          </div>
        </div>
      </header>

      <div className="container mx-auto px-4 py-8">
        {/* Welcome Section */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">
            Good morning, {user?.email?.split('@')[0]} 👋
          </h1>
          <p className="text-gray-600">
            Ready to crack your dream job today?
          </p>
        </div>

        {/* Quick Stats */}
        <div className="grid md:grid-cols-4 gap-6 mb-8">
          <div className="bg-white rounded-lg shadow p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-600 text-sm">Career Readiness</p>
                <p className="text-3xl font-bold text-gray-900">{summary.career_readiness}/100</p>
              </div>
              <Target className="w-12 h-12 text-blue-600" />
            </div>
          </div>
          <div className="bg-white rounded-lg shadow p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-600 text-sm">Applications</p>
                <p className="text-3xl font-bold text-gray-900">{summary.applications}</p>
              </div>
              <Briefcase className="w-12 h-12 text-blue-600" />
            </div>
          </div>
          <div className="bg-white rounded-lg shadow p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-600 text-sm">Interviews</p>
                <p className="text-3xl font-bold text-gray-900">{summary.interviews}</p>
              </div>
              <Calendar className="w-12 h-12 text-blue-600" />
            </div>
          </div>
          <div className="bg-white rounded-lg shadow p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-600 text-sm">Practice Score</p>
                <p className="text-3xl font-bold text-gray-900">{summary.practice_score}%</p>
              </div>
              <BookOpen className="w-12 h-12 text-blue-600" />
            </div>
          </div>
        </div>

        {/* Quick Actions */}
        <div className="mb-8">
          <h2 className="text-xl font-semibold text-gray-900 mb-4">Quick Actions</h2>
          <div className="grid md:grid-cols-4 gap-4">
            <Link href="/jobs">
              <div className="bg-white rounded-lg shadow p-6 hover:shadow-md transition cursor-pointer">
                <Briefcase className="w-8 h-8 text-blue-600 mb-3" />
                <h3 className="font-semibold text-gray-900 mb-2">Browse Jobs</h3>
                <p className="text-gray-600 text-sm">Find jobs that match your profile</p>
              </div>
            </Link>
            <Link href="/resume">
              <div className="bg-white rounded-lg shadow p-6 hover:shadow-md transition cursor-pointer">
                <FileText className="w-8 h-8 text-blue-600 mb-3" />
                <h3 className="font-semibold text-gray-900 mb-2">Optimize Resume</h3>
                <p className="text-gray-600 text-sm">Analyze and improve your resume</p>
              </div>
            </Link>
            <Link href="/preparation">
              <div className="bg-white rounded-lg shadow p-6 hover:shadow-md transition cursor-pointer">
                <BookOpen className="w-8 h-8 text-blue-600 mb-3" />
                <h3 className="font-semibold text-gray-900 mb-2">Start Preparation</h3>
                <p className="text-gray-600 text-sm">Begin your interview preparation</p>
              </div>
            </Link>
            <Link href="/network">
              <div className="bg-white rounded-lg shadow p-6 hover:shadow-md transition cursor-pointer">
                <Users className="w-8 h-8 text-blue-600 mb-3" />
                <h3 className="font-semibold text-gray-900 mb-2">Grow Network</h3>
                <p className="text-gray-600 text-sm">Connect with candidates and recruiters</p>
              </div>
            </Link>
          </div>
        </div>

        {/* Today's Tasks */}
        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-xl font-semibold text-gray-900 mb-4">Today's Preparation</h2>
          <div className="space-y-3">
            {summary.tasks.length === 0 ? (
              <p className="text-gray-600">No preparation tasks yet. Generate a plan to get started.</p>
            ) : summary.tasks.map((task) => (
              <div key={task.id} className="flex items-center justify-between p-3 bg-gray-50 rounded">
                <span className="text-gray-700">{task.title}</span>
                <span className="text-sm text-gray-500">{task.estimated_hours || 1}h</span>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  )
}
