'use client'

import { useEffect, useState } from 'react'
import { useRouter } from 'next/navigation'
import Link from 'next/link'
import { authService } from '@/lib/auth'
import { Upload, FileText, Sparkles, Download } from 'lucide-react'
import { Button } from '@/components/ui/button'

export default function ResumePage() {
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
            <span className="text-gray-900 font-medium">Resume Studio</span>
          </div>
          <Link href="/dashboard">
            <Button variant="ghost">Back to Dashboard</Button>
          </Link>
        </div>
      </header>

      <div className="container mx-auto px-4 py-8">
        <div className="max-w-4xl mx-auto">
          {/* Upload Section */}
          <div className="bg-white rounded-lg shadow p-8 mb-8">
            <h2 className="text-2xl font-bold text-gray-900 mb-4">Upload Your Resume</h2>
            <p className="text-gray-600 mb-6">
              Upload your resume in PDF or DOCX format to get started with AI-powered analysis.
            </p>
            
            <div className="border-2 border-dashed border-gray-300 rounded-lg p-12 text-center hover:border-blue-500 transition cursor-pointer">
              <Upload className="w-12 h-12 text-gray-400 mx-auto mb-4" />
              <p className="text-gray-600 mb-2">
                Drag and drop your resume here, or click to browse
              </p>
              <p className="text-sm text-gray-500">
                Supported formats: PDF, DOCX (Max 10MB)
              </p>
            </div>

            <div className="mt-6">
              <Button className="w-full">
                <Upload className="w-4 h-4 mr-2" />
                Upload Resume
              </Button>
            </div>
          </div>

          {/* Resume Analysis Section */}
          <div className="bg-white rounded-lg shadow p-8 mb-8">
            <h2 className="text-2xl font-bold text-gray-900 mb-4">ATS Analysis</h2>
            <p className="text-gray-600 mb-6">
              Get detailed insights about your resume's ATS compatibility and improvement suggestions.
            </p>

            <div className="grid md:grid-cols-4 gap-6 mb-6">
              <div className="text-center">
                <div className="text-4xl font-bold text-blue-600 mb-2">89%</div>
                <div className="text-gray-600">Keywords</div>
              </div>
              <div className="text-center">
                <div className="text-4xl font-bold text-green-600 mb-2">92%</div>
                <div className="text-gray-600">Structure</div>
              </div>
              <div className="text-center">
                <div className="text-4xl font-bold text-purple-600 mb-2">85%</div>
                <div className="text-gray-600">Projects</div>
              </div>
              <div className="text-center">
                <div className="text-4xl font-bold text-orange-600 mb-2">78%</div>
                <div className="text-gray-600">Job Match</div>
              </div>
            </div>

            <Button variant="outline" className="w-full">
              <Sparkles className="w-4 h-4 mr-2" />
              Analyze Resume
            </Button>
          </div>

          {/* Resume Versions */}
          <div className="bg-white rounded-lg shadow p-8">
            <h2 className="text-2xl font-bold text-gray-900 mb-4">Resume Versions</h2>
            <p className="text-gray-600 mb-6">
              Manage different versions of your resume tailored for specific companies or roles.
            </p>

            <div className="space-y-4">
              <div className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
                <div className="flex items-center space-x-4">
                  <FileText className="w-8 h-8 text-blue-600" />
                  <div>
                    <h3 className="font-semibold text-gray-900">Original Resume</h3>
                    <p className="text-sm text-gray-600">Last updated: 2 days ago</p>
                  </div>
                </div>
                <div className="flex gap-2">
                  <Button variant="outline" size="sm">
                    <Download className="w-4 h-4 mr-1" />
                    Download
                  </Button>
                  <Button variant="ghost" size="sm">
                    Edit
                  </Button>
                </div>
              </div>

              <div className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
                <div className="flex items-center space-x-4">
                  <FileText className="w-8 h-8 text-green-600" />
                  <div>
                    <h3 className="font-semibold text-gray-900">TechCorp - Software Engineer</h3>
                    <p className="text-sm text-gray-600">AI-tailored version • Last updated: 1 day ago</p>
                  </div>
                </div>
                <div className="flex gap-2">
                  <Button variant="outline" size="sm">
                    <Download className="w-4 h-4 mr-1" />
                    Download
                  </Button>
                  <Button variant="ghost" size="sm">
                    Edit
                  </Button>
                </div>
              </div>
            </div>

            <div className="mt-6">
              <Button variant="outline" className="w-full">
                <Sparkles className="w-4 h-4 mr-2" />
                Create New Version
              </Button>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
