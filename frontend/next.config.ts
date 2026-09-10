import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  env: {
    NEXT_PUBLIC_API_URL: process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000",
  },
  transpilePackages: ["react-markdown", "remark-gfm", "remark-parse", "unified", "vfile", "unist-util-visit"],
  async headers() {
    return [
      {
        source: "/(.*)",
        headers: [
          { key: "X-Frame-Options", value: "ALLOWALL" },
          {
            key: "Content-Security-Policy",
            value: "frame-ancestors 'self' https://teams.microsoft.com https://*.teams.microsoft.com https://*.skype.com",
          },
        ],
      },
    ];
  },
};

export default nextConfig;
