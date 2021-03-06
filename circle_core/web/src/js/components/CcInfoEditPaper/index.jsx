import PropTypes from 'prop-types'
import React from 'react'

import Paper from 'material-ui/Paper'

import ComponentWithOkButton from 'src/components/bases/ComponentWithOkButton'

import IdLabel from 'src/components/commons/IdLabel'

import DisplayNameTextField from 'src/components/commons/DisplayNameTextField'
import WorkTextField from 'src/components/commons/WorkTextField'


/**
 * CircleCoreInfo編集コンポーネント
 */
class CcInfoEditPaper extends React.Component {
  static propTypes = {
    ccInfo: PropTypes.object.isRequired,
    onUpdateClick: PropTypes.func,
  }

  /**
   * @override
   */
  constructor(props) {
    super(props)
    this.state = {
      editingCcInfo: this.props.ccInfo,
    }
  }

  /**
   * @override
   */
  render() {
    const {
      editingCcInfo,
    } = this.state
    const {
      onUpdateClick,
    } = this.props

    const style = {
      root: {
        display: 'flex',
        flexFlow: 'column nowrap',
        padding: 24,
      },

      contents: {
        display: 'flex',
        flexFlow: 'column nowrap',
      },

      displayNameArea: {
      },
      id: {
        fontSize: 14,
        lineHeight: 1,
      },

      workArea: {
        paddingTop: 16,
      },
    }


    return (
      <Paper>
        <div style={style.root}>
          <ComponentWithOkButton
            okButtonLabel="更新する"
            onOKButtonClick={() => onUpdateClick(editingCcInfo)}
          >
            <div style={style.contents}>
              <div style={style.displayNameArea}>
                <IdLabel
                  obj={editingCcInfo}
                />
                <DisplayNameTextField
                  obj={editingCcInfo}
                  floatingLabelText="CircleCore名"
                  onChange={(e) => this.setState({editingCcInfo: editingCcInfo.updateDisplayName(e.target.value)})}
                />
              </div>
              <div style={style.workArea}>
                <WorkTextField
                  obj={editingCcInfo}
                  onChange={(e) => this.setState({editingCcInfo: editingCcInfo.updateWork(e.target.value)})}
                />
              </div>
            </div>
          </ComponentWithOkButton>
        </div>
      </Paper>
    )
  }
}


export default CcInfoEditPaper
