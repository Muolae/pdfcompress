<template>
  <div class="mainw">
  <el-card class="card">
    <template #header>
      <div class="card-header">
        <h3>PDF定向压缩可以做什么?</h3>
      </div>
    </template>
    <p>将PDF文件压缩到您指定的大小,<br/>且不损失除图片外的其他内容的质量.
      并且,由于我们采用了渐进式压缩方案,<br/>文件的质量损失将达到最小.
      <br/>另外,您还可以根据图片的质量损失评估(<a href="https://zhuanlan.zhihu.com/p/1891387001640563898">PSNR</a>)或者每一个图片的优先级来压缩您的文件.</p>

  </el-card>

  <el-card class="card">
    <template #header>
      <div class="card-header">
        <h3>PDF定向压缩如何工作</h3>
      </div>
    </template>
    <p>我们通过压缩PDF文件中的图片实现减小PDF文件的体积.通过图片JPEG编码压缩优化和降低分辨率来减少图片大小.
      <br/><br/>并且,我们在压缩过程中引入了先进的JPEG编码器MozJPEG来提高图片质量.<br/>使用图片质量损失评估参数<a href="https://zhuanlan.zhihu.com/p/1891387001640563898">PSNR</a>和<a href="https://zhuanlan.zhihu.com/p/399215180">SSIM</a>
      帮助您精确的了解文件在压缩过程中的质量损失</p>

  </el-card>

  <el-card class="card">
    <template #header>
      <div class="card-header">
        <h3>我们的优势</h3>
      </div>
    </template>
    <ul class="ulsty">
      <li>不超过目标大小的最佳图片质量</li>
      <li>控制图片的质量损失程度</li>
      <li>精确控制每一张图片的质量</li>
      <li>完美免费,无需登录,无限制使用</li>
      <li >安全性保证</li>
    </ul>
  </el-card>
</div>

<div class="foot">
  <h3>Powered by LiuChao. 2025</h3>
  <p style="text-align: center;">supported</p>
<div class="flb">
  <link-button @beclick="toOutLink('https://cn.vuejs.org/')"  :src="require('@/assets/logo.png')" info="VUE"></link-button>
  <link-button @beclick="toOutLink('https://element-plus.org/')" :src="require('@/assets/element-plus.png')" info="element plus"></link-button>
  <link-button @beclick="toOutLink('https://www.mupdf.com/')" :src="require('@/assets/ODLS.png')" info="PYMUPDF"></link-button>
  <link-button @beclick="toOutLink('https://github.com/mozilla/mozjpeg')" :src="require('@/assets/github.png')" info="MozJPEG"></link-button>
</div>
</div>
</template>


<script setup>
import LinkButton from '@/components/LinkButton.vue';
const toOutLink=(url)=>{
    window.location.href=url
}
</script>

<style scoped>
.mainw{
  display: flex;
  justify-content: center;
  height: 500px;
}
.card{
  max-width: 320px;
  margin-left: 20px;
  margin-top: 20px;
  height: 400px;
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
p{
  text-align: left;
}
ul{
  text-align: left;
}
</style>