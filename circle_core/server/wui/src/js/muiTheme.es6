import getMuiTheme from 'material-ui/styles/getMuiTheme'
import {blue500, blue700, redA200} from 'material-ui/styles/colors'

const muiTheme = {
  fontFamily: 'Roboto, Hiragino Kaku Gothic ProN, ヒラギノ角ゴ ProN W3, Meiryo, ' +
              'メイリオ, Osaka, MS PGothic, arial, helvetica, sans-serif',
  palette: {
    accent1Color: redA200, // <- pinkA200,
    // accent2Color: grey100,
    // accent3Color: grey500,
    // alternateTextColor: white,
    // borderColor: grey300,
    // canvasColor: white,
    // clockCircleColor: 'rgba(0, 0, 0, 0.07)',
    // disabledColor: 'rgba(0, 0, 0, 0.3)',
    // pickerHeaderColor: cyan500,
    primary1Color: blue500, // <- cyan500,
    primary2Color: blue700, // <- cyan700,
    // primary3Color: grey400,
    // secondaryTextColor: lightBlack,
    // shadowColor: fullBlack,
    // textColor: darkBlack,
  },
  tableRow: {
    height: 56,
  },
  tableRowColumn: {
    height: 56,
  },
}

export default getMuiTheme(muiTheme)
