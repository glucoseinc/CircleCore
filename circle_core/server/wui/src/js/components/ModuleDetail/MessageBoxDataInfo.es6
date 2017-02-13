import React, {Component, PropTypes} from 'react'

import {grey300, grey400} from 'material-ui/styles/colors'


// TODO: Dataの取得
const mockHeader = [
  '日付',
  '項目名01',
  '項目名02項目名02',
  '項目名03項目名03項目名03',
  '項目名04項目名04項目名04項目名04項目名04項目名04項目名04項目名04項目名04項目名04項目名04項目名04項目名04項目名04項目名04項目名04',
]
const mockData = [
  [
    '2017/01/01 12:34',
    '12.345',
    '12.345',
    '12.345',
    '12.345',
  ],
  [
    '2017/01/01 12:34',
    '12.345',
    '12.345',
    '12.345',
    '12.345',
  ],
  [
    '2017/01/01 12:34',
    '12.345',
    '12.345',
    '12.345',
    '12.345',
  ],
  [
    '2017/01/01 12:34',
    '12.345',
    '12.345',
    '12.345',
    '12.345',
  ],
  [
    '2017/01/01 12:34',
    '12.345',
    '12.345',
    '12.345',
    '12.345',
  ],
]

/**
* MessageBox更新情報
*/
class MessageBoxDataInfo extends Component {
  static propTypes = {
    header: PropTypes.array,
    data: PropTypes.array,
    width: PropTypes.number,
  }

  /**
   * @override
   */
  render() {
    const {
      header = mockHeader,
      data = mockData,
      width = 0,
    } = this.props

    const style = {
      root: {
        width,
        overflowX: 'scroll',
      },
      table: {
        borderCollapse: 'collapse',
      },
      headerRow: {
        borderTopStyle: 'solid',
        borderTopWidth: 1,
        borderTopColor: grey300,
        borderBottomStyle: 'solid',
        borderBottomWidth: 1,
        borderBottomColor: grey300,
      },
      headerCell: {
        padding: 8,
        fontSize: 12,
        fontWeight: 'normal',
        color: grey400,
        whiteSpace: 'nowrap',
      },
      dataRowOdd: {
        backgroundColor: grey300,
      },
      dataRowEven: {
      },
      dataCell: {
        padding: 8,
        fontSize: 14,
        whiteSpace: 'nowrap',
      },
    }

    return (
      <div style={style.root}>
        <table style={style.table}>
          <thead>
            <tr style={style.headerRow}>
              {header.map((h, index) =>
                <th key={index} style={style.headerCell}>{h}</th>
              )}
            </tr>
          </thead>
          <tbody>
            {data.map((row, index) =>
              <tr key={index} style={index % 2 ? style.dataRowOdd : style.dataRowEven}>
                {row.map((cell, i) =>
                  <td key={i} style={style.dataCell}>{cell}</td>
                )}
              </tr>
            )}
          </tbody>
        </table>
      </div>
    )
  }
}


export default MessageBoxDataInfo
