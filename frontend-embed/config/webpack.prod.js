const { merge } = require('webpack-merge');
const commonConfig = require('./webpack.common');
const path = require('path');

// const prodConfig = {
//   mode: 'production',
//   entry: './src/index.js', // 진입점 파일
//   output: {
//     path: path.resolve(__dirname, '../dist'),
//     filename: 'chatui.bundle.js',
//     library: 'ChatUI', // 글로벌로 접근할 수 있도록 설정
//     libraryTarget: 'umd', // Universal Module Definition: 다른 환경에서 사용할 수 있도록 함
//   },
//   plugins: [

//   ],
// };

const TerserPlugin = require('terser-webpack-plugin');
const CompressionPlugin = require('compression-webpack-plugin');
const { BundleAnalyzerPlugin } = require('webpack-bundle-analyzer');
const { CleanWebpackPlugin } = require('clean-webpack-plugin');


const prodConfig = {
  mode: 'production',
  entry: {
    main: './src/index.js', // 진입점 파일
  },
  output: {
    path: path.resolve(__dirname, '../dist'),
    filename: 'socialbiz.chat.bundle.min.js', // 모든 코드가 하나의 파일로 번들링되도록 설정
    library: 'ChatUI', // 글로벌로 접근할 수 있도록 설정
    libraryTarget: 'umd', // Universal Module Definition: 다른 환경에서 사용할 수 있도록 함
  },
  optimization: {
    minimize: true, // 코드 압축 활성화
    minimizer: [
      new TerserPlugin({
        terserOptions: {
          compress: {
            drop_console: true, // console.log 제거하여 파일 크기 최적화
          },
        },
      }),
    ],
    splitChunks: {
      cacheGroups: {
        default: false, // 청크 분할 비활성화
      },
    },
  },
  plugins: [
    new CleanWebpackPlugin(), // 시작 시 dist 폴더 초기화
    new CompressionPlugin({
      algorithm: 'gzip', // gzip 압축 적용
      test: /\.(js|css)$/, // JS와 CSS 파일에 대해 압축 수행
      threshold: 10240, // 10KB 이상의 파일만 압축
      minRatio: 0.8, // 압축 비율이 0.8 이상인 경우만 적용
    }),
    new BundleAnalyzerPlugin({
      analyzerMode: 'static', // 번들 분석 리포트를 정적 파일로 생성
      openAnalyzer: false, // 자동으로 브라우저를 열지 않음
    }),
  ],
};

module.exports = merge(commonConfig, prodConfig);
