import React, {Component, PropTypes} from 'react'

import Paper from 'material-ui/Paper'
import {grey300, grey600, grey900, white} from 'material-ui/styles/colors'

const style = {
  root: {
    display: 'flex',
    flexFlow: 'row nowrap',
    width: '100%',
    lineHeight: 1,
  },
  cell: {
    flexGrow: 1,
    padding: '17px 24px',
    width: '50%',
  },
}

/**
 * プロパティ情報テーブルのヘッダ
 */
export class PropertyHeader extends Component {
  static propTypes = {
  }

  /**
   * @override
   */
  render() {
    const rootStyle = {
      ...style.root,
      fontSize: 12,
      color: grey600,
    }
    const cellStyle = {
      ...style.cell,
      paddingTop: 9,
      paddingBottom: 16,
    }

    return (
      <div style={rootStyle}>
        <div style={cellStyle}>属性名</div>
        <div style={cellStyle}>属性タイプ</div>
      </div>
    )
  }
}


/**
 * プロパティ情報テーブルのロウ
 */
class PropertyRow extends Component {
  static propTypes = {
    property: PropTypes.object.isRequired,
    backgroundColor: PropTypes.string,
  }

  /**
   * @override
   */
  render() {
    const {
      property,
      backgroundColor,
    } = this.props

    const rootStyle = {
      ...style.root,
      fontSize: 14,
      color: grey900,
      backgroundColor,
    }
    const cellStyle = {
      ...style.cell,
    }

    return (
      <div style={rootStyle}>
        <div style={cellStyle}>{property.name}</div>
        <div style={cellStyle}>{property.type}</div>
      </div>
    )
  }
}


/**
 * プロパティテーブルコンポーネント
 */
class PropertiesTableComponent extends Component {
  static propTypes = {
    schema: PropTypes.object.isRequired,
  }

  /**
   * @override
   */
  render() {
    const {
      schema,
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

    return (
      <div style={style.root}>
        <div>
          <div style={style.header}>
            <PropertyHeader />
          </div>
          <Paper>
            {schema.properties.valueSeq().map((property, index) => {
              const backgroundColor = index % 2 ? white :grey300
              return (
                <div key={index} style={style.row}>
                  <PropertyRow
                    property={property}
                    backgroundColor={backgroundColor}
                  />
                </div>
              )
            })}
          </Paper>
        </div>
      </div>
    )
  }
}


export default PropertiesTableComponent
