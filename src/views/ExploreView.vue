<script setup lang="ts">
import PostList from '@/components/PostList.vue'
import { onMounted, ref } from 'vue'
import type { TabsPaneContext } from 'element-plus'
import { postChannels, usePostsStore } from '@/stores/posts.ts'
import { Apple, Bowl, Food, IceCream, KnifeFork } from '@element-plus/icons-vue'

const activeTab = ref('All')

const postsStore = usePostsStore()

async function queryPosts(currentTab: string) {
  await postsStore.queryPosts(currentTab)
}

async function handleSwitchTab(tab: TabsPaneContext) {
  const currentTab = tab.paneName
  await queryPosts(currentTab as string)
}

onMounted(async () => {
  await queryPosts(activeTab.value)
})
</script>

<template>
  <div class="explore-view-container">
    <el-tabs class="explore-post-tabs" v-model="activeTab" @tab-click="handleSwitchTab">
      <el-tab-pane label="All" name="All">
        <PostList v-if="activeTab === 'All'" />
      </el-tab-pane>
      <el-tab-pane v-for="channel in postChannels" :key="channel" :name="channel">
        <template #label>
          <el-icon>
            <Apple v-if="channel === 'Vegetarian_Cuisine'" />
            <Food v-else-if="channel === 'Chinese_Cuisine'" />
            <KnifeFork v-else-if="channel === 'Western_Cuisine'" />
            <Bowl v-else-if="channel === 'Japanese_Cuisine'" />
            <IceCream v-else-if="channel === 'Desserts'" />
          </el-icon>
          <span>&nbsp;{{ channel.replace('_', ' ') }}</span>
        </template>
        <PostList v-if="activeTab === channel" />
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<style scoped>
.explore-view-container {
  max-height: calc(100vh - 42px);
  overflow-y: auto;
}

.explore-view-container::-webkit-scrollbar {
  display: none;
}
</style>
<style>
.explore-post-tabs .el-tabs__header {
  position: sticky;
  top: 0;
  left: 0;
  background: #fff;
}
</style>
