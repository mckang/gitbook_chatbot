/** @type {import('next').NextConfig} */
import fs from "fs";
import withLlamaIndex from "llamaindex/next";
import webpack from "./webpack.config.mjs";

const nextConfig = JSON.parse(fs.readFileSync("./next.config.json", "utf-8"));
nextConfig.webpack = webpack;

// 모든 경로를 index.html로 리디렉션하는 rewrites 설정 추가
nextConfig.rewrites = async () => [
    {
      source: '/:path*',
      destination: '/', // 모든 경로를 index.html로 리다이렉션
    },
  ];

// reactStrictMode 설정 추가
nextConfig.reactStrictMode = false;

// const cspHeader = `
//   default-src *;
//   script-src 'self' 'unsafe-eval' 'unsafe-inline' *;
//   style-src 'self' 'unsafe-inline'  *;
//   img-src 'self' blob: data: *;
//   font-src 'self' *;
//   object-src  *;
//   base-uri 'self'  *;
//   form-action 'self'  *;
//   frame-ancestors  *;
//   frame-src *;
// `
// // headers 설정 추가
// nextConfig.headers = async () => {
//   return [
//     {
//       // 모든 경로에 대해 적용
//       source: '/:path*',
//       headers: [
//         {
//           key: 'Content-Security-Policy',
//           value: cspHeader.replace(/\n/g, ''),
//         },
//       ],
//     },
//   ];
// };

nextConfig.rea


// use withLlamaIndex to add necessary modifications for llamaindex library
export default withLlamaIndex(nextConfig);
