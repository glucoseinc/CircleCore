import React, {Component, PropTypes} from 'react'
import {findDOMNode} from 'react-dom'

import IconButton from 'material-ui/IconButton'
import {grey500} from 'material-ui/styles/colors'

import ComponentWithIcon from 'src/components/bases/ComponentWithIcon'
import {IdIcon, CopyIcon} from 'src/components/bases/icons'


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
 * IDラベル
 */
class IdLabel extends Component {
  static propTypes = {
    obj: PropTypes.object.isRequired,
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
    this.props.onTouchTap(this.props.obj.uuid)
  }


  /**
   * @override
   */
  render() {
    const {
      obj,
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

    return (
      <ComponentWithIcon icon={IdIcon}>
        <HiddenTextArea text={obj.uuid} ref="hiddenTextArea"/>
        <div style={style.root}>
          <div style={style.label}>{obj.uuid}</div>
          <IconButton
            style={style.iconButton}
            iconStyle={style.icon}
            onTouchTap={::this.onTouchTap}
          >
            <CopyIcon color={grey500}/>
          </IconButton>
        </div>
      </ComponentWithIcon>
    )
  }
}

export default IdLabel
