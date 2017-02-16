import React, {Component, PropTypes} from 'react'

import Paper from 'material-ui/Paper'
import {grey300, grey600, grey900, white} from 'material-ui/styles/colors'


const tableStyle = {
  root: {
    display: 'flex',
    flexFlow: 'row nowrap',
    width: '100%',
    lineHeight: 1,
  },
  cell: {
    flexGrow: 1,
    padding: '16px 24px',
    width: '50%',
  },
}


/**
* 共有項目テーブルのヘッダ
*/
class ReplicationTargetsTableHeader extends Component {
  static propTypes = {
  }

  /**
   * @override
   */
  render() {
    const style = {
      root: {
        ...tableStyle.root,
        fontSize: 12,
        color: grey600,
      },
      cell: {
        ...tableStyle.cell,
        paddingTop: 9,
        paddingBottom: 16,
      },
    }

    return (
      <div style={style.root}>
        <div style={style.cell}>モジュール名</div>
        <div style={style.cell}>メッセージボックス名</div>
      </div>
    )
  }
}


/**
* 共有項目テーブルのロウ
*/
class ReplicationTargetsTableRow extends Component {
  static propTypes = {
    messageBoxes: PropTypes.array.isRequired,
    module: PropTypes.object.isRequired,
    backgroundColor: PropTypes.string,
  }

  /**
   * @override
   */
  render() {
    const {
      messageBoxes,
      module,
      backgroundColor,
    } = this.props

    const style = {
      root: {
        ...tableStyle.root,
        fontSize: 14,
        backgroundColor,
      },
      module: {
        ...tableStyle.cell,
        fontWeight: 'bold',
        color: grey900,
      },
      messageBoxes: {
        ...tableStyle.cell,
        display: 'flex',
        flexFlow: 'column nowrap',
        marginTop: -4,
        color: grey600,
      },
      messageBox: {
        paddingTop: 4,
      },
    }


    return (
      <div style={style.root}>
        <div style={style.module}>{module.displayName}</div>
        <div style={style.messageBoxes}>
          {messageBoxes.map((messageBox) =>
            <div key={messageBox.uuid} style={style.messageBox}>
              {messageBox.displayName}
            </div>
          )}
        </div>
      </div>
    )
  }
}


/**
* 共有項目テーブルコンポーネント
*/
class ReplicationTargetsTableComponent extends Component {
  static propTypes = {
    messageBoxes: PropTypes.object.isRequired,
    modules: PropTypes.object.isRequired,
  }

  /**
   * @override
   */
  render() {
    const {
      messageBoxes,
      modules,
    } = this.props

    const style = {
      root: {
        display: 'flex',
        flexFlow: 'column nowrap',
      },
      header: {
        display: 'flex',
        flexFlow: 'row nowrap',
      },
      row: {
        display: 'flex',
        flexFlow: 'row nowrap',
      },
    }

    const targetModules = messageBoxes.reduce((m, messageBox) => {
      if(!m.hasOwnProperty(messageBox.module)) {
        m[messageBox.module] = {
          module: modules.get(messageBox.module),
          messageBoxes: [],
        }
      }
      m[messageBox.module].messageBoxes.push(messageBox)
      return m
    }, {})

    return (
      <div style={style.root}>
        <div style={style.header}>
          <ReplicationTargetsTableHeader />
        </div>
        <Paper>
          {Object.values(targetModules).map(({module, messageBoxes}, index) => {
            return <div key={module.uuid} style={style.row}>
              <ReplicationTargetsTableRow
                module={module}
                messageBoxes={messageBoxes}
                backgroundColor={index % 2 ? white : grey300}
              />
            </div>
          })}
        </Paper>
      </div>
    )
  }
}

export default ReplicationTargetsTableComponent
