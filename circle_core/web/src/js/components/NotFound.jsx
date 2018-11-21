import React from 'react'
import {Link} from 'react-router'
import Title from '@shnjp/react-title-component'

import AppBar from 'material-ui/AppBar'
import Paper from 'material-ui/Paper'
import {blue500, grey700} from 'material-ui/styles/colors'

import CCFlatButton from 'src/components/bases/CCFlatButton'


/**
 * 404 Not Found
 */
class NotFound extends React.Component {
  static propTypes = {
  }

  /**
   *@override
   */
  render() {
    const style = {
      root: {
        padding: 24,
      },

      contents: {
        display: 'flex',
        flexFlow: 'column nowrap',
        alignItems: 'center',
      },
      primaryLabel: {
        paddingTop: 64,
        fontSize: 24,
        fontWeight: 'bold',
        lineHeight: 1,
        color: blue500,
      },
      secondaryLabel: {
        paddingTop: 16,
        fontSize: 14,
        lineHeight: 1,
        color: grey700,
      },
      button: {
        paddingTop: 40,
        paddingBottom: 40,
      },
    }

    return (
      <div>
        <Title render="CircleCore" />
        <AppBar
          title="CircleCore"
          showMenuIconButton={false}
        />
        <div style={style.root}>
          <Paper>
            <div style={style.contents}>
              <div style={style.primaryLabel}>404 Not Found</div>
              <div style={style.secondaryLabel}>お探しのページは見つかりませんでした。</div>
              <div style={style.button}>
                <Link to="/">
                  <CCFlatButton
                    label="トップへ戻る"
                    primary={true}
                  />
                </Link>
              </div>
            </div>
          </Paper>
        </div>
      </div>
    )
  }
}

export default NotFound
