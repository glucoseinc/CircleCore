import React, {Component, PropTypes} from 'react'
import withWidth from 'material-ui/utils/withWidth'
import spacing from 'material-ui/styles/spacing'

import FullWidthSection from '../components/FullWidthSection'


/**
 * Homeページのレンダリング
 */
class HomePage extends Component {
  static propTypes = {
    width: PropTypes.number.isRequired,
  }

  static contextTypes = {
    router: PropTypes.object.isRequired,
  }

  /**
   * @override
   */
  render() {
    const style = {
      paddingTop: spacing.desktopKeylineIncrement,
    }

    return (
      <div style={style}>
        <FullWidthSection>Homeだよ</FullWidthSection>
      </div>
    )
  }
}

export default withWidth()(HomePage)
