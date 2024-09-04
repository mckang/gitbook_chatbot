const HtmlWebpackPlugin = require('html-webpack-plugin');
const webpack = require('webpack');
require('dotenv').config();

module.exports = {
  resolve: {
    extensions: ['.ts', '.tsx', ".js", ".jsx"],
  },  
  module: {
    rules: [
      {
        test: /\.(ts|tsx|js|jsx|mjs|cjs)$/, // 모든 JS 및 TS 파일 처리
        exclude: /node_modules/,
        use: {
          loader: 'babel-loader',
          options: {
            presets: [
              '@babel/preset-env',
              '@babel/preset-react',
              '@babel/preset-typescript',
            ],
            plugins: ['@babel/plugin-transform-runtime'],
          },
        },
      },   
      {
        test: /\.module\.css$/, // CSS Modules 처리
        use: [
          'style-loader', // 스타일을 `<style>` 태그로 삽입
          {
            loader: 'css-loader', // CSS 파일을 자바스크립트로 변환
            options: {
              modules: true, // CSS Modules 활성화
            },
          },
          'postcss-loader'
        ],
      },      
      {
        test: /\.css$/i,
        exclude: [/\.module\.css$/, /tailwind\.generated\.css$/i], // CSS Modules가 아닌 일반 CSS 파일만 처리
        use: ["style-loader", "css-loader",'postcss-loader'],
      },
      {
        test: /tailwind\.generated\.css$/i,
        use: ["raw-loader",'postcss-loader'],
      },      
      {
        test: /\.(png|jpe?g|gif)$/i,
        type: 'asset/resource',
      },      
    ],
  },
  plugins: [
    new HtmlWebpackPlugin({
      template: './public/index.html',
    }),
    new webpack.DefinePlugin({
      'process.env': JSON.stringify(process.env),
    }),    
  ],
};
