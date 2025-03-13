export function getAccessToken() {
  return localStorage.getItem('account_access_token') ?? void 0
}

export function validateAccessToken() {
  return !!localStorage.getItem('account_access_token')
}

export function deleteAccessToken() {
  localStorage.removeItem('account_access_token')
}

export function saveAccessToken(token: string) {
  localStorage.setItem('account_access_token', token)
}
