import type { Metadata } from 'next'
import { AuthGuard } from '@/components/auth/auth-guard'
import { RegisterForm } from '@/components/auth/register-form'
import { APP_NAME } from '@/lib/constants'

export const metadata: Metadata = {
  title: 'Create Account',
  description: `Create your ${APP_NAME} account`,
}

export default function RegisterPage() {
  return (
    <AuthGuard requireAuth={false}>
      <div className="min-h-screen flex items-center justify-center bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
        <div className="max-w-md w-full space-y-8">
          <div className="text-center">
            <h1 className="text-3xl font-bold text-gray-900 mb-2">
              {APP_NAME}
            </h1>
            <p className="text-gray-600">
              Commodity Trading CRM System
            </p>
          </div>
          <RegisterForm />
        </div>
      </div>
    </AuthGuard>
  )
}