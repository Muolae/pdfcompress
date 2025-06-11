<template>
  <el-carousel height="500px"   :autoplay="true" :interval="2000" :arrow="always">
    <el-carousel-item >
      <div class="mainbox">
        <div class="coverbox">
          <h1 style="margin-top: 160px;">PDF QUANTIFY COMPRESS</h1>
          <span>将PDF文件压缩到您指定的大小,并且达到最小的质量损失.</span>
          <div class="mybtnx" @click="dialogVisible = true">立即体验</div>
        </div>
        <img src="@\assets\intro-bg.jpg" class="bkimg">
      </div>
    </el-carousel-item>

    <el-carousel-item>
      <div class="mainbox">
        <div class="coverbox" style="color: #ffffff;">
          <h1 style="margin-top: 160px;">控制图片质量损失</h1>
          <span>基于图片质量损失(PSNR)的PDF压缩,确保您的图片质量</span>
          <div class="mybtnx" @click="dialogVisible = true">立即体验</div>
        </div>
        <img src="@\assets\bk1.jpg" class="bkimg">
      </div>
    </el-carousel-item>

    <el-carousel-item>
      <div class="mainbox">
        <div class="coverbox">
          <h1 style="margin-top: 160px;">自定义每一张图片</h1>
          <el-text>自定义每一张图片的优先级,让您文件中的重要图片保留更大的质量</el-text>
          <div class="mybtnx" @click="dialogVisible = true">立即体验</div>
        </div>
        <img src="@\assets\bk2.png" class="bkimg">
      </div>
    </el-carousel-item>
  </el-carousel>

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
    width="600"
    :before-close="handleClose"
    
  >
  <div class="mainw">

    
    <el-card class="card">
    <template #header>
      <div class="card-header">
        <h4>根据大小压缩</h4>
      </div>
    </template>
    <span style="height:160px;">将PDF文件压缩到您指定的大小,并且支持控制每一张图像的质量</span>
    <template #footer>
      <div class="card-header">
        <el-button type="primary" @click="tosize('/image')">
          选择
        </el-button>
      </div>
    </template>
  </el-card>

  <el-card class="card">
    <template #header>
      <div class="card-header">
        <h4>根据质量压缩</h4>
      </div>
    </template>
    <span style="height:160px;">设置图片的最低质量,确保每一张图片的质量不会低于您设定的值</span>
    <template #footer>
      <div class="card-header">
        <el-button type="primary" @click="tosize('/quality')">
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
  import { useRouter } from 'vue-router';
  import { ref,onMounted } from 'vue';
  import LinkButton from '@/components/LinkButton.vue';
  const dialogVisible = ref(false)
  const router =useRouter()
  const tosize=(target)=>{
    router.push(target)
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
  width: 280px;
  margin-left: 20px;
  margin-top: 20px;
  height: 300px;
  }
.el-carousel__item h3 {
  color: #475669;
  opacity: 0.75;
  line-height: 200px;
  margin: 0;
  text-align: center;
}

.el-carousel__item:nth-child(2n) {
  background-color: #99a9bf;
}

.el-carousel__item:nth-child(2n + 1) {
  background-color: #d3dce6;
}
.homepage{
  height: 400px;
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
  border: 1px solid rgb(15, 210, 54);
  border-radius: 5px;
  width: 100px;
  height: 30px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: rgb(15, 210, 54);
}
.mybtnx:hover{
  background-color: rgb(15, 210, 54);
  color: #ffffff;
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
