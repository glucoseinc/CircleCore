import gulp from 'gulp'
import eslint from 'gulp-eslint'
import gzip from 'gulp-gzip'
import notifier from 'node-notifier'
import runSequence from 'run-sequence'
import named from 'vinyl-named'
import webpack from 'webpack-stream'
import shell from 'gulp-shell'
import postcss from 'gulp-postcss'
import del from 'del'
import plumber from 'gulp-plumber'


const DESTINATION_DIR = './circle_core/server/wui/static'
const BROWSER_LIST = ['last 2 versions', 'iOS >= 8', 'Android >= 4.0']


gulp.task('default', (cb) => {
  return runSequence(['script', 'style'], cb)
})

gulp.task('script', (cb) => {
  return runSequence('lint', 'clean_script', 'babel', cb)
})

gulp.task('clean_script', del.bind(null, [`${DESTINATION_DIR}/*.js`]))

gulp.task('lint', () => {
  return gulp.src(['src/js/**/*.es6']) // lint のチェック先を指定
    .pipe(plumber({
      // エラーをハンドル
      errorHandler: function(error) {
        // var taskName = 'eslint'
        // var title = '[task]' + taskName + ' ' + error.plugin
        // var errorMsg = 'error: ' + error.message
        // // ターミナルにエラーを出力
        // console.error(title + '\n' + errorMsg)
        // // エラーを通知
        // notifier.notify({
        //   title: title,
        //   message: errorMsg,
        //   time: 3000
        // })
      },
    }))
    .pipe(eslint({eslintrc: true})) // .eslintrc を参照
    .pipe(eslint.format())
    .pipe(eslint.failOnError())
    .pipe(plumber.stop())
})

gulp.task('babel', () => {
  return gulp.src(['src/js/main.es6'])
    .pipe(named())
    .pipe(webpack(require('./webpack.config.js'), null, (err, stats) => {
      if(!err) {
        let elapsedTime = (stats.endTime - stats.startTime) / 1000.
        notifier.notify({
          title: 'gulp scripts',
          message: `Webpack build. ${elapsedTime}secs`
        })
      } else {
        notifier.notify({
          title: 'gulp scripts',
          message: 'Error on `scripts`: <%= err %>',
        })
      }
    }))
    .pipe(gulp.dest(DESTINATION_DIR))
})


gulp.task('style', () => {
  return gulp.src(['src/css/main.css'])
    .pipe(postcss([
      require('postcss-import'),
      require('postcss-mixins'),
      require('postcss-nested'),
      require('postcss-color-function'),
      require('postcss-simple-vars'),
      require('postcss-cssnext')({browsers: BROWSER_LIST}),
      // require('postcss-asset-hash')({
      //   assets_directories: [dest]
      // })
    ]))
    .pipe(gulp.dest(DESTINATION_DIR))
})


gulp.task('watch', () => {
  gulp.watch(['src/js/*.es6', 'src/js/**/*.es6'], ['script'])
  gulp.watch(['src/css/**/*.css', 'assets/css/common.css'], ['style'])
})
