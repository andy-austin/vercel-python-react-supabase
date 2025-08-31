/** @type {import('next').NextConfig} */
const nextConfig = {
  transpilePackages: ['shared', 'db'],
  experimental: {
    appDir: true
  },
  async rewrites() {
    const isDev = process.env.NODE_ENV === 'development'
    const apiUrl = isDev 
      ? 'http://localhost:8000' 
      : process.env.API_DOMAIN || 'https://your-api-domain.vercel.app'
    
    return [
      {
        source: '/api/graphql/:path*',
        destination: `${apiUrl}/graphql/:path*`
      }
    ]
  }
}

module.exports = nextConfig