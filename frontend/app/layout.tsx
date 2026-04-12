import type { Metadata } from 'next'
import { Geist, Geist_Mono } from 'next/font/google'
import { Analytics } from '@vercel/analytics/next'
import './globals.css'
import ClientWrapper from "@/components/ClientWrapper"
import { ThemeProvider } from "@/components/theme-provider"

const _geist = Geist({ subsets: ["latin"] });
const _geistMono = Geist_Mono({ subsets: ["latin"] });
const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});
export const metadata: Metadata = {
  title: 'Dastoor Desk - AI-Powered Legal Guidance',
  description: 'Get instant legal guidance and understand your rights with AI-powered assistance across property disputes, cybercrime, traffic regulations, consumer rights, and more.',
  generator: 'v0.app',
  icons: {
    icon: [
    {
      url: '/dastoorlogo.png', // This points to the new file you just moved
      href: '/dastoorlogo.png',
    },
  ],
    apple: '/apple-icon.png',
  },
}

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode
}>) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body className={`${geistSans.variable} ${geistMono.variable} font-sans antialiased`}>
        <ThemeProvider
          attribute="class"
          defaultTheme="dark"
          enableSystem
          disableTransitionOnChange
        >
          {/* The ClientWrapper handles the LogoIntro animation and wrapping */}
          <ClientWrapper>
            {children}
          </ClientWrapper>
          <Analytics />
        </ThemeProvider>
      </body>
    </html>
  )
}
