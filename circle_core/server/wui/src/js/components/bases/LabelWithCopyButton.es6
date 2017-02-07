import React, {Component, PropTypes} from 'react'
import {findDOMNode} from 'react-dom'

import IconButton from 'material-ui/IconButton'
import {grey500} from 'material-ui/styles/colors'

import {CopyIcon} from 'src/components/bases/icons'


/**
 * Clopboard copy用のテキストエリア
 */
class HiddenTextArea extends Component {
  static propTypes = {
    text: PropTypes.string.isRequired,
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
      <textarea readOnly={true} style={style} value={this.props.text} />
    )
  }
}

/**
 * Copyボタン付きラベル
 */
class LabelWithCopyButton extends Component {
  static propTypes = {
    label: PropTypes.string.isRequired,
    labelStyle: PropTypes.object,
    onTouchTap: PropTypes.func,
  }

  /**
   * コピーボタン押下時、クリップボードにUUIDをコピーし親にイベントを送る
   * @param {object} e
   */
  onTouchTap(e) {
    const dom = findDOMNode(this.refs.hiddenTextArea)
    dom.focus()
    dom.select()
    document.execCommand('copy')
    dom.blur()
    this.props.onTouchTap(this.props.label)
  }


  /**
   * @override
   */
  render() {
    const {
      label,
      labelStyle = {},
    } = this.props

    const style = {
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
        width: 16,
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
      ...style.label,
      ...labelStyle,
    }

    return (
      <div style={style.root}>
        <HiddenTextArea text={label} ref="hiddenTextArea"/>
        <div style={mergedLabelStyle}>{label}</div>
        <IconButton
          style={style.iconButton}
          iconStyle={style.icon}
          onTouchTap={::this.onTouchTap}
        >
          <CopyIcon color={grey500}/>
        </IconButton>
      </div>
    )
  }
}

export default LabelWithCopyButton
