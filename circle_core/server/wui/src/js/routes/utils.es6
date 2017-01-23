import path from 'path'

import {formatPattern} from 'react-router'

import Root from './Root'


const createURLs = (route, parentPath = '') => {
  let urls = {}

  if (route.key !== undefined) {
    urls[route.key] = {
      fullPath: path.join(parentPath, route.path || ''),
      label: route.label,
      icon: route.icon,
    }
  }
  if (route.childRoutes !== undefined) {
    urls = route.childRoutes.reduce((_urls, childRoute) => ({
      ..._urls,
      ...createURLs(childRoute, path.join(parentPath, route.path || '')),
    }), urls)
  }

  return urls
}

export const urls = createURLs(Root)

export const createPathName = (url, params) => {
  return formatPattern(url.fullPath, params)
}
