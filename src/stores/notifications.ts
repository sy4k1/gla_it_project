import { defineStore } from 'pinia'
import type { IComment } from '@/stores/posts.ts'
import { ref } from 'vue'
import { sendRequest } from '@/utils/http.ts'

export type INotification = IComment & {
  id: number
  liked_account_email: string
  liked_account_name: string
  post_id: number
  poster_email: string
  read: boolean
  create_datetime: string
} & {
  id: number
  follower_email: string
  follower_name: string
  follower_id: number
  followed_email: string
  read: boolean
  create_datetime: string
}

export type TNotifications = Record<string, Array<INotification>>

export const useNotificationStore = defineStore('notifications', () => {
  const notifications = ref<TNotifications>({})

  const currentType = ref('comments')

  async function queryNotifications() {
    try {
      const resp = await sendRequest<{ type: string; email?: string }, TNotifications>(
        '/api/account/query_notification',
      )
      if (resp.code !== 1) {
        throw new Error(resp?.message ?? 'Failed to query notifications!')
      }

      notifications.value = resp?.data || ({} as TNotifications)
    } catch (err) {
      console.warn(err)
    }
  }

  async function readNotification(item: INotification) {
    try {
      const resp = await sendRequest<{ id: number; type: string }, boolean>(
        '/api/account/read_notification',
        void 0,
        {
          id: item.id,
          type: currentType.value,
        },
      )
      if (resp.code !== 1) {
        throw new Error(resp?.message ?? 'Failed to read notification!')
      }

      notifications.value[currentType.value] = notifications.value[currentType.value].filter(
        (i) => {
          return i.id !== item.id
        },
      )
    } catch (err) {
      console.warn(err)
    }
  }

  function getNotificationText(item: INotification) {
    if (currentType.value === 'comments') {
      return `${item.commentator_name} commented on your post (${item.post_title})`
    } else if (currentType.value === 'likes') {
      return `${item.commentator_name} liked your post (${item.post_title})`
    }
    return `${item.commentator_name} followed you`
  }

  return { notifications, currentType, queryNotifications, readNotification, getNotificationText }
})

export const notificationTypes = [
  {
    value: 'comments',
    label: 'Comments',
  },
  {
    value: 'likes',
    label: 'Likes',
  },
  {
    value: 'followers',
    label: 'Folloers',
  },
]
