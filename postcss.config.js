module.exports = {
  'plugins': [
    require('postcss-import'),
    require('postcss-mixins'),
    require('postcss-nested'),
    require('postcss-color-function'),
    require('postcss-simple-vars'),
    require('postcss-cssnext'),
  ],
  'autoprefixer': {
    'browsers': [
      'last 2 versions',
      'iOS >= 8',
      'Android >= 4.0',
    ],
  },
}
