<script setup lang="ts">
import { onMounted } from 'vue'
import { Comment, Flag, StarFilled } from '@element-plus/icons-vue'
import { formatDatetime } from '@/utils/format.ts'
import {
  type INotification,
  notificationTypes,
  useNotificationStore,
} from '@/stores/notifications.ts'

const notificationStore = useNotificationStore()

onMounted(async () => {
  await notificationStore.queryNotifications()
})

function getNotificationDatetime(item: INotification) {
  return `at ${formatDatetime(item.create_datetime)}`
}
</script>

<template>
  <div class="notification-view-container">
    <el-radio-group class="notification-tabs" v-model="notificationStore.currentType">
      <el-radio-button v-for="type in notificationTypes" :key="type.value" :value="type.value">
        <el-badge
          :show-zero="false"
          :offset="[10, -12]"
          :value="notificationStore.notifications[type.value]?.length || 0"
        >
          <div class="tab-item">
            <el-icon size="large">
              <Comment v-if="type.value === 'comments'" />
              <StarFilled v-else-if="type.value === 'likes'" />
              <Flag v-else-if="type.value === 'followers'" />
            </el-icon>
            <el-text>{{ type.label }}</el-text>
          </div>
        </el-badge>
      </el-radio-button>
    </el-radio-group>
    <div
      class="notification-list"
      v-if="
        Array.isArray(notificationStore.notifications[notificationStore.currentType]) &&
        notificationStore.notifications[notificationStore.currentType].length > 0
      "
    >
      <el-alert
        v-for="item in notificationStore.notifications[notificationStore.currentType]"
        :key="item.id"
        :title="notificationStore.getNotificationText(item)"
        type="info"
        @close="notificationStore.readNotification(item)"
      >
        <template #default>
          <div class="notification-item-datetime">{{ getNotificationDatetime(item) }}</div>
        </template>
      </el-alert>
    </div>
    <el-empty v-else description="No Data" />
  </div>
</template>

<style scoped>

.notification-view-container {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.notification-list {
  margin-top: 28px;
  max-height: calc(100vh - 77px);
  width: 70%;
  min-width: 330px;
  overflow-y: auto;
  display: flex;
  gap: 20px;
  flex-direction: column;
}

.notification-list::-webkit-scrollbar {
  display: none;
}

.tab-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 8px;
}

.is-active .tab-item .el-text {
  color: #f2f6fc;
}

.notification-item-datetime {
  text-align: right;
}
</style>

<style>
.notification-list .el-alert__content {
  width: calc(100% - 28px);
}
</style>
