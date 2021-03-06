import PropTypes from 'prop-types'
import React from 'react'

import {blue500} from 'material-ui/styles/colors'

import ComponentWithIcon from 'src/components/bases/ComponentWithIcon'
import LabelWithCopyButton from 'src/containers/bases/LabelWithCopyButton'
import {ReplicationLinkIcon} from 'src/components/bases/icons'


/**
 * URLラベル
 */
class UrlLabel extends React.Component {
  static propTypes = {
    obj: PropTypes.object.isRequired,
  }

  /**
   * @override
   */
  render() {
    const {
      obj,
    } = this.props

    const style = {
      label: {
        fontWeight: 'bold',
        color: blue500,
        lineHeight: 1.4,
      },
    }
    return (
      <ComponentWithIcon icon={ReplicationLinkIcon}>
        <LabelWithCopyButton
          label={obj.url}
          labelStyle={style.label}
          messageWhenCopying="URLをコピーしました"
        />
      </ComponentWithIcon>
    )
  }
}

export default UrlLabel
