'use client'

import { useEffect, useState } from 'react'
import { useRouter } from 'next/navigation'
import Link from 'next/link'
import { authService } from '@/lib/auth'
import { Target, BookOpen, CheckCircle, Clock, Play } from 'lucide-react'
import { Button } from '@/components/ui/button'

export default function PreparationPage() {
  const router = useRouter()
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    if (!authService.isAuthenticated()) {
      router.push('/login')
      return
    }
    setLoading(false)
  }, [router])

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-gray-600">Loading...</div>
      </div>
    )
  }

  // Mock preparation data
  const mockPreparationPlan = {
    title: 'TechCorp Software Engineer Preparation',
    progress: 45,
    totalDays: 7,
    currentDay: 3,
    tasks: [
      {
        day: 1,
        title: 'Java + OOP Fundamentals',
        status: 'completed',
        topics: ['Classes and Objects', 'Inheritance', 'Polymorphism', 'Encapsulation']
      },
      {
        day: 2,
        title: 'SQL + DBMS',
        status: 'completed',
        topics: ['Basic Queries', 'Joins', 'Indexing', 'Normalization']
      },
      {
        day: 3,
        title: 'Data Structures & Algorithms',
        status: 'in_progress',
        topics: ['Arrays', 'Linked Lists', 'Stacks', 'Queues']
      },
      {
        day: 4,
        title: 'Company-Specific Questions',
        status: 'pending',
        topics: ['TechCorp Culture', 'Recent Projects', 'Technical Interview Questions']
      },
      {
        day: 5,
        title: 'Technical Interview Practice',
        status: 'pending',
        topics: ['System Design', 'Coding Problems', 'Problem Solving']
      },
      {
        day: 6,
        title: 'HR Interview Preparation',
        status: 'pending',
        topics: ['Behavioral Questions', 'Salary Negotiation', 'Company Values']
      },
      {
        day: 7,
        title: 'Full Mock Interview',
        status: 'pending',
        topics: ['Complete Interview Simulation', 'AI Feedback', 'Performance Analysis']
      }
    ]
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white border-b border-gray-200">
        <div className="container mx-auto px-4 py-4 flex justify-between items-center">
          <div className="flex items-center space-x-4">
            <Link href="/dashboard" className="text-2xl font-bold text-blue-600">
              JobCrack AI
            </Link>
            <span className="text-gray-600">|</span>
            <span className="text-gray-900 font-medium">Preparation</span>
          </div>
          <Link href="/dashboard">
            <Button variant="ghost">Back to Dashboard</Button>
          </Link>
        </div>
      </header>

      <div className="container mx-auto px-4 py-8">
        <div className="max-w-4xl mx-auto">
          {/* Current Plan */}
          <div className="bg-white rounded-lg shadow p-8 mb-8">
            <div className="flex justify-between items-start mb-6">
              <div>
                <h2 className="text-2xl font-bold text-gray-900 mb-2">
                  {mockPreparationPlan.title}
                </h2>
                <p className="text-gray-600">
                  Day {mockPreparationPlan.currentDay} of {mockPreparationPlan.totalDays}
                </p>
              </div>
              <div className="text-right">
                <div className="text-3xl font-bold text-blue-600 mb-1">
                  {mockPreparationPlan.progress}%
                </div>
                <div className="text-sm text-gray-600">Complete</div>
              </div>
            </div>

            {/* Progress Bar */}
            <div className="w-full bg-gray-200 rounded-full h-2 mb-6">
              <div 
                className="bg-blue-600 h-2 rounded-full transition-all"
                style={{ width: `${mockPreparationPlan.progress}%` }}
              ></div>
            </div>

            <div className="flex gap-4">
              <Button className="flex-1">
                <Play className="w-4 h-4 mr-2" />
                Continue Learning
              </Button>
              <Button variant="outline">
                Generate New Plan
              </Button>
            </div>
          </div>

          {/* Preparation Tasks */}
          <div className="bg-white rounded-lg shadow p-8">
            <h2 className="text-2xl font-bold text-gray-900 mb-6">Preparation Schedule</h2>
            
            <div className="space-y-4">
              {mockPreparationPlan.tasks.map((task) => (
                <div 
                  key={task.day}
                  className={`p-4 rounded-lg border-2 ${
                    task.status === 'completed' 
                      ? 'border-green-200 bg-green-50' 
                      : task.status === 'in_progress'
                      ? 'border-blue-200 bg-blue-50'
                      : 'border-gray-200 bg-gray-50'
                  }`}
                >
                  <div className="flex items-start justify-between mb-3">
                    <div className="flex items-center space-x-3">
                      {task.status === 'completed' ? (
                        <CheckCircle className="w-6 h-6 text-green-600" />
                      ) : task.status === 'in_progress' ? (
                        <Clock className="w-6 h-6 text-blue-600" />
                      ) : (
                        <Target className="w-6 h-6 text-gray-400" />
                      )}
                      <div>
                        <h3 className="font-semibold text-gray-900">
                          Day {task.day}: {task.title}
                        </h3>
                        <p className="text-sm text-gray-600 capitalize">
                          {task.status.replace('_', ' ')}
                        </p>
                      </div>
                    </div>
                    {task.status === 'pending' && (
                      <Button variant="outline" size="sm">
                        Start
                      </Button>
                    )}
                  </div>

                  <div className="flex flex-wrap gap-2 ml-9">
                    {task.topics.map((topic) => (
                      <span key={topic} className="px-3 py-1 bg-white rounded-full text-sm text-gray-700">
                        {topic}
                      </span>
                    ))}
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Quick Actions */}
          <div className="grid md:grid-cols-2 gap-6 mt-8">
            <div className="bg-white rounded-lg shadow p-6">
              <BookOpen className="w-8 h-8 text-blue-600 mb-3" />
              <h3 className="font-semibold text-gray-900 mb-2">Interview Questions</h3>
              <p className="text-gray-600 text-sm mb-4">
                Practice company-specific interview questions
              </p>
              <Button variant="outline" className="w-full">
                Browse Questions
              </Button>
            </div>
            <div className="bg-white rounded-lg shadow p-6">
              <Target className="w-8 h-8 text-blue-600 mb-3" />
              <h3 className="font-semibold text-gray-900 mb-2">Mock Interview</h3>
              <p className="text-gray-600 text-sm mb-4">
                Practice with AI-powered mock interviews
              </p>
              <Button variant="outline" className="w-full">
                Start Mock Interview
              </Button>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
