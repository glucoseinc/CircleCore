import path from 'path'
import DefinePlugin from 'webpack/lib/DefinePlugin'

module.exports = {
  entry: {
    'main': ['babel-polyfill', './src/js/main.es6'],
  },
  output: {
    publicPath: '/styles/',
    filename: '[name].bundle.js',
    chunkFilename: '[id].[chunkhash].chunked.js',
  },
  module: {
    loaders: [
      {
        test: /\.es6$/,
        exclude: /node_modules/,
        loader: 'babel',
        query: {
          cacheDirectory: true,
        },
      },
      {test: /\.json$/, loader: 'json'},
    ],
  },
  resolve: {
    root: path.resolve('src/js'),
    modulesDirectories: ['node_modules'],
    extensions: ['', '.es6', '.js'],
  },
  plugins: [
    new DefinePlugin({
      'process.env.NODE_ENV': JSON.stringify(process.env.NODE_ENV),
    }),
  ],
}
