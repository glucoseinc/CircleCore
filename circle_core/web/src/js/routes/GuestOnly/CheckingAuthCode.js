import React from 'react'

const CheckingAuthCode = () => <div>Checking AuthCode...</div>

const checkingAuthCodeRoute = {
  key: 'checkingAuthCode',
  path: '/oauth/callback',
  component: CheckingAuthCode,
}

export default checkingAuthCodeRoute
