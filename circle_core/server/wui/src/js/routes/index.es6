import path from 'path'

import React from 'react'

import Master from './Master'

const rootRoute = {
  childRoutes: [
    Master,
  ],
}

export default rootRoute


const createURLs = (route, parentPath = '') => {
  let urls = {}

  if (route.key !== undefined) {
    urls[route.key] = {
      fullPath: path.join(parentPath, route.path),
      label: route.label,
    }
  }

  if (route.childRoutes !== undefined) {
    urls = route.childRoutes.reduce((_urls, childRoute) => ({
      ..._urls,
      ...createURLs(childRoute, route.path),
    }), urls)
  }
  return urls
}

export const urls = createURLs(rootRoute)
