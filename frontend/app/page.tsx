import Link from 'next/link'
import { ArrowRight, CheckCircle, Target, BookOpen, Briefcase, MessageSquare } from 'lucide-react'

export default function LandingPage() {
  return (
    <div className="min-h-screen bg-gradient-to-b from-blue-50 to-white">
      {/* Navigation */}
      <nav className="container mx-auto px-4 py-4 flex justify-between items-center">
        <div className="text-2xl font-bold text-blue-600">JobCrack AI</div>
        <div className="space-x-4">
          <Link href="/login" className="text-gray-600 hover:text-blue-600 transition">
            Login
          </Link>
          <Link 
            href="/register" 
            className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition"
          >
            Get Started
          </Link>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="container mx-auto px-4 py-20 text-center">
        <h1 className="text-5xl font-bold text-gray-900 mb-6">
          Find the job. Prepare for the company. Crack the interview.
        </h1>
        <p className="text-xl text-gray-600 mb-8 max-w-2xl mx-auto">
          One AI-powered platform for job discovery, resume optimization, company-specific preparation, 
          coding practice, mock interviews and application tracking.
        </p>
        <div className="space-x-4 justify-center flex">
          <Link 
            href="/register" 
            className="bg-blue-600 text-white px-8 py-3 rounded-lg hover:bg-blue-700 transition font-semibold"
          >
            Get Started Free
          </Link>
          <Link 
            href="/jobs" 
            className="border border-blue-600 text-blue-600 px-8 py-3 rounded-lg hover:bg-blue-50 transition font-semibold"
          >
            Explore Jobs
          </Link>
        </div>
      </section>

      {/* Features Section */}
      <section className="container mx-auto px-4 py-20">
        <h2 className="text-3xl font-bold text-center mb-12">How It Works</h2>
        <div className="grid md:grid-cols-3 gap-8">
          <div className="bg-white p-6 rounded-lg shadow-md">
            <Target className="w-12 h-12 text-blue-600 mb-4" />
            <h3 className="text-xl font-semibold mb-2">Job Discovery</h3>
            <p className="text-gray-600">
              Find jobs that match your skills and preferences with AI-powered job matching.
            </p>
          </div>
          <div className="bg-white p-6 rounded-lg shadow-md">
            <BookOpen className="w-12 h-12 text-blue-600 mb-4" />
            <h3 className="text-xl font-semibold mb-2">Company Preparation</h3>
            <p className="text-gray-600">
              Get company-specific interview questions, preparation plans, and coding challenges.
            </p>
          </div>
          <div className="bg-white p-6 rounded-lg shadow-md">
            <MessageSquare className="w-12 h-12 text-blue-600 mb-4" />
            <h3 className="text-xl font-semibold mb-2">AI Mock Interviews</h3>
            <p className="text-gray-600">
              Practice with AI-powered mock interviews tailored to your target companies and roles.
            </p>
          </div>
        </div>
      </section>

      {/* Problem Section */}
      <section className="container mx-auto px-4 py-20 bg-gray-50 rounded-lg">
        <h2 className="text-3xl font-bold text-center mb-12">The Problem</h2>
        <div className="max-w-3xl mx-auto">
          <ul className="space-y-4">
            <li className="flex items-start">
              <ArrowRight className="w-6 h-6 text-blue-600 mr-3 mt-1" />
              <span className="text-gray-700">
                Job search is fragmented across multiple platforms with no unified workflow
              </span>
            </li>
            <li className="flex items-start">
              <ArrowRight className="w-6 h-6 text-blue-600 mr-3 mt-1" />
              <span className="text-gray-700">
                Resume optimization is guesswork without proper ATS analysis
              </span>
            </li>
            <li className="flex items-start">
              <ArrowRight className="w-6 h-6 text-blue-600 mr-3 mt-1" />
              <span className="text-gray-700">
                Company-specific interview preparation is scattered and unreliable
              </span>
            </li>
            <li className="flex items-start">
              <ArrowRight className="w-6 h-6 text-blue-600 mr-3 mt-1" />
              <span className="text-gray-700">
                Application tracking is manual and disorganized
              </span>
            </li>
          </ul>
        </div>
      </section>

      {/* Solution Section */}
      <section className="container mx-auto px-4 py-20">
        <h2 className="text-3xl font-bold text-center mb-12">The Solution</h2>
        <div className="grid md:grid-cols-2 gap-8">
          <div className="space-y-4">
            <div className="flex items-start">
              <CheckCircle className="w-6 h-6 text-green-600 mr-3 mt-1" />
              <div>
                <h3 className="font-semibold">AI-Powered Job Matching</h3>
                <p className="text-gray-600">Get personalized job recommendations based on your skills and preferences</p>
              </div>
            </div>
            <div className="flex items-start">
              <CheckCircle className="w-6 h-6 text-green-600 mr-3 mt-1" />
              <div>
                <h3 className="font-semibold">ATS Resume Analysis</h3>
                <p className="text-gray-600">Optimize your resume with AI-driven ATS analysis and suggestions</p>
              </div>
            </div>
            <div className="flex items-start">
              <CheckCircle className="w-6 h-6 text-green-600 mr-3 mt-1" />
              <div>
                <h3 className="font-semibold">Company-Specific Prep</h3>
                <p className="text-gray-600">Access verified interview questions and preparation plans for top companies</p>
              </div>
            </div>
          </div>
          <div className="space-y-4">
            <div className="flex items-start">
              <CheckCircle className="w-6 h-6 text-green-600 mr-3 mt-1" />
              <div>
                <h3 className="font-semibold">Coding Practice</h3>
                <p className="text-gray-600">Practice coding problems tagged by companies and difficulty levels</p>
              </div>
            </div>
            <div className="flex items-start">
              <CheckCircle className="w-6 h-6 text-green-600 mr-3 mt-1" />
              <div>
                <h3 className="font-semibold">AI Mock Interviews</h3>
                <p className="text-gray-600">Practice with AI interviewers that adapt to your responses</p>
              </div>
            </div>
            <div className="flex items-start">
              <CheckCircle className="w-6 h-6 text-green-600 mr-3 mt-1" />
              <div>
                <h3 className="font-semibold">Application Tracking</h3>
                <p className="text-gray-600">Track all your applications in one place with timeline and notifications</p>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Features Deep Dive */}
      <section className="container mx-auto px-4 py-20">
        <h2 className="text-3xl font-bold text-center mb-12">Platform Features</h2>
        <div className="grid md:grid-cols-4 gap-6">
          <div className="text-center">
            <Briefcase className="w-12 h-12 text-blue-600 mx-auto mb-4" />
            <h3 className="font-semibold mb-2">Job Discovery</h3>
            <p className="text-gray-600 text-sm">Smart search with filters for location, role, experience, and skills</p>
          </div>
          <div className="text-center">
            <Target className="w-12 h-12 text-blue-600 mx-auto mb-4" />
            <h3 className="font-semibold mb-2">Skill Matching</h3>
            <p className="text-gray-600 text-sm">AI-powered analysis showing skill gaps and match percentages</p>
          </div>
          <div className="text-center">
            <BookOpen className="w-12 h-12 text-blue-600 mx-auto mb-4" />
            <h3 className="font-semibold mb-2">Resume Studio</h3>
            <p className="text-gray-600 text-sm">Upload, analyze, and tailor your resume for specific jobs</p>
          </div>
          <div className="text-center">
            <MessageSquare className="w-12 h-12 text-blue-600 mx-auto mb-4" />
            <h3 className="font-semibold mb-2">Career Copilot</h3>
            <p className="text-gray-600 text-sm">AI assistant available 24/7 for career guidance and questions</p>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="container mx-auto px-4 py-20 text-center bg-blue-600 rounded-lg">
        <h2 className="text-3xl font-bold text-white mb-4">Ready to Crack Your Dream Job?</h2>
        <p className="text-blue-100 mb-8">Join thousands of candidates who have transformed their job search with JobCrack AI</p>
        <Link 
          href="/register" 
          className="bg-white text-blue-600 px-8 py-3 rounded-lg hover:bg-gray-100 transition font-semibold"
        >
          Get Started Free
        </Link>
      </section>

      {/* Footer */}
      <footer className="container mx-auto px-4 py-8 text-center text-gray-600">
        <p>&copy; 2024 JobCrack AI. All rights reserved.</p>
      </footer>
    </div>
  )
}
