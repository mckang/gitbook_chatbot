const { merge } = require('webpack-merge');
const commonConfig = require('./webpack.common');
const path = require('path');

const prodConfig = {
  mode: 'production',
  entry: './src/index.js', // 진입점 파일
  output: {
    path: path.resolve(__dirname, '../dist'),
    filename: 'chatui.bundle.js',
    library: 'ChatUI', // 글로벌로 접근할 수 있도록 설정
    libraryTarget: 'umd', // Universal Module Definition: 다른 환경에서 사용할 수 있도록 함
  },
  plugins: [

  ],
};

module.exports = merge(commonConfig, prodConfig);
