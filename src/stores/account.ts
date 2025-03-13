import { defineStore } from 'pinia'
import { sendRequest } from '@/utils/http.ts'
import { ref } from 'vue'
import { deleteAccessToken, saveAccessToken, validateAccessToken } from '@/utils/local_storage.ts'

export interface IAccountData {
  id?: number
  email?: string
  name?: string
  role?: string
  bio?: string
  avatar?: string
  wallpaper?: string
  create_datetime?: string
  access_token?: string
  // following?: number
  followers?: number
  likes?: number
}

export interface ISignupReq {
  name: string
  email: string
  password: string
  passcode: string
}

export interface ILoginReq {
  email: string
  password: string
}

export const useAccountStore = defineStore('account', () => {
  const hasLogin = ref(false)
  const data = ref<IAccountData | undefined>(void 0)

  /**
   * query current account info
   */
  async function query() {
    try {
      if (!validateAccessToken()) {
        return
      }

      const resp = await sendRequest<undefined, IAccountData>('/api/account/query')
      if (resp.code !== 1) {
        throw new Error(resp?.message ?? 'Failed to query account!')
      }
      hasLogin.value = true
      data.value = resp.data
    } catch (err) {
      console.warn(err)
      hasLogin.value = false
      data.value = void 0
      deleteAccessToken()
    }
  }

  async function logout() {
    try {
      if (!validateAccessToken()) {
        return
      }

      const resp = await sendRequest<undefined, IAccountData>('/api/account/logout')
      if (resp.code !== 1) {
        throw new Error(resp?.message ?? 'Failed to log out!')
      }
      hasLogin.value = false
      data.value = void 0
      deleteAccessToken()
      return null
    } catch (err) {
      console.warn(err)
      return err as Error
    }
  }

  async function signup(req: ISignupReq) {
    try {
      const resp = await sendRequest<ISignupReq, IAccountData>(
        '/api/account/signup',
        {
          noAccessToken: true,
        },
        req,
      )
      if (resp.code !== 1) {
        throw new Error(resp?.message ?? 'Failed to sign up!')
      }
      hasLogin.value = true
      data.value = resp.data
      saveAccessToken(resp.data?.access_token ?? '')
      return null
    } catch (err) {
      console.warn(err)
      return err as Error
    }
  }

  async function login(req: ILoginReq) {
    try {
      const resp = await sendRequest<ILoginReq, IAccountData>(
        '/api/account/login',
        {
          noAccessToken: true,
        },
        req,
      )
      if (resp.code !== 1) {
        throw new Error(resp?.message ?? 'Failed to log in!')
      }
      hasLogin.value = true
      data.value = resp.data
      saveAccessToken(resp.data?.access_token ?? '')
      return null
    } catch (err) {
      console.warn(err)
      return err as Error
    }
  }

  return { hasLogin, data, query, logout, signup, login }
})
