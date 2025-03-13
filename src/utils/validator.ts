const EMAIL_ADDRESS_REG = /^[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$/

export function validateEmailAddress(emailAddress: string): boolean {
  return EMAIL_ADDRESS_REG.test(emailAddress)
}
