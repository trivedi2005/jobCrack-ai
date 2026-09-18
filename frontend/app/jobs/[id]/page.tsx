'use client'

import { useEffect, useState } from 'react'
import { useRouter, useParams } from 'next/navigation'
import Link from 'next/link'
import { authService } from '@/lib/auth'
import { 
  MapPin, Briefcase, DollarSign, Clock, 
  Calendar, Building2, CheckCircle, AlertCircle,
  ArrowLeft, Target, BookOpen, FileText
} from 'lucide-react'
import { Button } from '@/components/ui/button'

export default function JobDetailsPage() {
  const router = useRouter()
  const params = useParams()
  const jobId = params.id as string
  const [loading, setLoading] = useState(true)
  const [job, setJob] = useState<any>(null)
  const [matchAnalysis, setMatchAnalysis] = useState<any>(null)

  useEffect(() => {
    if (!authService.isAuthenticated()) {
      router.push('/login')
      return
    }

    fetchJobDetails()
  }, [jobId, router])

  const fetchJobDetails = async () => {
    try {
      const response = await fetch(`http://localhost:8000/api/jobs/${jobId}`, {
        headers: {
          'Authorization': `Bearer ${authService.getAccessToken()}`,
        },
      })
      if (response.ok) {
        const jobData = await response.json()
        setJob(jobData)
      }
    } catch (error) {
      console.error('Failed to fetch job details:', error)
    } finally {
      setLoading(false)
    }
  }

  const fetchMatchAnalysis = async () => {
    try {
      const response = await fetch(`http://localhost:8000/api/matching/jobs/${jobId}/match`, {
        headers: {
          'Authorization': `Bearer ${authService.getAccessToken()}`,
        },
      })
      if (response.ok) {
        const matchData = await response.json()
        setMatchAnalysis(matchData)
      }
    } catch (error) {
      console.error('Failed to fetch match analysis:', error)
    }
  }

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-gray-600">Loading...</div>
      </div>
    )
  }

  if (!job) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-gray-600">Job not found</div>
      </div>
    )
  }

  // Mock match analysis for demonstration
  const mockMatchAnalysis = {
    overall_score: 82,
    skills_score: 85,
    experience_score: 75,
    education_score: 90,
    location_score: 100,
    matched_skills: ['Java', 'Spring Boot', 'React', 'SQL'],
    missing_skills: ['AWS', 'Docker', 'Kubernetes'],
    relevant_experience: [
      {
        company: 'Previous Company',
        role: 'Software Developer',
        relevance: 'high'
      }
    ],
    skill_gaps: [
      {
        skill: 'AWS',
        importance: 'high',
        suggested_learning: 'AWS Fundamentals'
      }
    ],
    suggested_preparation: [
      'Learn AWS basics',
      'Practice Docker and Kubernetes',
      'Study system design patterns'
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
            <span className="text-gray-900 font-medium">Job Details</span>
          </div>
          <Link href="/jobs">
            <Button variant="ghost">
              <ArrowLeft className="w-4 h-4 mr-2" />
              Back to Jobs
            </Button>
          </Link>
        </div>
      </header>

      <div className="container mx-auto px-4 py-8">
        <div className="max-w-6xl mx-auto">
          {/* Job Header */}
          <div className="bg-white rounded-lg shadow p-8 mb-8">
            <div className="flex justify-between items-start mb-6">
              <div className="flex-1">
                <h1 className="text-3xl font-bold text-gray-900 mb-2">{job.title}</h1>
                <div className="flex items-center space-x-4 text-gray-600 mb-4">
                  <div className="flex items-center">
                    <Building2 className="w-5 h-5 mr-2" />
                    {job.company_name}
                  </div>
                  <div className="flex items-center">
                    <MapPin className="w-5 h-5 mr-2" />
                    {job.location}
                  </div>
                </div>
                <div className="flex flex-wrap gap-4 text-sm text-gray-600">
                  <div className="flex items-center">
                    <Briefcase className="w-4 h-4 mr-2" />
                    {job.experience_level}
                  </div>
                  <div className="flex items-center">
                    <Clock className="w-4 h-4 mr-2" />
                    {job.work_mode}
                  </div>
                  <div className="flex items-center">
                    <DollarSign className="w-4 h-4 mr-2" />
                    {job.salary_min && job.salary_max 
                      ? `${job.salary_currency} ${job.salary_min.toLocaleString()} - ${job.salary_max.toLocaleString()}`
                      : 'Salary not specified'
                    }
                  </div>
                  <div className="flex items-center">
                    <Calendar className="w-4 h-4 mr-2" />
                    Posted {new Date(job.posted_date).toLocaleDateString()}
                  </div>
                </div>
              </div>
              <div className="text-right">
                <div className="mb-4">
                  <span className="px-4 py-2 bg-green-100 text-green-700 rounded-full text-lg font-semibold">
                    {mockMatchAnalysis.overall_score}% Match
                  </span>
                </div>
                <div className="space-y-2">
                  <Button className="w-full">Apply Now</Button>
                  <Button variant="outline" className="w-full">
                    <Target className="w-4 h-4 mr-2" />
                    Analyze Match
                  </Button>
                </div>
              </div>
            </div>

            {/* Job Description */}
            <div className="mb-6">
              <h2 className="text-xl font-semibold text-gray-900 mb-3">Job Description</h2>
              <p className="text-gray-700 whitespace-pre-line">{job.description || 'No description provided'}</p>
            </div>

            {/* Requirements */}
            {job.requirements && (
              <div className="mb-6">
                <h2 className="text-xl font-semibold text-gray-900 mb-3">Requirements</h2>
                <p className="text-gray-700 whitespace-pre-line">{job.requirements}</p>
              </div>
            )}

            {/* Responsibilities */}
            {job.responsibilities && (
              <div className="mb-6">
                <h2 className="text-xl font-semibold text-gray-900 mb-3">Responsibilities</h2>
                <p className="text-gray-700 whitespace-pre-line">{job.responsibilities}</p>
              </div>
            )}

            {/* Skills */}
            <div>
              <h2 className="text-xl font-semibold text-gray-900 mb-3">Required Skills</h2>
              <div className="flex flex-wrap gap-2">
                <span className="px-3 py-1 bg-blue-50 text-blue-700 rounded-full">Java</span>
                <span className="px-3 py-1 bg-blue-50 text-blue-700 rounded-full">Spring Boot</span>
                <span className="px-3 py-1 bg-blue-50 text-blue-700 rounded-full">React</span>
                <span className="px-3 py-1 bg-blue-50 text-blue-700 rounded-full">SQL</span>
              </div>
            </div>
          </div>

          {/* Match Analysis */}
          <div className="bg-white rounded-lg shadow p-8 mb-8">
            <h2 className="text-2xl font-bold text-gray-900 mb-6">Match Analysis</h2>
            
            {/* Match Scores */}
            <div className="grid md:grid-cols-4 gap-6 mb-8">
              <div className="text-center">
                <div className="text-4xl font-bold text-blue-600 mb-2">{mockMatchAnalysis.overall_score}%</div>
                <div className="text-gray-600">Overall</div>
              </div>
              <div className="text-center">
                <div className="text-4xl font-bold text-green-600 mb-2">{mockMatchAnalysis.skills_score}%</div>
                <div className="text-gray-600">Skills</div>
              </div>
              <div className="text-center">
                <div className="text-4xl font-bold text-purple-600 mb-2">{mockMatchAnalysis.experience_score}%</div>
                <div className="text-gray-600">Experience</div>
              </div>
              <div className="text-center">
                <div className="text-4xl font-bold text-orange-600 mb-2">{mockMatchAnalysis.education_score}%</div>
                <div className="text-gray-600">Education</div>
              </div>
            </div>

            {/* Matched Skills */}
            <div className="mb-6">
              <h3 className="text-lg font-semibold text-gray-900 mb-3 flex items-center">
                <CheckCircle className="w-5 h-5 text-green-600 mr-2" />
                Matched Skills
              </h3>
              <div className="flex flex-wrap gap-2">
                {mockMatchAnalysis.matched_skills.map((skill: string) => (
                  <span key={skill} className="px-3 py-1 bg-green-50 text-green-700 rounded-full">
                    {skill}
                  </span>
                ))}
              </div>
            </div>

            {/* Missing Skills */}
            <div className="mb-6">
              <h3 className="text-lg font-semibold text-gray-900 mb-3 flex items-center">
                <AlertCircle className="w-5 h-5 text-red-600 mr-2" />
                Missing Skills
              </h3>
              <div className="flex flex-wrap gap-2">
                {mockMatchAnalysis.missing_skills.map((skill: string) => (
                  <span key={skill} className="px-3 py-1 bg-red-50 text-red-700 rounded-full">
                    {skill}
                  </span>
                ))}
              </div>
            </div>

            {/* Skill Gaps */}
            <div className="mb-6">
              <h3 className="text-lg font-semibold text-gray-900 mb-3">Skill Gaps</h3>
              <div className="space-y-3">
                {mockMatchAnalysis.skill_gaps.map((gap: any, index: number) => (
                  <div key={index} className="p-4 bg-gray-50 rounded-lg">
                    <div className="flex justify-between items-center mb-2">
                      <span className="font-medium">{gap.skill}</span>
                      <span className="px-2 py-1 bg-orange-100 text-orange-700 rounded text-sm">
                        {gap.importance}
                      </span>
                    </div>
                    <p className="text-gray-600 text-sm">Suggested: {gap.suggested_learning}</p>
                  </div>
                ))}
              </div>
            </div>

            {/* Suggested Preparation */}
            <div>
              <h3 className="text-lg font-semibold text-gray-900 mb-3">Suggested Preparation</h3>
              <ul className="space-y-2">
                {mockMatchAnalysis.suggested_preparation.map((item: string, index: number) => (
                  <li key={index} className="flex items-start">
                    <Target className="w-5 h-5 text-blue-600 mr-2 mt-0.5" />
                    <span className="text-gray-700">{item}</span>
                  </li>
                ))}
              </ul>
            </div>
          </div>

          {/* Action Buttons */}
          <div className="grid md:grid-cols-3 gap-4">
            <Button className="text-lg py-6">
              <Briefcase className="w-5 h-5 mr-2" />
              Apply Now
            </Button>
            <Button variant="outline" className="text-lg py-6">
              <FileText className="w-5 h-5 mr-2" />
              Tailor Resume
            </Button>
            <Button variant="outline" className="text-lg py-6">
              <BookOpen className="w-5 h-5 mr-2" />
              Prepare for Company
            </Button>
          </div>
        </div>
      </div>
    </div>
  )
}
