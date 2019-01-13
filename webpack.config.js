/* eslint-disable require-jsdoc */
const path = require('path')
const DefinePlugin = require('webpack/lib/DefinePlugin')
const CleanObsoleteChunks = require('webpack-clean-obsolete-chunks')
const ManifestPlugin = require('webpack-manifest-plugin')
const CopyWebpackPlugin = require('copy-webpack-plugin')
const TerserPlugin = require('terser-webpack-plugin')

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

module.exports = (env, argv) => ({
  context: _resolve(SOURCE_DIR, 'js'),
  entry: {
    main: ['@babel/polyfill', `${SOURCE_DIR}/js/main.jsx`],
    public: ['@babel/polyfill', `${SOURCE_DIR}/js/public.jsx`],
  },
  output: {
    path: DEST_DIR,
    filename: '[name].[chunkhash].js'
  },
  module: {
    rules: [
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
  devtool: (argv && argv.mode == 'production') ? false : 'cheap-module-eval-source-map',
  resolve: {
    alias: {
      'src': _resolve(SOURCE_DIR, 'js')
    },
    modules: ['node_modules'],
    extensions: ['.jsx', '.js'],
  },
  plugins: [
    new CopyWebpackPlugin([
      {
        from: _resolve(SOURCE_DIR, 'images'),
      },
    ]),
    new LoggerPlugin(),
    new ManifestPlugin(),
    new CleanObsoleteChunks({verbose: true, deep: true}),
  ],
  target: 'web',
  ...((argv && argv.mode != 'production') ? {} : {
    optimization: {
      // `$super`をmangleしないように
      // https://github.com/shutterstock/rickshaw#minification
      minimizer: [
        new TerserPlugin({
          cache: true,
          parallel: true,
          sourceMap: false,
          terserOptions: {
            mangle: {
              reserved: ['$super'],
            }
          }
        })
      ]
    }
  })
})
