<script setup lang="ts">
import { ref } from 'vue'
import { sendRequest } from '@/utils/http.ts'
import { useRouter } from 'vue-router'
import { postChannels } from '@/stores/posts.ts'
import { useAccountStore } from '@/stores/account.ts'

const title = ref('')
const content = ref('')
const channel = ref('')

const router = useRouter()
const accountStore = useAccountStore()

async function publish() {
  try {
    if (title.value.length < 5) {
      throw new Error('Minimum title length is 5!')
    }

    if (content.value.length < 10) {
      throw new Error('Minimum content length is 10!')
    }

    if (!channel.value) {
      throw new Error('Please select a category!')
    }

    const resp = await sendRequest('/api/post/publish', void 0, {
      title: title.value,
      content: content.value,
      channel: channel.value,
    })
    if (resp.code !== 1) {
      throw new Error(resp?.message ?? 'Failed to publish!')
    }

    ElMessage.success({
      plain: true,
      message: 'Publish successfully!',
      showClose: true,
      duration: 2000,
    })
    await router.push({
      name: 'explore',
    })
  } catch (err) {
    console.warn(err)
    ElMessage.warning({
      plain: true,
      message: (err as Error)?.message,
      showClose: true,
      duration: 2000,
    })
  }
}
</script>

<template>
  <div class="publish-view-container">
    <div class="line">
      <el-input
        size="large"
        v-model="title"
        placeholder="Please input title"
        clearable
        minlength="5"
        maxlength="60"
        show-word-limit
      />
      <el-button :disabled="!accountStore.hasLogin" size="large" type="primary" @click="publish">Publish</el-button>
    </div>
    <el-input
      class="content-input"
      v-model="content"
      minlength="10"
      maxlength="1000"
      placeholder="Please input content"
      show-word-limit
      type="textarea"
      :autosize="{ minRows: 10, maxRows: 20 }"
    />
    <div>
      <el-text size="large">Choose the category of the recipe</el-text>
      <el-radio-group v-model="channel" class="channel-selector">
        <el-radio v-for="channel in postChannels" :key="channel" :value="channel" size="large">
          {{ channel.replace('_', ' ') }}
        </el-radio>
      </el-radio-group>
    </div>
  </div>
</template>

<style scoped>
.publish-view-container {
  width: 100%;
  display: flex;
  justify-content: space-between;
  flex-direction: column;
  gap: 20px;
}

.publish-view-container .line {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 30px;
}

.content-input {
  width: calc(100% - 114px);
}

.channel-selector {
  width: calc(100% - 114px);
}
</style>
