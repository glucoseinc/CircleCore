import React, {Component, PropTypes} from 'react'

import ComponentWithTitle from 'src/components/bases/ComponentWithTitle'
import DisplayNamePaper from 'src/components/commons/DisplayNamePaper'

import UserInfoPaper from './UserInfoPaper'


/**
* User詳細コンポーネント
*/
class UserDetail extends Component {
  static propTypes = {
    user: PropTypes.object.isRequired,
  }

  /**
   * @override
   */
  render() {
    const {
      user,
    } = this.props

    const style = {
      root: {
        display: 'flex',
        flexFlow: 'column nowrap',
      },

      displayNamePaper: {
      },

      infoArea: {
        paddingTop: 32,
      },

    }

    return (
      <div style={style.root}>
        <div style={style.displayNamePaper}>
          <DisplayNamePaper
            obj={user}
            secondaryType="id"
          />
        </div>

        <div style={style.infoArea}>
          <ComponentWithTitle title="ユーザー情報">
            <UserInfoPaper user={user} />
          </ComponentWithTitle>
        </div>
      </div>
    )
  }
}


export default UserDetail
