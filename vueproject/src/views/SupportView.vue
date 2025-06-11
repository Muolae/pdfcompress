<template>

  <div class="mainbox">
    <div class="coverbox">
      <h1 style="margin-top: 160px;">获取更多支持</h1>
      <el-text>需要获取更多支持?请联系作者</el-text>
        <link-button class="slb" :src="require('@/assets/QQ.png')" info="3229701951" @click="changex"></link-button>
      <link-button class="slb" :src="require('@/assets/电话.png')" info="15675957097"></link-button>
    </div>
    <img src="@\assets\intro-bg.jpg" class="bkimg">
  </div>

  <div class="foot">
    <h3>Powered by LiuChao. 2025</h3>
    <p>supported</p>
  <div class="flb">
    <link-button @beclick="toOutLink('https://cn.vuejs.org/')"  :src="require('@/assets/logo.png')" info="VUE"></link-button>
    <link-button @beclick="toOutLink('https://element-plus.org/')" :src="require('@/assets/element-plus.png')" info="element plus"></link-button>
    <link-button @beclick="toOutLink('https://www.mupdf.com/')" :src="require('@/assets/ODLS.png')" info="PYMUPDF"></link-button>
    <link-button @beclick="toOutLink('https://github.com/mozilla/mozjpeg')" :src="require('@/assets/github.png')" info="MozJPEG"></link-button>
  </div>
  </div>

  <el-dialog
    v-model="dialogVisible"
    title="选择压缩模式"
    width="700"
    :before-close="handleClose"
    
  >
  <span>我们提供了几种不同的压缩功能来满足您的不同压缩需求,请选择一个适合您的压缩模式</span>
  <div class="mainw">

    
    <el-card class="card">
    <template #header>
      <div class="card-header">
        <h4>指定大小压缩</h4>
      </div>
    </template>
    <span>将PDF文件压缩到您指定的大小,且不超过您指定的质量</span>
    <template #footer>
      <div class="card-header">
        <el-button type="primary" @click="dialogVisible = false">
          选择
        </el-button>
      </div>
    </template>
  </el-card>

  <el-card class="card">
    <template #header>
      <div class="card-header">
        <h4>指定质量压缩</h4>
      </div>
    </template>
    <span>设置图片的最低质量,确保每一张图片的质量不会低于您设定的值</span>
    <template #footer>
      <div class="card-header">
        <el-button type="primary" @click="dialogVisible = false">
          选择
        </el-button>
      </div>
    </template>
  </el-card>

  <el-card class="card">
    <template #header>
      <div class="card-header">
        <h4>指定图像优先级压缩</h4>
      </div>
    </template>
    <span style="">通过调整图像优先级,让您文件中的重要图片拥有更好的质量</span>
    <template #footer>
      <div class="card-header">
        <el-button type="primary">
          选择
        </el-button>
      </div>
    </template>
  </el-card>
  </div>
    <template #footer>
      <div class="dialog-footer">
        <el-button type="primary" @click="dialogVisible = false">
          关闭
        </el-button>
      </div>
    </template>
  
  </el-dialog>
</template>

<script setup>
import { ref,onMounted } from 'vue';
import LinkButton from '@/components/LinkButton.vue';
import axios from 'axios';
import { useStore } from 'vuex';
import { ElMessageBox } from 'element-plus'

const dialogVisible = ref(false)

const info=ref('')
const sendtest=()=>{
  axios.get("http://127.0.0.1:5000/reqtest").then(response => {
        // 处理成功的响应
        console.log(response.data);
  })
  .catch(error => {
    // 处理错误
    console.error(error);
  });

}
const store = useStore();
// count不会变化
const count = store.state.count;
const changex=()=>{
    ElMessageBox.alert('您的文件已经无法继续压缩,因此最终压缩的文件大于您的预设值', '压缩已达到极限!', {
    confirmButtonText: 'OK',
  })
}
const toOutLink=(url)=>{
    window.location.href=url
}
</script>


<style scoped>
  .mainw{
  display: flex;
  justify-content: center;
  height: 330px;
  }
  .card{
  width: 180px;
  margin-left: 20px;
  margin-top: 20px;
  height: 300px;
  }
  .mainbox{
    width: 100%;
    height: 500px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
  }
  .bkimg{
    width: 100%;
    height: 500px;
    position: absolute;
    z-index: 0;
  }
  .coverbox{
    background: rgba(255, 255, 255, 0.1);
    z-index: 1;
    width: 100%;
    height: 500px;
    display: flex;
    flex-direction: column;
    align-items: center;
  }
  .mybtnx{
    margin-top: 20px;
    border: 1px solid rgb(18, 106, 179);
    border-radius: 5px;
    width: 100px;
    height: 30px;
    display: flex;
    align-items: center;
    justify-content: center;
    color: rgb(18, 106, 179);
  }
  .mybtnx:hover{
    
    background-color: rgb(18, 106, 179);
    color: #ffffff;
  }
  .slb{
    margin-top: 10px;
  }
  .foot{
    width: 100%;
    height: 150px;
    background-color: rgb(9, 15, 15);
    display: flex;
    flex-direction: column;
    color: #fff;
    padding: 0 0 0 20px;
  }
  .flb{
    display: flex;
    flex-direction: row;
    justify-content: center;
  }
</style>