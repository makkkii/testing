var path = require('path');
var webpack = require('webpack');
var BundleTracker = require('webpack-bundle-tracker');
var { CleanWebpackPlugin } = require('clean-webpack-plugin');

module.exports = {
  context: __dirname,
  entry: './client/index',
  output: {
      path: path.resolve( __dirname, 'etesting', 'default', 'js', 'bundles'),
      publicPath: 'http://localhost:3000/static/',
      filename: "[name]-[hash].js"
  },
  module: {
    rules: [
      { 
        test: /\.jsx?$/, 
        exclude: /node_modules/,
        loader: [ 'babel-loader']
      },
    ]
  },
  resolve: {
    extensions: ['.js', '.jsx']
  },
  plugins: [
    new BundleTracker({filename: './webpack-stats.json'}),
    new CleanWebpackPlugin()
  ],
  mode: 'development'
}