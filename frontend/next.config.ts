import type { NextConfig } from 'next'

// A static export: every page is HTML built ahead of time, served from frontend/out. Security
// headers live in vercel.json, because a static export cannot set them.
const nextConfig: NextConfig = {
  output: 'export',
  poweredByHeader: false,
}

export default nextConfig
