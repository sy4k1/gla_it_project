import { defineStore } from 'pinia'
import { ref } from 'vue'
import { sendRequest } from '@/utils/http.ts'

export interface IPost {
  id: number
  title: string
  content: string
  // images: Array<string>
  poster_email: string
  poster_id: number
  poster_name: string
  likes: number
  // views: number
  channel: string
  create_datetime: string
}

export interface IComment {
  id: number
  // parent_comment_id: number
  post: number
  post_title: string
  poster_email: string
  commentator_email: string
  commentator_id: number
  commentator_name: string
  comment: string
  read: boolean
  create_datetime: string
}

export const usePostsStore = defineStore('posts', () => {
  const posts = ref<Array<IPost>>([])

  async function queryPosts(type: string, email?: string) {
    try {
      const resp = await sendRequest<{ type: string; email?: string }, Array<IPost>>(
        '/api/post/query',
        {
          noAccessToken: true,
        },
        {
          type: type,
          email: email,
        },
      )
      if (resp.code !== 1) {
        throw new Error(resp?.message ?? 'Failed to query posts!')
      }

      posts.value = resp?.data || []
    } catch (err) {
      console.warn(err)
    }
  }

  function updatePostLikes(id: number, newValue: number) {
    posts.value.forEach((post) => {
      if (post.id === id) {
        post.likes = newValue
      }
    })
  }

  const comments = ref<Array<IComment>>([])

  async function queryComments(post: IPost) {
    try {
      const resp = await sendRequest<
        {
          id: number
        },
        Array<IComment>
      >(
        '/api/post/query_comments',
        {
          noAccessToken: true,
        },
        {
          id: post.id,
        },
      )

      if (resp.code === 1) {
        comments.value = resp.data || []
      }
    } catch (err) {
      console.warn(err)
    }
  }

  const liked = ref(false)

  async function queryLiked(post: IPost) {
    try {
      const resp = await sendRequest<
        {
          id: number
        },
        boolean
      >('/api/post/query_like_status', void 0, {
        id: post.id,
      })

      if (resp.code === 1) {
        // update follow status
        liked.value = resp.data as boolean
      }
    } catch (err) {
      console.warn(err)
    }
  }

  async function likePost(post: IPost) {
    try {
      const resp = await sendRequest<
        {
          id: number
        },
        boolean
      >('/api/post/like', void 0, {
        id: post.id,
      })

      if (resp.code === 1) {
        // update follow status
        liked.value = resp.data as boolean
        updatePostLikes(post.id, post.likes + (liked.value ? 1 : -1))
      }
    } catch (err) {
      console.warn(err)
    }
  }

  const followStatus = ref(true)

  async function queryFollowStatus(post: IPost) {
    try {
      const resp = await sendRequest<
        {
          email: string
        },
        boolean
      >('/api/account/query_follow_status', void 0, {
        email: post.poster_email,
      })

      if (resp.code === 1) {
        // update follow status
        followStatus.value = resp.data as boolean
      }
    } catch (err) {
      console.warn(err)
    }
  }

  async function follow(post: IPost) {
    try {
      const resp = await sendRequest<
        {
          email: string
        },
        boolean
      >('/api/account/follow', void 0, {
        email: post.poster_email,
      })

      if (resp.code === 1) {
        // update follow status
        followStatus.value = resp.data as boolean
      }
    } catch (err) {
      console.warn(err)
    }
  }

  async function deletePost(post: IPost) {
    try {
      const resp = await sendRequest<
        {
          id: number
        },
        boolean
      >('/api/post/delete', void 0, {
        id: post.id,
      })

      if (resp.code !== 1) {
        return resp?.message || 'Failed to delete!'
      }

      // delete post
      posts.value = posts.value.filter((p) => {
        return p.id !== post.id
      })
      return void 0
    } catch (err) {
      console.warn(err)
      return 'Failed to delete!'
    }
  }

  return {
    posts,
    queryPosts,
    comments,
    queryComments,
    liked,
    queryLiked,
    likePost,
    followStatus,
    queryFollowStatus,
    follow,
    deletePost,
  }
})

export const postChannels = [
  'Vegetarian_Cuisine',
  'Chinese_Cuisine',
  'Western_Cuisine',
  'Japanese_Cuisine',
  'Desserts',
  'Soups',
]
