/* eslint-disable require-jsdoc */
const path = require('path')
const DefinePlugin = require('webpack/lib/DefinePlugin')
const CopyWebpackPlugin = require('copy-webpack-plugin')

const _resolve = (...args) => path.resolve(__dirname, ...args)

class LoggerPlugin {
  apply(compiler) {
    const timestamp = () => `[${(new Date()).toLocaleString()}]`
    compiler.plugin('compile', (params) => {
      console.log('\x1b[1;36m' + '================================')
      console.log(timestamp() + ' Start compile' + '\x1b[0m')
    })
    compiler.plugin('after-emit', (params, callback) => {
      callback()
      console.log('\x1b[1;35m' + timestamp() + ' Finish compile')
      console.log('================================' + '\x1b[0m')
    })
  }
}

const SOURCE_DIR = _resolve('./circle_core/web/src')
const DEST_DIR = _resolve('./circle_core/web/static')

module.exports = {
  context: _resolve(SOURCE_DIR, 'js'),
  entry: {
    main: ['@babel/polyfill', `${SOURCE_DIR}/js/main.jsx`],
    public: ['@babel/polyfill', `${SOURCE_DIR}/js/public.jsx`],
  },
  output: {
    path: DEST_DIR,
    filename: '[name].bundle.js',
    chunkFilename: '[id].[chunkhash].chunked.js',
  },
  module: {
    rules: [
      {
        enforce: 'pre',
        test: /\.jsx?$/,
        exclude: /node_modules/,
        loader: 'eslint-loader',
      },
      {
        test: /\.jsx?$/,
        exclude: /node_modules/,
        loader: 'babel-loader',
        query: {
          cacheDirectory: true,
        },
      },
      {
        test: /\.css$/,
        loader: 'ignore-loader'
      }
    ],
  },
  devtool: 'source-map',
  resolve: {
    alias: {
      'src': _resolve(SOURCE_DIR, 'js')
    },
    modules: [
      'node_modules',
    ],
    extensions: ['.jsx', '.js'],
  },
  plugins: [
    new CopyWebpackPlugin([
      {
        from: _resolve(SOURCE_DIR, 'images'),
      },
    ]),
    new LoggerPlugin(),
  ],
  target: 'web',
}
