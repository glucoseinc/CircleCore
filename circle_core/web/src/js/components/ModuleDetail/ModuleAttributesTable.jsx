import PropTypes from 'prop-types'
import React from 'react'

import {grey300, grey400} from 'material-ui/styles/colors'


/**
* ModuleAttributesテーブル
*/
class ModuleAttributesTable extends React.Component {
  static propTypes = {
    module: PropTypes.object.isRequired,
  }

  /**
   * @override
   */
  render() {
    const {
      module,
    } = this.props

    const style = {
      table: {
        width: '100%',
        borderCollapse: 'collapse',
      },
      thead: {
        fontSize: 12,
        color: grey400,
        textAlign: 'left',
        borderTopWidth: 1,
        borderTopStyle: 'solid',
        borderTopColor: grey300,
        borderBottomWidth: 1,
        borderBottomStyle: 'solid',
        borderBottomColor: grey300,
      },
      td: {
        padding: '8px 16px',
      },
    }

    return (
      <table style={style.table}>
        <thead style={style.thead}>
          <tr>
            <th style={style.td}>属性名</th>
            <th style={style.td}>属性値</th>
          </tr>
        </thead>
        <tbody>
          {module.attributes.valueSeq().map((attribute, index) => {
            const trStyle = {
              backgroundColor: index % 2 ? grey300 : null,
            }
            return (
              <tr key={index} style={trStyle}>
                <td style={style.td}>{attribute.name}</td>
                <td style={style.td}>{attribute.value}</td>
              </tr>
            )
          })}
        </tbody>
      </table>
    )
  }
}


export default ModuleAttributesTable
