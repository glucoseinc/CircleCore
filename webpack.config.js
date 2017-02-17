/* eslint-disable require-jsdoc */
const DefinePlugin = require('webpack/lib/DefinePlugin')
const CopyWebpackPlugin = require('copy-webpack-plugin')
const ExtractTextPlugin = require('extract-text-webpack-plugin')

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

const SOURCE_DIR = './circle_core/web/src'
const DEST_DIR = './circle_core/web/static'

module.exports = {
  entry: {
    main: ['babel-polyfill', `${SOURCE_DIR}/js/main.es6`],
    public: ['babel-polyfill', `${SOURCE_DIR}/js/public.es6`],
  },
  output: {
    path: DEST_DIR,
    filename: '[name].bundle.js',
    chunkFilename: '[id].[chunkhash].chunked.js',
  },
  module: {
    preLoaders: [
      {
        test: /\.es6$/,
        exclude: /node_modules/,
        loader: 'eslint',
      },
    ],
    loaders: [
      {
        test: /\.es6$/,
        exclude: /node_modules/,
        loader: 'babel',
        query: {
          cacheDirectory: true,
        },
      },
      {
        test: /\.css$/,
        loader: ExtractTextPlugin.extract('css!postcss'),
      },
    ],
  },
  // devtool: 'source-map',
  resolve: {
    root: `${SOURCE_DIR}/js`,
    modulesDirectories: ['node_modules'],
    extensions: ['', '.es6', '.js'],
  },
  plugins: [
    new ExtractTextPlugin('main.css'),
    new CopyWebpackPlugin([
      {
        from: `${SOURCE_DIR}/images/`,
      },
    ]),
    new DefinePlugin({
      'process.env.NODE_ENV': JSON.stringify(process.env.NODE_ENV),
    }),
    new LoggerPlugin(),
  ],
}
