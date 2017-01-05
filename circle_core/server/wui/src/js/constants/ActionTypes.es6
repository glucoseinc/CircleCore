import {LOCATION_CHANGE} from 'react-router-redux'

const actionTypes = {
  navDrawer: {
    toggleOpen: 'NAV_DRAWER_TOGGLE_OPEN',
  },
  schemas: {
    fetchRequested: 'SCHEMAS_FETCH_REQUESTED',
    fetchSucceeded: 'SCHEMAS_FETCH_SUCCEEDED',
    fetchFailed: 'SCHEMAS_FETCH_FAILED',
  },
  schema: {
    update: 'SCHEMA_UPDATE',
    createInit: 'SCHEMA_CREATE_INIT',
    createRequested: 'SCHEMA_CREATE_REQUESTED',
    createSucceeded: 'SCHEMA_CREATE_SUCCEEDED',
    createFailed: 'SCHEMA_CREATE_FAILED',

    deleteAsked: 'SCHEMA_DELETE_ASKED',
    deleteCanceled: 'SCHEMA_DELETE_CANCELED',
    deleteRequested: 'SCHEMA_DELETE_REQUESTED',
    deleteSucceeded: 'SCHEMA_DELETE_SUCCEEDED',
    deleteFailed: 'SCHEMA_DELETE_FAILED',


    propertyTypes: {
      fetchRequested: 'SCHEMA_PROPERTY_TYPE_FETCH_REQUESTER',
      fetchSucceeded: 'SCHEMA_PROPERTY_TYPE_FETCH_SUCCEEDED',
      fetchFailed: 'SCHEMA_PROPERTY_TYPE_FETCH_FAILED',
    },
  },
  location: {
    changeRequested: 'LOCATION_CHANGE_REQUESTED',
    changeCanceled: 'LOCATION_CHANGE_CANCELED',
    change: LOCATION_CHANGE,
  },
}

export default actionTypes
