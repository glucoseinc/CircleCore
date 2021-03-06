import PropTypes from 'prop-types'
import React from 'react'
import moment from 'moment'
import Rickshaw from 'rickshaw'

import CCAPI from 'src/api'
import LoadingIndicator from 'src/components/bases/LoadingIndicator'


const RANGE_30MINS = '30m'
const RANGE_1HOUR = '1h'
const RANGE_6HOURS = '6h'
const RANGE_1DAY = '1d'
const RANGE_7DAYS = '7d'
export const RANGES = [RANGE_30MINS, RANGE_1HOUR, RANGE_6HOURS, RANGE_1DAY, RANGE_7DAYS]
export const RANGE_LABELS = {
  [RANGE_30MINS]: '30分',
  [RANGE_1HOUR]: '1時間',
  [RANGE_6HOURS]: '6時間',
  [RANGE_1DAY]: '1日',
  [RANGE_7DAYS]: '7日',
}

// time zone offset in seconds
const TZ_OFFSET = (new Date()).getTimezoneOffset() * 60


/**
 * CircleCoreのグラフのX軸メモリ用の時間軸(日本語がおかしい)
 */
class GraphTime {
  /**
   * サポートしている単位系のリストを返す
   * @return {Array}
   */
  get units() {
    return [
      {
        name: RANGE_7DAYS,
        seconds: 60 * 60 * 24,
        formatter: (d) => moment(d).format('MM-DD'),
      }, {
        name: RANGE_1DAY,
        seconds: 60 * 60 * 12,
        formatter: ::this.format,
      }, {
        name: RANGE_6HOURS,
        seconds: 60 * 60 * 3,
        formatter: ::this.format,
      }, {
        name: RANGE_1HOUR,
        seconds: 60 * 30,
        formatter: ::this.format,
      }, {
        name: RANGE_30MINS,
        seconds: 60 * 15,
        formatter: ::this.format,
      },
    ]
  }

  /**
   * 単位系を返す
   * @param {str} unitName
   * @return {Object}
   */
  unit(unitName) {
    return this.units.filter((unit) => unitName == unit.name).shift()
  }

  /**
   * X軸の線のラベル
   * @param {Date} d
   * @return {str} ラベル
   */
  format(d) {
    // dはepochから生成しているので正しいTimezoneのはず
    return moment(d).format('YYYY-MM-DD<br/>HH:mm')
  }

  /**
   * 与えられた時間をまるめて、どのX軸ガイドに合わせるか決める
   * @param {float} time
   * @param {Object} unit 現在選択されている単位系
   * @return {float} まとめられた時間
   */
  ceil(time, unit) {
    // 時差を加味して丸めないと、違和感のある感覚になる
    time -= TZ_OFFSET
    time = Math.ceil(time / unit.seconds) * unit.seconds
    time += TZ_OFFSET
    return time
  }
}


/**
 * モジュールのグラフを描画するコンポーネント
 * MessageBoxを渡すとMessageBoxのグラフを書く
 * クラスを分けようと思ったのだけど、継承させて書くとちょっと面倒なので、ifで...
 */
class ModuleGraph extends React.Component {
  static propTypes = {
    autoUpdate: PropTypes.number,
    module: PropTypes.object.isRequired,
    messageBox: PropTypes.object,
    range: PropTypes.string.isRequired,
  }

  static defaultProps = {
    autoUpdate: 0,
  }

  /**
   * @constructor
   */
  constructor(...args) {
    super(...args)

    this.state = {
      graphData: null,
    }
    this.graph = null
    this.updateTimer = null

    this.graphContainerRef = React.createRef()
    this.yAxisRef = React.createRef()
    this.chartRef = React.createRef()
    this.previewRef = React.createRef()
    this.legendRef = React.createRef()
  }

  /**
   * @override
   */
  componentDidMount() {
    this.fetchGraphData(this.props.range)

    this.resizeHandler = ::this.onResize
    window.addEventListener('resize', this.resizeHandler)
  }

  /**
   * @override
   */
  componentWillReceiveProps(nextProps) {
    if (this.props.range != nextProps.range) {
      // rangeが変わったのでグラフデータ再取得
      this.setState({graphData: null})
      this.fetchGraphData(nextProps.range)
    }
  }

  /**
   * @override
   */
  componentWillUpdate(nextProps, nextState) {
    if (this.props.autoUpdate != nextProps.autoUpdate) {
      this.clearUpdateTimer()

      // グラフデータが既に取得済みであれば、タイマーを再設定
      if (nextState.graphData) {
        this.setUpdateTimer(nextProps.autoUpdate)
      }
    }
  }

  /**
   * @override
   */
  componentWillUnmount() {
    this.clearUpdateTimer()

    if (this.resizeHandler) {
      window.removeEventListener('resize', this.resizeHandler)
      delete this.resizeHandler
    }
  }


  /**
   * Legendを描画するか？
   * @return {bool}
   */
  get isShowLegend() {
    return this.props.messageBox ? false : true
  }

  /**
   * グラフのデータをサーバに取りに行く
   * @param {str} range '30m', '1h', ...
   */
  async fetchGraphData(range) {
    let request
    const query = {
      range: range,
      tzOffset: TZ_OFFSET * 60,
    }

    if (this.props.messageBox) {
      request = CCAPI.getMessageBoxGraphData(this.props.module, this.props.messageBox, query)
    } else {
      request = CCAPI.getModuleGraphData(this.props.module, query)
    }

    const {graphData} = await request

    this.setState({graphData}, () => {
      this.updateGraph()
      this.setUpdateTimer(this.props.autoUpdate)
    })
  }

  /**
   * データに基づいてグラフを再描画する
   */
  updateGraph() {
    const {
      range,
    } = this.props
    const {
      graphData,
    } = this.state

    if (!this.graphContainerRef.current || !graphData) {
      return
    }

    const palette = new Rickshaw.Color.Palette({scheme: 'colorwheel'})

    // remove graph if exists
    if (this.graph) {
      this.yAxisRef.current.innerHTML = ''
      this.chartRef.current.innerHTML = ''
      this.previewRef.current.innerHTML = ''
      if (this.isShowLegend) {
        this.legendRef.current.innerHTML = ''
      }
      delete this.graph
    }

    const graph = new Rickshaw.Graph({
      strokeWidth: 1,
      element: this.chartRef.current,
      renderer: 'line',
      series: graphData.map((gd) => {
        return {
          color: palette.color(),
          data: gd.data,
          name: gd.messageBox.displayName,
        }
      }),
    })
    const timeFixture = new GraphTime()
    new Rickshaw.Graph.Axis.Time({
      graph,
      timeFixture: timeFixture,
      timeUnit: timeFixture.unit(range),
    })
    new Rickshaw.Graph.Axis.Y({
      graph: graph,
      orientation: 'left',
      tickFormat: Rickshaw.Fixtures.Number.formatKMBT,
      element: this.yAxisRef.current,
    })
    new Rickshaw.Graph.RangeSlider.Preview({
      graph,
      height: 40,
      element: this.previewRef.current,
    })
    new Rickshaw.Graph.HoverDetail( {
      graph: graph,
    })
    if (this.isShowLegend) {
      new Rickshaw.Graph.Legend( {
        graph,
        element: this.legendRef.current,
      })
    }

    graph.render()
    this.graph = graph
  }

  /**
   * 表示領域のサイズが変更されたら呼ばれる
   */
  onResize() {
    // TODO:navDrawerのOpenが完了したタイミングで幅が変わるので、グラフがはみ出る...
    if (!this.chartRef.current) {
      return
    }

    const bb = this.chartRef.current.getBoundingClientRect()

    this.graph.configure({
      width: bb.width,
      height: bb.height,
    })
    this.graph.render()
  }

  /**
   * グラフ更新タイマーが設定されてあれば、キャンセルする
   */
  clearUpdateTimer() {
    if (this.updateTimer) {
      clearTimeout(this.updateTimer)
      this.updateTimer = null
    }
  }

  /**
   * グラフ更新タイマーが設定されてあれば、キャンセルする
   * @param {int} delay 間隔を秒で
   */
  setUpdateTimer(delay) {
    if (this.updateTimer) {
      console.warn('clearUpdateTimer@setUpdateTimer')
      this.clearUpdateTimer()
    }

    if (!delay) {
      return
    }
    this.updateTimer = setTimeout(() => {
      this.updateTimer = null
      this.fetchGraphData()
    }, delay * 1000)
  }

  /**
   * @override
   */
  render() {
    const {
      graphData,
    } = this.state

    return (
      <div
        ref={this.graphContainerRef}
        className={`graph graph-module ${graphData ? '' : 'is-loading'}`}
      >
        {!graphData && <LoadingIndicator className="graph-loadingIndicator" />}
        <div ref={this.yAxisRef} className="graph-yAxis" />
        <div ref={this.chartRef} className="graph-chart" />
        <div ref={this.previewRef} className="graph-preview" />
        {this.isShowLegend && <div ref={this.legendRef} className="graph-legend" />}
      </div>
    )
  }
}

export default ModuleGraph
