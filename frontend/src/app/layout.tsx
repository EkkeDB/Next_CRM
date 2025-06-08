import type { Metadata, Viewport } from 'next'
import { Inter } from 'next/font/google'
import { Toaster } from 'react-hot-toast'
import { QueryProvider } from '@/components/providers/query-provider'
import ErrorBoundary from '@/components/error-boundary'
import { APP_NAME } from '@/lib/constants'
import '@/styles/globals.css'

const inter = Inter({ subsets: ['latin'] })

export const metadata: Metadata = {
  title: {
    default: APP_NAME,
    template: `%s | ${APP_NAME}`,
  },
  description: 'Comprehensive Commodity Trading CRM System',
  keywords: ['CRM', 'Commodity Trading', 'Contract Management', 'NextJS', 'Django'],
  authors: [{ name: 'NextCRM Team' }],
  creator: 'NextCRM',
  publisher: 'NextCRM',
  robots: {
    index: false, // Prevent indexing for internal business app
    follow: false,
  },
}

export const viewport: Viewport = {
  width: 'device-width',
  initialScale: 1,
  maximumScale: 1,
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body className={inter.className}>
        <ErrorBoundary>
          <QueryProvider>
            {children}
            <Toaster
              position="top-right"
              toastOptions={{
                duration: 4000,
                style: {
                  background: 'hsl(var(--card))',
                  color: 'hsl(var(--card-foreground))',
                  border: '1px solid hsl(var(--border))',
                },
                success: {
                  iconTheme: {
                    primary: 'hsl(var(--primary))',
                    secondary: 'white',
                  },
                },
                error: {
                  iconTheme: {
                    primary: 'hsl(var(--destructive))',
                    secondary: 'white',
                  },
                },
              }}
            />
          </QueryProvider>
        </ErrorBoundary>
      </body>
    </html>
  )
}