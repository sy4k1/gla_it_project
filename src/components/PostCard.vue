<script setup lang="ts">
import { ref } from 'vue'
import { type IComment, type IPost, usePostsStore } from '@/stores/posts.ts'
import { Star } from '@element-plus/icons-vue'
import { sendRequest } from '@/utils/http.ts'
import { getAvatarByID, getPostImage } from '@/utils/image.ts'
import { useAccountStore } from '@/stores/account.ts'
import { formatDatetime } from '@/utils/format.ts'
import { useRouter } from 'vue-router'

const props = defineProps<{ post: IPost }>()
const postsStore = usePostsStore()
const accountStore = useAccountStore()

const postDialogVisible = ref(false)

async function showPostDialog() {
  await postsStore.queryComments(props.post)
  await postsStore.queryFollowStatus(props.post)
  await postsStore.queryLiked(props.post)
  postDialogVisible.value = true
}

const newComment = ref('')

async function sendComment() {
  try {
    const resp = await sendRequest<
      {
        id: number
        comment: string
      },
      Array<IComment>
    >('/api/post/comment', void 0, {
      id: props.post.id,
      comment: newComment.value,
    })
    if (resp.code !== 1) {
      throw new Error(resp.message)
    }

    postsStore.comments.push(...(resp?.data || []))
    newComment.value = ''
  } catch (err) {
    console.warn(err)
  }
}

const router = useRouter()

function openProfile() {
  router.push({
    name: 'profile',
    query: {
      id: props.post.poster_id,
    },
  })
}
</script>

<template>
  <el-card class="post-card" shadow="hover" @click="showPostDialog">
    <div class="post-card-body-container">
      <el-image
        class="post-image"
        :src="getPostImage(props.post.channel, props.post.id)"
        fit="cover"
      />
      <el-text class="post-title" truncated :line-clamp="2">
        {{ props.post.title }}
      </el-text>
      <div class="post-card-footer">
        <div class="post-card-footer-left">
          <el-avatar shape="circle" :size="20" :src="getAvatarByID(props.post.poster_id)" />
          <el-text>{{ props.post.poster_name }}</el-text>
        </div>
        <el-text>
          <el-icon>
            <Star />
          </el-icon>
          {{ props.post.likes }}
        </el-text>
      </div>
    </div>
  </el-card>
  <el-dialog
    class="post-dialog"
    v-model="postDialogVisible"
    width="70%"
    :show-close="false"
    align-center
  >
    <div class="post-dialog-body">
      <div class="post-dialog-left">
        <el-image
          class="post-dialog-image"
          :src="getPostImage(props.post.channel, props.post.id)"
          fit="cover"
        />
        <div class="post-dialog-header">
          <div class="account-container" @click="openProfile">
            <el-avatar shape="circle" :size="42" :src="getAvatarByID(props.post.poster_id)" />
            <el-text class="poser-dialog-name">{{ props.post.poster_name }}</el-text>
          </div>
          <el-button
            type="primary"
            v-if="
              !postsStore.followStatus &&
              accountStore.hasLogin &&
              props.post.poster_email !== accountStore.data?.email
            "
            @click="postsStore.follow(props.post)"
          >
            Follow
          </el-button>
        </div>
      </div>
      <div class="post-dialog-right">
        <el-text class="post-dialog-content">{{ props.post.content }}</el-text>
        <el-text size="small" type="info" class="post-dialog-datetime">
          Published at {{ formatDatetime(props.post.create_datetime) }}
        </el-text>
        <el-divider />
        <div class="comment-list" v-if="postsStore.comments.length > 0">
          <div class="comment-item" v-for="comment in postsStore.comments" :key="comment.id">
            <el-avatar shape="circle" :size="24" :src="getAvatarByID(comment.commentator_id)" />
            <div class="comment-data">
              <el-text type="info">
                {{ comment.commentator_name }}
              </el-text>
              <el-text>
                {{ comment.comment }}
              </el-text>
              <el-text size="small" type="info">
                {{ formatDatetime(comment.create_datetime) }}
              </el-text>
            </div>
          </div>
        </div>
        <el-empty v-else description="No Comment" />
        <el-divider />
        <div class="comment-container">
          <el-button
            @click="postsStore.likePost(props.post)"
            :icon="Star"
            :disabled="!accountStore.hasLogin"
            text
            :type="postsStore.liked ? 'danger' : 'info'"
          >
            {{ props.post.likes }}
          </el-button>
          <div class="comment-input">
            <el-input v-model="newComment" placeholder="Comment" maxlength="100" show-word-limit>
              <template #append>
                <el-button
                  @click="sendComment"
                  :disabled="newComment.length < 1 || !accountStore.hasLogin"
                >
                  Send
                </el-button>
              </template>
            </el-input>
          </div>
        </div>
      </div>
    </div>
  </el-dialog>
</template>
<style scoped>
.post-card {
  width: 220px;
  cursor: pointer;
  margin-bottom: 16px;
}

.post-card-body-container {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-direction: column;
  gap: 12px;
}

.post-title {
  width: 100%;
}

.post-image {
  width: 100%;
  height: 100%;
  border-radius: 4px;
}

.post-card-footer {
  width: 100%;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.post-card-footer-left {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 8px;
}

.post-dialog-body {
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: space-between;
  gap: 20px;
  align-items: stretch;
  min-height: 70vh;
  max-height: 85vh;
}

.post-dialog-left {
  flex: 1;
  width: calc(50% - 10px);
  display: flex;
  justify-content: space-between;
  align-items: stretch;
  flex-direction: column;
  gap: 24px;
}

.post-dialog-image {
  flex: 1;
  width: 100%;
  height: 100%;
  border-radius: 8px;
}

.post-dialog-right {
  width: calc(50% - 10px);
  flex: 1;
  display: flex;
  justify-content: space-between;
  align-items: stretch;
  flex-direction: column;
}

.post-dialog-header {
  width: 100%;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.account-container {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 12px;
  cursor: pointer;
}

.poser-dialog-name {
  font-size: 18px;
}

.post-dialog-content {
  white-space: pre-line;
}

.post-dialog-content,
.post-dialog-datetime {
  width: 100%;
}

.post-dialog-datetime {
  margin-top: 12px;
}

.comment-list {
  flex: 1;
  overflow-y: auto;
}

.comment-list::-webkit-scrollbar {
  display: none;
}

.comment-container {
  width: 100%;
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 8px;
}

.comment-item {
  display: flex;
  justify-content: flex-start;
  align-items: flex-start;
  gap: 8px;
  margin-bottom: 14px;
}

.comment-data {
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  align-items: flex-start;
  gap: 4px;
}

.comment-data span {
  width: 100%;
}
</style>
