import React from 'react'
import ReactDOM from 'react-dom'
import MuiThemeProvider from 'material-ui/styles/MuiThemeProvider'


import RaisedButton from 'material-ui/RaisedButton'


class CCApp extends React.Component {

  render() {
    return (
      <div className="hogehoge">
        hogehoge
         <RaisedButton label="Default" />
      </div>
    )
  }
}



ReactDOM.render(
  <MuiThemeProvider>
    <CCApp />
  </MuiThemeProvider>,
  document.getElementById('app')
)
