'use client'

import { useEffect, useState } from 'react'
import { useRouter } from 'next/navigation'
import Link from 'next/link'
import { authService } from '@/lib/auth'
import { Upload, FileText, Sparkles, Download } from 'lucide-react'
import { Button } from '@/components/ui/button'

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

type Resume = {
  id: number
  original_filename: string
  file_size?: number
  created_at: string
  is_current: boolean
}

type Analysis = {
  keyword_score?: number
  structure_score?: number
  formatting_score?: number
  overall_score?: number
  job_match_score?: number
  missing_keywords?: string[]
  suggested_improvements?: string[]
}

export default function ResumePage() {
  const router = useRouter()
  const [loading, setLoading] = useState(true)
  const [resumes, setResumes] = useState<Resume[]>([])
  const [selectedFile, setSelectedFile] = useState<File | null>(null)
  const [selectedResumeId, setSelectedResumeId] = useState<number | null>(null)
  const [analysis, setAnalysis] = useState<Analysis | null>(null)
  const [targetRole, setTargetRole] = useState('')
  const [versionCreated, setVersionCreated] = useState(false)
  const [busy, setBusy] = useState(false)
  const [message, setMessage] = useState('')

  useEffect(() => {
    if (!authService.isAuthenticated()) {
      router.push('/login')
      return
    }
    fetchResumes()
    setLoading(false)
  }, [router])

  const authHeaders = () => ({ Authorization: `Bearer ${authService.getAccessToken()}` })

  const fetchResumes = async () => {
    try {
      const response = await fetch(`${API_URL}/api/resumes/`, { headers: authHeaders(), cache: 'no-store' })
      if (!response.ok) throw new Error('Unable to load resumes')
      const data: Resume[] = await response.json()
      setResumes(data)
      if (data[0]) setSelectedResumeId(data[0].id)
    } catch {
      setMessage('Unable to load your resumes. Please sign in again.')
    }
  }

  const uploadResume = async () => {
    if (!selectedFile) {
      setMessage('Choose a PDF or DOCX file first.')
      return
    }
    setBusy(true)
    setMessage('')
    const formData = new FormData()
    formData.append('file', selectedFile)
    try {
      const response = await fetch(`${API_URL}/api/resumes/upload`, { method: 'POST', headers: authHeaders(), body: formData })
      const data = await response.json()
      if (!response.ok) setMessage(data.detail || 'Upload failed.')
      else {
        setMessage('Resume uploaded successfully.'); setSelectedFile(null); await fetchResumes(); setSelectedResumeId(data.id)
      }
    } catch {
      setMessage('Upload failed. Check that the backend is running and try again.')
    }
    setBusy(false)
  }

  const analyzeResume = async () => {
    if (!selectedResumeId) { setMessage('Upload a resume before analyzing it.'); return }
    if (!targetRole.trim()) { setMessage('Enter the role you are applying for first.'); return }
    setBusy(true); setMessage('')
    try {
      const response = await fetch(`${API_URL}/api/resumes/analyze`, { method: 'POST', headers: { ...authHeaders(), 'Content-Type': 'application/json' }, body: JSON.stringify({ resume_id: selectedResumeId, target_role: targetRole.trim() }) })
      const data = await response.json()
      if (!response.ok) setMessage(data.detail || 'Analysis failed.')
      else { setAnalysis(data); setMessage('ATS analysis completed.') }
    } catch {
      setMessage('Analysis failed. Check that the backend is running and try again.')
    }
    setBusy(false)
  }

  const createAtsVersion = async () => {
    if (!selectedResumeId || !targetRole.trim()) return
    setBusy(true)
    const response = await fetch(`${API_URL}/api/resumes/tailor`, { method: 'POST', headers: { ...authHeaders(), 'Content-Type': 'application/json' }, body: JSON.stringify({ resume_id: selectedResumeId, target_role: targetRole.trim() }) })
    const data = await response.json()
    if (!response.ok) setMessage(data.detail || 'Could not create ATS version.')
    else { setVersionCreated(true); setMessage(`Created ${data.version_name}.`) }
    setBusy(false)
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
            
            <div className="block border-2 border-dashed border-gray-300 rounded-lg p-12 text-center">
              <Upload className="w-12 h-12 text-gray-400 mx-auto mb-4" />
              <p className="text-gray-600 mb-2">
                Drag and drop your resume here, or click to browse
              </p>
              <p className="text-sm text-gray-500">
                Supported formats: PDF, DOCX (Max 10MB)
              </p>
              <label htmlFor="resume-file" className="inline-flex cursor-pointer rounded-md bg-blue-600 px-4 py-2 text-sm font-medium text-white hover:bg-blue-700">Choose PDF or DOCX</label>
              <input id="resume-file" type="file" accept=".pdf,.docx,application/pdf,application/vnd.openxmlformats-officedocument.wordprocessingml.document" className="sr-only" onChange={(event) => { setAnalysis(null); setSelectedFile(event.target.files?.[0] || null) }} />
              {selectedFile && <p className="mt-3 text-sm font-medium text-blue-700">Selected: {selectedFile.name}</p>}
            </div>

            <div className="mt-6">
              <Button className="w-full" onClick={uploadResume} disabled={busy || !selectedFile}>
                <Upload className="w-4 h-4 mr-2" />
                Upload Resume
              </Button>
            </div>
            {message && <p className="mt-4 rounded bg-blue-50 px-4 py-3 text-blue-700">{message}</p>}
          </div>

          {/* Resume Analysis Section */}
          <div className="bg-white rounded-lg shadow p-8 mb-8">
            <h2 className="text-2xl font-bold text-gray-900 mb-4">ATS Analysis</h2>
            <p className="text-gray-600 mb-6">
              Get detailed insights about your resume's ATS compatibility and improvement suggestions.
            </p>

            {!selectedResumeId && <p className="mb-6 rounded bg-gray-50 px-4 py-3 text-gray-600">Upload a resume to unlock role-specific ATS analysis.</p>}
            {selectedResumeId && <>
              <label htmlFor="target-role" className="mb-2 block text-sm font-medium text-gray-700">Role you are applying for</label>
              <input id="target-role" value={targetRole} onChange={(event) => { setTargetRole(event.target.value); setAnalysis(null); setVersionCreated(false) }} placeholder="e.g. Frontend Developer" className="mb-6 w-full rounded-md border border-gray-300 px-3 py-2" />
            </>}
            <div className="grid md:grid-cols-4 gap-6 mb-6">
              <div className="text-center">
                <div className="text-4xl font-bold text-blue-600 mb-2">{analysis?.keyword_score ?? '-'}{analysis ? '%' : ''}</div>
                <div className="text-gray-600">Keywords</div>
              </div>
              <div className="text-center">
                <div className="text-4xl font-bold text-green-600 mb-2">{analysis?.structure_score ?? '-'}{analysis ? '%' : ''}</div>
                <div className="text-gray-600">Structure</div>
              </div>
              <div className="text-center">
                <div className="text-4xl font-bold text-purple-600 mb-2">{analysis?.formatting_score ?? '-'}{analysis ? '%' : ''}</div>
                <div className="text-gray-600">Projects</div>
              </div>
              <div className="text-center">
                <div className="text-4xl font-bold text-orange-600 mb-2">{analysis?.overall_score ?? '-'}{analysis ? '%' : ''}</div>
                <div className="text-gray-600">Job Match</div>
              </div>
            </div>

            {selectedResumeId && <Button variant="outline" className="w-full" onClick={analyzeResume} disabled={busy || !targetRole.trim()}>
              <Sparkles className="w-4 h-4 mr-2" />
              Analyze Resume for This Role
            </Button>}
            {analysis && (analysis.overall_score || 0) < 90 && !versionCreated && (
              <div className="mt-4 rounded-lg border border-orange-200 bg-orange-50 p-4">
                <p className="text-sm text-orange-800">This resume needs improvement for the {targetRole} role.</p>
                <Button className="mt-3 w-full" onClick={createAtsVersion} disabled={busy}>Create ATS Resume Version</Button>
              </div>
            )}
          </div>

          {/* Resume Versions */}
          <div className="bg-white rounded-lg shadow p-8">
            <h2 className="text-2xl font-bold text-gray-900 mb-4">Resume Versions</h2>
            <p className="text-gray-600 mb-6">
              Manage different versions of your resume tailored for specific companies or roles.
            </p>

            <div className="space-y-4">
              {resumes.length === 0 && <p className="text-gray-600">No resume uploaded yet.</p>}
              {resumes.map((resume) => <div key={resume.id} className={`flex items-center justify-between p-4 rounded-lg ${selectedResumeId === resume.id ? 'bg-blue-50 ring-2 ring-blue-200' : 'bg-gray-50'}`} onClick={() => setSelectedResumeId(resume.id)}>
                <div className="flex items-center space-x-4">
                  <FileText className="w-8 h-8 text-blue-600" />
                  <div>
                    <h3 className="font-semibold text-gray-900">{resume.original_filename}</h3>
                    <p className="text-sm text-gray-600">{Math.round((resume.file_size || 0) / 1024)} KB</p>
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
              </div>)}
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
