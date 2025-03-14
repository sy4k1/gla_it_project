<script setup lang="ts">
import { ref, watch } from 'vue'
import { Bell, Compass, DocumentAdd, Food, Message, User } from '@element-plus/icons-vue'
import { type RouteLocationRaw, useRouter, useRoute } from 'vue-router'

import { useAccountStore } from '@/stores/account.ts'
import { validateEmailAddress } from '@/utils/validator.ts'
import { sendRequest } from '@/utils/http.ts'

const accountStore = useAccountStore()

const router = useRouter()
const route = useRoute()

const pagePaths: Array<string> = ['explore', 'publish', 'notification', 'profile']
const activateMenuIdx = ref(0)

watch(
  () => route.name,
  (newName) => {
    activateMenuIdx.value = pagePaths.indexOf(newName as string)
  },
)

function jumpTo(idx: number) {
  if (idx === activateMenuIdx.value) {
    return
  }

  if (!accountStore.hasLogin && (idx === 1 || idx === 2 || idx === 3)) {
    showLoginDialog()
    return
  }

  const path = pagePaths[idx]
  const to: RouteLocationRaw = {
    name: path,
  }
  if (path === 'profile') {
    to.query = {
      id: accountStore.data?.id ?? -1,
    }
  }
  router.push(to)
}

async function logout() {
  const err = await accountStore.logout()
  if (!err) {
    ElMessage.success({
      plain: true,
      message: 'Log out successfully!',
      showClose: true,
      duration: 2000,
    })
    jumpTo(0)
  } else {
    ElMessage.error({
      plain: true,
      message: err.message,
      showClose: true,
      duration: 2000,
    })
  }
}

const loginDialogVisible = ref(false)

const email = ref('')
const name = ref('')
const password = ref('')
const curDialogStatus = ref('login')
const passcode = ref('')
const sent = ref(false)
const sentSecond = ref(60)

async function showLoginDialog() {
  loginDialogVisible.value = true
  email.value = ''
  name.value = ''
  password.value = ''
  curDialogStatus.value = 'login'
  passcode.value = ''
  sent.value = false
  sentSecond.value = 60
}

async function sendPasscode() {
  if (!validateEmailAddress(email.value)) {
    ElMessage.warning({
      plain: true,
      message: 'Please input valid email address!',
      showClose: true,
      duration: 2000,
    })
    return
  }

  try {
    const resp = await sendRequest<{ email?: string }, string>(
      '/api/account/send_passcode',
      {
        noAccessToken: true,
      },
      {
        email: email.value,
      },
    )
    if (resp.code !== 1) {
      throw new Error(resp?.message ?? 'Failed to send passcode!')
    }

    ElMessage.success({
      plain: true,
      message: `Your passcode is ${resp?.data} !`,
      showClose: true,
      duration: 5000,
    })

    sent.value = true
    sentSecond.value = 60
    const sendPasscodeTimeoutHandle = () => {
      if (sentSecond.value > 0) {
        sentSecond.value--
        setTimeout(sendPasscodeTimeoutHandle, 1000)
      } else {
        sent.value = false
      }
    }
    setTimeout(sendPasscodeTimeoutHandle, 1000)
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

async function signup() {
  // validate username & passcode
  if (name.value.length < 1) {
    throw new Error('Please input valid username!')
  } else if (passcode.value.length !== 6) {
    throw new Error('Please input valid passcode!')
  }

  const err = await accountStore.signup({
    name: name.value,
    email: email.value,
    password: password.value,
    passcode: passcode.value,
  })

  if (!!err) {
    throw err
  }
}

async function login() {
  try {
    // validate email & password
    if (!validateEmailAddress(email.value)) {
      throw new Error('Please input valid email address!')
    } else if (password.value.length < 8) {
      throw new Error('Please input valid password!')
    }

    // sign up
    if (curDialogStatus.value === 'signup') {
      await signup()
    } else {
      // login in
      const err = await accountStore.login({
        email: email.value,
        password: password.value,
      })

      if (!!err) {
        throw err
      }
    }

    loginDialogVisible.value = false
    window.location.reload()
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
  <div class="navigation-container">
    <div class="navigation-container-main">
      <el-button size="large" type="primary" :icon="Food">Share Your Recipe</el-button>
      <div class="menu-container">
        <el-button @click="jumpTo(0)" :bg="activateMenuIdx === 0" size="large" text :icon="Compass">
          Explore
        </el-button>
        <el-button
          v-if="accountStore.hasLogin"
          @click="jumpTo(1)"
          :bg="activateMenuIdx === 1"
          size="large"
          text
          :icon="DocumentAdd"
        >
          Publish
        </el-button>
        <el-button
          v-if="accountStore.hasLogin"
          @click="jumpTo(2)"
          :bg="activateMenuIdx === 2"
          size="large"
          text
          :icon="Bell"
        >
          Notification
        </el-button>
        <el-button
          v-if="accountStore.hasLogin"
          @click="jumpTo(3)"
          :bg="activateMenuIdx === 3"
          size="large"
          text
          :icon="User"
        >
          Profile
        </el-button>
      </div>
    </div>
    <div class="navigation-container-footer">
      <el-button v-if="accountStore.hasLogin" type="info" plain @click="logout">Log out</el-button>
      <el-button v-else type="primary" plain @click="showLoginDialog">Log in / Sign up</el-button>
    </div>
  </div>
  <el-dialog
    v-model="loginDialogVisible"
    :title="`&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;${curDialogStatus === 'login' ? 'Log in' : 'Sign up'}`"
    width="400"
    body-class="login-dialog-body"
    show-close
    center
    align-center
  >
    <template v-if="curDialogStatus === 'login'">
      <el-input
        v-model="email"
        size="large"
        placeholder="Please input email address"
        :prefix-icon="Message"
      />
      <el-input
        v-model="password"
        size="large"
        type="password"
        placeholder="Please input password"
        show-password
        minlength="8"
        maxlength="20"
      />
      <div>
        <el-text size="small">Don't have an account?</el-text>
        <el-button type="primary" text @click="curDialogStatus = 'signup'" size="small">
          Sign up
        </el-button>
      </div>
    </template>
    <template v-else>
      <el-input
        v-model="name"
        size="large"
        placeholder="Please input username"
        minlength="8"
        maxlength="20"
        show-word-limit
      />
      <el-input
        v-model="email"
        size="large"
        placeholder="Please input email address"
        :prefix-icon="Message"
        maxlength="30"
      />
      <el-input
        v-model="password"
        size="large"
        type="password"
        placeholder="Please input password"
        show-password
        minlength="8"
        maxlength="20"
      />
      <el-input v-model="passcode" size="large" placeholder="Passcode" minlength="6" maxlength="6">
        <template #append>
          <el-button :disabled="sent" @click="sendPasscode">
            {{ sent ? `Wait ${sentSecond}s` : 'Send Passcode' }}
          </el-button>
        </template>
      </el-input>
      <div>
        <el-text size="small">Already have an account?</el-text>
        <el-button type="primary" text @click="curDialogStatus = 'login'" size="small">
          Log in
        </el-button>
      </div>
    </template>
    <template #footer>
      <el-button type="primary" @click="login">
        {{ curDialogStatus === 'login' ? 'Log in' : 'Sign up' }}
      </el-button>
    </template>
  </el-dialog>
</template>

<style scoped>
.navigation-container {
  padding: 20px 32px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-direction: column;
  min-height: 100vh;
}

.navigation-container-main {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-direction: column;
}

.menu-container {
  margin: 32px;
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  flex-direction: column;
  gap: 12px;
}

.menu-container button {
  margin-left: 0px;
}
</style>

<style>
.login-dialog-body {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-direction: column;
  gap: 16px;
  padding: 16px 40px 0;
}
</style>
