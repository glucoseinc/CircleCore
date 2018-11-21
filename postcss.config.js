module.exports = ({env, file, options}) => {
  let plugins = [
    require('postcss-import'),
    require('postcss-mixins'),
    require('postcss-preset-env')(),
  ]

  if(env === 'staging' || env === 'production') {
    plugins.push(require('cssnano'))
  }

  return {
    plugins,
  }
}
