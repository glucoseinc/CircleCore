import React, {Component, PropTypes} from 'react'
import moment from 'moment'

import CCAPI from 'src/api'
import {SchemaPropertyLabel} from 'src/components/commons/SchemaPropertiesLabel'


/**
 * MessageBoxDataInfoのメッセージ1行分
 */
class MessageRow extends Component {
  static propTypes = {
    message: PropTypes.object.isRequired,
    schemaProperties: PropTypes.array.isRequired,
  }

  /**
   * @override
   */
  render() {
    const {
      message,
      schemaProperties,
    } = this.props

    const date = moment.unix(message.timestamp)

    return (
      <tr>
        <td className="messageBox-latestMessages-date">{date.toISOString()}</td>
        <td className="messageBox-latestMessages-timestamp">{message.timestamp}</td>
        <td className="messageBox-latestMessages-counter">{message.counter}</td>
        {schemaProperties.map(({name, type}) => (
          <td
            key={`${name}-${type}`}
            className={`messageBox-latestMessages-value is-${type}`}>
            {valueToString(message.payload[name], type)}
          </td>
        ))}
      </tr>
    )
  }
}

/**
 * データを表示も列に変更
 * @param {object} val
 * @param {string} type
 * @return {string}
 */
function valueToString(val, type) {
  return '' + val
}

/**
* MessageBox更新情報
*/
class MessageBoxDataInfo extends Component {
  static propTypes = {
    messageBox: PropTypes.object.isRequired,
    module: PropTypes.object.isRequired,
  }

  state = {
    loading: true,
    messages: null,
  }

  /**
   * @override
   */
  componentDidMount() {
    this.fetchLatestData()
  }

  /**
   * @override
   */
  render() {
    if(this.state.loading) {
      return <div>loading...</div>
    }

    const {
      messages,
      schemaProperties,
    } = this.state

    return (
      <div className="messageBox-latestMessages">
        <table>
          <thead>
            <tr>
              <th className="messageBox-latestMessages-date">
                日付
              </th>
              <th className="messageBox-latestMessages-timestamp">
                timestamp
              </th>
              <th className="messageBox-latestMessages-counter">
                counter
              </th>
              {schemaProperties.map(({name, type}, index) =>
                <th key={index} className="messageBox-latestMessages-value">
                  <SchemaPropertyLabel name={name} type={type} style={{fontSize: 'inherit'}}/>
                </th>
              )}
            </tr>
          </thead>
          <tbody>
            {messages.length
              ? messages.map((message, index) =>
                  <MessageRow
                    key={index} message={message} schemaProperties={schemaProperties} />
                )
              : (
                <tr>
                  <td className="messageBox-latestMessages-nodata" colSpan={3 + schemaProperties.length}>NO DATA</td>
                </tr>
              )
            }
          </tbody>
        </table>
      </div>
    )
  }

  /**
   * サーバから最新メッセージをとってくる
   */
  async fetchLatestData() {
    let {messages, schema: {properties}} = await CCAPI.fetchLatestMessageBox(
      this.props.module.uuid,
      this.props.messageBox.uuid
    )

    this.setState({
      loading: false,
      messages: messages,
      schemaProperties: properties,
    })
  }
}


export default MessageBoxDataInfo
