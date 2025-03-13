export function formatDatetime(str: string) {
  return `${str.split('T')[0]} ${str.split('T')[1].split(':').slice(0, 2).join(':')}`
}
