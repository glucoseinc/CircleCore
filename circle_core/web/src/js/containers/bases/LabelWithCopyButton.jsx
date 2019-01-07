import PropTypes from 'prop-types'
import React from 'react'
import {connect} from 'react-redux'

import IconButton from 'material-ui/IconButton'
import {grey500} from 'material-ui/styles/colors'

import actions from 'src/actions'

import {CopyIcon} from 'src/components/bases/icons'


/**
 * Clipboard copy用のテキストエリア
 */
class HiddenTextArea extends React.Component {
  static propTypes = {
    text: PropTypes.string.isRequired,
  }

  constructor(props) {
    super(props)
    this.textareaRef = React.createRef()
  }

  copy() {
    if (!this.textareaRef.current) {
      console.error('TEXTAREA not refrenced')
      return
    }

    const node = this.textareaRef.current

    node.focus()
    node.select()
    document.execCommand('copy')
    node.blur()
  }

  /**
   * @override
   */
  render() {
    const style = {
      width: 0,
      height: 0,
      position: 'fixed',
      top: -10000,
      left: -10000,
    }
    return (
      <textarea readOnly={true} style={style} value={this.props.text} ref={this.textareaRef} />
    )
  }
}

/**
 * Copyボタン付きラベル
 */
class LabelWithCopyButton extends React.Component {
  static propTypes = {
    style: PropTypes.object,
    label: PropTypes.string.isRequired,
    labelStyle: PropTypes.object,
    messageWhenCopying: PropTypes.string.isRequired,
    copyButtonOnly: PropTypes.bool,
    onClick: PropTypes.func,
  }

  constructor(props) {
    super(props)

    this.hiddenTextAreaRef = React.createRef()
  }

  /**
   * コピーボタン押下時、クリップボードにUUIDをコピーし親にイベントを送る
   */
  onClick() {
    const {
      messageWhenCopying,
      onClick,
    } = this.props

    if (!this.hiddenTextAreaRef.current) {
      console.error('HiddenTextArea not refrenced')
      return
    }

    this.hiddenTextAreaRef.current.copy()

    onClick && onClick(messageWhenCopying)
  }

  /**
   * @override
   */
  render() {
    const {
      style,
      label,
      labelStyle = {},
      copyButtonOnly = false,
    } = this.props

    const styles = {
      root: {
        display: 'flex',
        flexFlow: 'row nowrap',
        alignItems: 'center',
      },

      label: {
        fontSize: 12,
        lineHeight: 1,
        color: grey500,
      },

      iconButton: {
        width: 20,
        height: 16,
        padding: 0,
        paddingLeft: 4,
      },
      icon: {
        width: 16,
        height: 16,
      },
    }

    const mergedLabelStyle = {
      ...styles.label,
      ...labelStyle,
    }

    const labelArea = copyButtonOnly ? (
      null
    ) : (
      <div style={mergedLabelStyle}>{label}</div>
    )

    return (
      <div style={{...styles.root, ...(style || {})}}>
        <HiddenTextArea text={label} ref={this.hiddenTextAreaRef} />
        {labelArea}
        <IconButton
          style={styles.iconButton}
          iconStyle={styles.icon}
          onClick={() => this.onClick()}
        >
          <CopyIcon color={grey500} />
        </IconButton>
      </div>
    )
  }
}


const mapStateToProps = (state) => ({
})

const mapDispatchToProps = (dispatch) => ({
  onClick: (message) => dispatch(actions.page.showSnackbar(message)),
})

export default connect(
  mapStateToProps,
  mapDispatchToProps,
)(LabelWithCopyButton)
