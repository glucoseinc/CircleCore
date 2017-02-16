let path = require('path')
let DefinePlugin = require('webpack/lib/DefinePlugin')

const SOURCE_DIR = './circle_core/web/src'

module.exports = {
  entry: {
    'main': ['babel-polyfill', `${SOURCE_DIR}/js/main.es6`],
    'public': ['babel-polyfill', `${SOURCE_DIR}/js/public.es6`],
  },
  output: {
    path: './circle_core/web/static/',
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
        test: /\.json$/,
        loader: 'json',
      },
    ],
  },
  // devtool: 'source-map',
  resolve: {
    root: path.resolve(`${SOURCE_DIR}/js`),
    modulesDirectories: ['node_modules'],
    extensions: ['', '.es6', '.js'],
  },
  plugins: [
    new DefinePlugin({
      'process.env.NODE_ENV': JSON.stringify(process.env.NODE_ENV),
    }),
    function() {
      this.plugin('watch-run', (watching, callback) => {
        console.log('\033[36m' + 'Begin compile at ' + new Date() + ' \033[39m')
        callback()
      })
    },
  ],
}
