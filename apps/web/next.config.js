/** @type {import('next').NextConfig} */
const nextConfig = {
  transpilePackages: ['shared', 'db'],
  async rewrites() {
    const isDev = process.env.NODE_ENV === 'development'
    
    if (isDev) {
      return [
        {
          source: '/api/graphql/:path*',
          destination: 'http://localhost:8000/graphql/:path*'
        }
      ]
    }
    
    // In production, Vercel handles API routes via vercel.json
    return []
  }
}

module.exports = nextConfig
