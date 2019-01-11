import PropTypes from 'prop-types'
import React from 'react'

import LabelWithCopyButton from 'src/containers/bases/LabelWithCopyButton'
import CCFlatButton from 'src/components/bases/CCFlatButton'


/**
* トークンコンポーネント
*/
class TokenComponent extends React.Component {
  static propTypes = {
    onGenerate: PropTypes.func,
    token: PropTypes.string,
  }

  /**
   * @override
   */
  render() {
    const {
      onGenerate,
      token,
    } = this.props

    const style = {
      root: {
        display: 'flex',
        flexFlow: 'column nowrap',
        width: '100%',
      },

      labelArea: {
        paddingTop: 8,
      },

      label: {
        wordBreak: 'break-all',
        paddingRight: 16,
      },

      actionsArea: {
        paddingTop: 16,
      },
    }

    return (
      <div style={style.root}>
        <div style={style.labelArea}>
          {token ? (
            <LabelWithCopyButton
              label={token}
              labelStyle={style.label}
              messageWhenCopying="トークンをコピーしました"
            />
          ) : (
            '未生成'
          )}
        </div>

        <div style={style.actionsArea}>
          <CCFlatButton
            label={`トークンを${token && '再'}生成する`}
            primary={true}
            onClick={onGenerate}
          />
        </div>
      </div>
    )
  }
}


export default TokenComponent
