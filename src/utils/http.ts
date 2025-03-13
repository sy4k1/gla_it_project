import { getAccessToken } from '@/utils/local_storage.ts'

export interface ISendRequestOptions {
  noAccessToken?: boolean
}

export interface ISendRequestData {
  access_token?: string
}

export interface IResponse<IRespData> {
  code: number
  message?: string
  data?: IRespData
}

export async function sendRequest<TReq, TRes>(
  path: string,
  options?: ISendRequestOptions,
  requestData?: TReq & ISendRequestData,
): Promise<IResponse<TRes>> {
  const req = requestData ?? ({} as TReq & ISendRequestData)
  if (!options?.noAccessToken) {
    req.access_token = getAccessToken()
  }
  const resp = await fetch(path, {
    method: 'POST',
    body: JSON.stringify(req),
  })

  if (!resp.ok) {
    throw new Error(`Response status: ${resp.status}`)
  }

  return await resp.json()
}
