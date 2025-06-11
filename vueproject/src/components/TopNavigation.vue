<template>
    <div class="header-container">
      <div class="logo">
        <img src="@/assets/lc.png" alt="Logo" height="40" />
        <span>PDF在线精确压缩</span>
      </div>
      
      <el-menu
        
        class="nav-menu"
        mode="horizontal"
       
        :router="true"
      >
        <el-menu-item index="/">首页</el-menu-item>
        <el-sub-menu >
          <template #title>压缩</template>
          <el-menu-item index="/image">根据大小压缩</el-menu-item>
          <el-menu-item index="/quality">根据质量压缩</el-menu-item>
        </el-sub-menu>
        <el-menu-item index="/about">关于</el-menu-item>
        <el-menu-item index="/support">支持</el-menu-item>
      </el-menu>
      
      <!-- <div class="user-info">
        <el-dropdown>
          <span class="el-dropdown-link">
            <el-avatar :size="32" src="https://cube.elemecdn.com/3/7c/3ea6beec64369c2642b92c6726f1epng.png" />
            <span style="margin-left: 8px;">用户名</span>
          </span>
          <template #dropdown>
            <el-dropdown-menu>
              <el-dropdown-item>个人中心</el-dropdown-item>
              <el-dropdown-item>设置</el-dropdown-item>
              <el-dropdown-item divided>退出登录</el-dropdown-item>
            </el-dropdown-menu>
          </template>
        </el-dropdown>
      </div> -->
    </div>
  </template>
  
<script>
  import { ref } from 'vue';
  
  const activeIndex = ref('1');
  const handleSelect = (key, keyPath) => {
    console.log(key, keyPath);
  };
  export default {
  name: 'TopNavigation',
  }
</script>
  
<style scoped>
  .header-container {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0 20px;
    border-bottom: 1px solid #eee;
  }
  
  .logo {
    display: flex;
    align-items: center;
    font-size: 18px;
    font-weight: bold;
  }
  
  .logo img {
    margin-right: 10px;
  }
  
  .nav-menu {
    flex: 1;
    margin: 0 20px;
    border-bottom: none;
  }
  
  .user-info {
    display: flex;
    align-items: center;
  }
  
  .el-dropdown-link {
    display: flex;
    align-items: center;
    cursor: pointer;
  }
</style>