import {combineReducers} from 'redux'
import {routerReducer as routing} from 'react-router-redux'


// load action groups
let reducers = {routing}
const reducerFiles = [
  'asyncs',
  'auth',
  'entities',
  'misc',
  'page',
]
reducerFiles.forEach((reducerFile) => reducers[reducerFile] = require(`./${reducerFile}`).default)

const rootReducer = combineReducers(reducers)

export default rootReducer
