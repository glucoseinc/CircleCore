import path from 'path'

import {formatPattern} from 'react-router'

import Root from './Root'


const createURLs = (route, parentPath = '') => {
  let urls = {}

  if (route.key !== undefined) {
    urls[route.key] = {
      fullPath: path.join(parentPath, route.path || ''),
      query: route.query,
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

export const createQuery = (url, params) => {
  if (url.query === undefined || params === undefined) {
    return null
  }

  return Object.entries(url.query).reduce((query, [key, value]) => {
    try {
      return {
        ...query,
        [key]: formatPattern(value, params),
      }
    } catch (e) {
      return query
    }
  }, {})
}
