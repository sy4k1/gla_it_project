<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { type IAccountData, useAccountStore } from '@/stores/account.ts'
import PostList from '@/components/PostList.vue'
import { usePostsStore } from '@/stores/posts.ts'
import type { TabsPaneContext } from 'element-plus'
import { sendRequest } from '@/utils/http.ts'
import { getAvatarByID, getWallpaperByID } from '@/utils/image.ts'

const route = useRoute()
const router = useRouter()

const id = ref(Number(route.query.id))

function goToExplore() {
  router.push({
    name: 'explore',
  })
}

const accountStore = useAccountStore()
const account = ref<IAccountData | undefined>(void 0)

const activeTab = ref('publish')

async function handleSwitchTab(tab: TabsPaneContext) {
  const currentTab = tab.paneName
  await queryPosts(currentTab as string)
}

async function queryAccount() {
  try {
    const resp = await sendRequest<{ id: number }, IAccountData>(
      '/api/account/query',
      {
        noAccessToken: true,
      },
      {
        id: id.value,
      },
    )
    if (resp.code !== 1) {
      throw new Error(resp?.message ?? 'Failed to query account!')
    }

    account.value = resp.data
  } catch (err) {
    console.warn(err)
    ElMessage.warning({
      plain: true,
      message: (err as Error)?.message,
      showClose: true,
      duration: 2000,
    })
    id.value = 0
  }
}

onMounted(async () => {
  if (id.value === accountStore.data?.id) {
    account.value = accountStore.data
  } else {
    await queryAccount()
  }
  await queryPosts(activeTab.value)
})

const postsStore = usePostsStore()

async function queryPosts(currentTab: string) {
  await postsStore.queryPosts(currentTab, account.value?.email)
}
</script>

<template>
  <el-empty v-if="!id" description="Invalid URL">
    <el-button @click="goToExplore" type="primary" text size="large"
      >Go to explore recipes
    </el-button>
  </el-empty>
  <div v-else class="profile-view-container">
    <el-image
      fit="cover"
      class="wallpaper"
      :src="getWallpaperByID(account?.id)"
      alt="account's wallpaper"
    >
      <template #placeholder>
        <div class="image-slot">Loading<span class="dot">...</span></div>
      </template>
    </el-image>
    <div class="account-info-container">
      <div class="avatar-container">
        <el-avatar shape="square" :size="140" :src="getAvatarByID(account?.id)" />
      </div>
      <el-descriptions :column="2" class="account-info-list" :title="account?.name">
        <el-descriptions-item label="Email Address" :span="2">
          {{ account?.email }}
        </el-descriptions-item>
        <el-descriptions-item label="Followers">
          {{ account?.followers || 0 }}
        </el-descriptions-item>
        <!--        <el-descriptions-item label="Following">-->
        <!--          {{ account?.following || 0 }}-->
        <!--        </el-descriptions-item>-->
        <el-descriptions-item label="Likes">
          {{ account?.likes || 0 }}
        </el-descriptions-item>
      </el-descriptions>
    </div>
    <el-tabs class="post-tabs" v-model="activeTab" @tab-click="handleSwitchTab">
      <el-tab-pane label="Publish" name="publish">
        <PostList v-if="activeTab === 'publish'" />
      </el-tab-pane>
      <el-tab-pane label="Like" name="like">
        <PostList v-if="activeTab === 'like'" />
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<style scoped>
.profile-view-container {
  max-height: calc(100vh - 42px);
  overflow-y: auto;
}

.profile-view-container::-webkit-scrollbar {
  display: none;
}

.account-info-container {
  position: relative;
  margin: 0 20px 24px;
  display: flex;
  justify-content: flex-start;
  gap: 20px;
  align-items: center;
}

.avatar-container {
  position: relative;
  top: -40px;
  background: #fff;
  padding: 4px;
  width: fit-content;
  border-radius: 6px;
}

.wallpaper {
  width: 100%;
  height: 240px;
}

.account-info-list {
  width: 100%;
  position: relative;
  top: -16px;
}

.post-tabs {
  margin-top: -50px;
}
</style>
