# Vue 3 安裝步驟與 Axios API 串接筆記

## 1. 環境與套件安裝

1. 安裝官方 Node.js / npm 並設定環境變數。
2. 安裝相關套件：

```bash
# 安裝 Vue 3 本體
npm install vue@next

# 安裝 Vue CLI
npm install -g @vue/cli

# 安裝 HTTP 連線套件 Axios
npm install axios
```

## 2. 建立與啟動基礎專案

```bash
# 建立專案
vue create <專案名稱>

# 進入專案後主要編輯項目：
# - vue.config.js（專案與代理設定）
# - src/components/（各獨立元件）
# - src/App.vue（主畫面組合入口）

# 啟動開發伺服器
npm run serve
```

## 3. 連接後端 API 範例（`ApiInteraction.vue`）

```vue
<template>
  <div>
    <h1>Vue 3 + Axios 範例</h1>
    <p>點擊按鈕以取得資料</p>
    <button @click="getData">取得資料</button>
    <div v-if="loading">
      <p>正在載入中...</p>
    </div>
    <div v-else>
      <h2>資料結果</h2>
      <ul>
        <li v-for="item in data" :key="item.id">{{ item.name }}</li>
      </ul>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue';
import axios from 'axios';

export default {
  setup() {
    const data = ref([]); // 使用 ref 儲存從 API 取得之陣列資料
    const loading = ref(false); // 控制載入中狀態顯示

    const getData = async () => {
      loading.value = true;
      try {
        const response = await axios.get('https://api.example.com/data');
        data.value = response.data;
      } catch (error) {
        console.error(error);
      } finally {
        loading.value = false;
      }
    };

    return {
      data,
      loading,
      getData,
    };
  },
};
</script>
```
