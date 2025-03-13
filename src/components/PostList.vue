<script setup lang="ts">
import { nextTick, onUpdated } from 'vue'
import { usePostsStore } from '@/stores/posts.ts'
import PostCard from '@/components/PostCard.vue'
import Masonry from 'masonry-layout'
import imagesLoaded from 'imagesloaded'

const postsStore = usePostsStore()

let msnry: Masonry | undefined = void 0

onUpdated(() => {
  nextTick(() => {
    if (!msnry) {
      msnry = new Masonry('.post-list-container', {
        itemSelector: '.post-list-container .post-card',
        columnWidth: 220,
        gutter: 16,
        horizontalOrder: true,
      })
    }

    imagesLoaded('.post-list-container', () => {
      msnry?.layout?.()
    })
  })
})
</script>

<template>
  <div class="post-list-container" v-if="postsStore.posts.length > 0">
    <PostCard v-for="post in postsStore.posts" :key="post.id" :post="post" />
  </div>
  <el-empty v-else description="No Data" />
</template>

<style scoped></style>
