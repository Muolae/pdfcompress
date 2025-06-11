<template>
  <h1>将PDF文件压缩到不超过您指定大小的最佳质量</h1>
  <el-text>同时支持自定义每一张图片的优先级,让您文件中的重要图片保留更大的质量</el-text>
  <el-upload
    class="upload-demo"
    drag
    :multiple="false"
    accept=".pdf,application/pdf"
    :show-file-list="false"
    :auto-upload="false"
    :on-change="submitUpload"
  >
    <el-icon class="el-icon--upload"><upload-filled /></el-icon>
    <div class="el-upload__text">
      拖动文件到此处 或者 <em>点击上传</em>
    </div>
  </el-upload>
  <div class="processbox">
      <span>{{mes}}</span>
      <img src="@/assets/success-fill.png" class="mesimg" v-if="process==100"/>
      <img src="@/assets/loading.gif" class="mesimg" v-else-if="process>0"/>
      <el-progress :percentage="process" :stroke-width="15" striped-flow="true" duration="0" striped/>
  </div>

  <el-descriptions title="已经上传的文件" class="fileitem" v-if="step>0">
    <el-descriptions-item label="文件名">{{upfileinfo.name}}</el-descriptions-item>
    <el-descriptions-item label="大小">{{upfileinfo.size}}KB</el-descriptions-item>
    <el-descriptions-item label="最小压缩大小">{{ upfileinfo.maxcompressize }}KB</el-descriptions-item>
    <el-descriptions-item label="目标压缩大小(KB)">
      <el-input v-model="targetSize" type="number" ></el-input>
    </el-descriptions-item>
    <el-descriptions-item label="操作">
      <el-button type="primary" @click="checkinput">压缩</el-button>
      <el-button type="danger" @click="delfile('input')">删除</el-button>
    </el-descriptions-item>
  </el-descriptions>

  <pdf-item v-if="step>1" @compress="downloadfile" @delfile="delfile('output')" :info="filedata2" style="margin-left: 30px;margin-top: 20px;"></pdf-item>
  

<el-collapse v-model="activeNames" @change="handleChange" class="PdfItem" v-if="step>0">

  <el-collapse-item title="调整图像优先级" name="1">
    <div class="imagebox" style="margin-left: 30px;" v-if="step>0">
      <image-number :info="store.state.url+'/pdfimg/'+item+'?id='+store.state.userid" v-model="p[ix]" v-for="(item,ix) in imagelist" :key="ix"></image-number>
    </div>
  </el-collapse-item>


</el-collapse>
  
  
</template>

<script setup>
import { UploadFilled } from '@element-plus/icons-vue'
import ImageNumber from '@/components/ImageNumber.vue'
import { ElMessageBox } from 'element-plus'
import PdfItem from '@/components/PdfItem.vue'
import { QuestionFilled} from '@element-plus/icons-vue'
import { ref,onMounted,computed } from 'vue';
import axios from 'axios';
import {useStore} from 'vuex';

import { CollapseModelValue } from 'element-plus'
const activeNames = ref([])

const store = useStore();
var process=computed(() => {
	    return store.state.process
	})
var mes=computed(() => {
    return store.state.mes
})
var filedata=["已经上传的文件","test.pdf","文件大小","4.5MB","最小压缩大小","2.1MB",true]
var filedata2=ref(["完成压缩的文件","test-compress.pdf","文件大小","2.4MB","平均PSNR","21.0",false,0.83])
const upfileinfo=ref({
  name:"test.pdf",
  size:4.5,
  maxcompressize:2.0,
})
const v=1
var p=[]
const step=ref(0)
const imagelist=ref([])
const priority=[]
const indexx=[1,2,3,4,5]
const getdata=()=>{
  console.log(items)
}
const targetSize=ref(0)
const tips = () => {
    ElMessageBox.alert(
      "<strong>点击图片调整图片压缩优先级</strong>\
      <br/><span>图片的优先级越高</span>\
      <br/><span>压缩后的图片质量就越好</span>\
      <br/><span>相同分辨率下</span>\
      <br/><span>优先级为n的图片体积将是优先级为1的图片的n倍</span>",
      '压缩优先级',
      {
        dangerouslyUseHTMLString: true,
        showClose:false
      }
    )
  }

  const filestate={}
  var upfilename = ""
  const parsefile=()=>{
    axios.get(store.state.url+'/parseimage', {
      headers: {
          'Accept': 'application/json'
      },
      params: {
          uid: store.state.userid, // 查询参数
          filename: upfilename
      }
    })
    .then(response => {
        console.log('Response data:', response.data);
        p=Array(response.data.imagelist.length).fill(5)
        imagelist.value=response.data.imagelist
        //处理接收到的这部分数据
        filestate.fileMaxSize = response.data.filesize
        filestate.fileMinSize = response.data.emptysize
        //设置已经上传的文件信息
        upfileinfo.value.maxcompressize= response.data.emptysize+response.data.imgact*0.001
        upfileinfo.value.name=upfilename
        upfileinfo.value.size=response.data.filesize

        filestate.fileImgSize = response.data.imgsize
        filestate.imgact = response.data.imgact
        filestate.compressedSize = response.data.filesize
        filestate.state = 3
        step.value=1
        
        store.commit("setmes","文件上传解析完成")
    })
    .catch(error => {
        console.error('Error:', error);
    });
  }
  onMounted(() => {
    store.commit("setmes","选择文件上传")
    if(store.state.wslink==null){//建立连接
      store.commit('buildws')
    }
    else{
      console.log("连接已经建立",store.state.wslink)
    }
  })
  const checkinput=()=>{

    if(targetSize.value<filestate.fileMinSize){
      ElMessageBox.confirm('您输入的目标大小小于最小可压缩大小,输出文件可能达不到预期大小,确定继续吗?')
      .then(() => {
        start_compress()
      })
      .catch(() => {
        // catch error
      })
    }
    else start_compress()
  }
  //文件上传函数
  const submitUpload = (UploadFile) => {
    console.log("文件变化",UploadFile)
    
    const formData = new FormData();
    formData.append('file', UploadFile.raw);
    store.commit("setmes","正在上传文件")
    axios.post(store.state.url+'/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
      onUploadProgress: (progressEvent) => {
        // 计算上传进度
        const percentCompleted = Math.round(
          (progressEvent.loaded * 100) / progressEvent.total
        );
        store.commit("setprocess", percentCompleted); // 更新进度
      },
    })
    .then(response => {
      // this.message = response
      upfilename=response.data.filename
      store.commit("setmes","正在解析文件")
      // console.log("un",upfilename)
      console.log("返回消息:",response)
      parsefile()
      step.value=1
    })
    .catch(error => {
      store.commit("setmes","上传失败")
      console.log(error)
    });
}
//启动压缩:获取参数,发起请求
const start_compress=()=>{
  if (targetSize.value==null){
    targetSize.value=0
  }
  let params= {
          uid: store.state.userid, // 查询参数
          filename: upfilename,
          priority: p,
          imgurl:imagelist.value,
          maxsize: parseInt(targetSize.value),
          imgact:  filestate.imgact,
          emptysize: filestate.fileMinSize
    }
  axios.post(store.state.url+'/compresstoimage',params ,{
      headers: {
          'Accept': 'application/json'
      }
    })
      .then(response => {
          step.value=2
          console.log('Response data:', response.data);
          // filedata2=["完成压缩的文件","test-compress.pdf","文件大小","2.4MB","平均PSNR","21.0",false,0.83]
          filedata2.value[1]=upfilename,
          filedata2.value[3]=response.data.size,
          filedata2.value[5]=response.data.PSNR
          filedata2.value[7]=response.data.SSIM
          if(response.data.message=="notget"){
            ElMessageBox.alert('您的文件已经无法继续压缩,因此最终压缩的文件大于您的预设值', '压缩已达到极限!', {
            confirmButtonText: 'OK',
            })
          }
      })
      .catch(error => {
          console.error('Error:', error);
      });
}
const downloadfile=async ()=>{
  try {
      // 发送 GET 请求到后端下载接口
      const response = await fetch(store.state.url+'/download?name=' + upfilename);
      if (!response.ok) {
          throw new Error('文件下载失败');
      }

      // 将响应内容转换为 Blob 对象
      const blob = await response.blob();

      // 创建一个临时链接
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;

      // 设置下载文件的名称
      link.setAttribute('download', upfilename);  // 替换为实际文件名

      // 触发下载
      document.body.appendChild(link);
      link.click();

      // 清理临时链接

      document.body.removeChild(link);
      window.URL.revokeObjectURL(url);
  } catch (error) {
      console.error('下载失败:', error);
  }
}
const delfile=(isinput)=>{
  console.log("delete function")
  let params={  filename: upfilename,loc:isinput}
  axios.delete('http://127.0.0.1:5000/delfile', {
    params:params
  })
  .then(response => {
    console.log('Resource deleted successfully:', response.data);
    if(response.data.loc=="input"){
      step.value=0
      store.commit("setmes","选择文件上传")
    }
    else{
      step.value=1
      store.commit("setmes","文件解析完成")
    }
  })
  .catch(error => {
  console.error('Error deleting resource:', error);
  });
}
</script>

<style scoped>
.processbox{
  display: flex;
}
.processbox span{
  margin-left: 30px;
}
.el-progress {
width: 70%;
  margin-left: auto;
  margin-right: 20px;

}
.PdfItem{
  margin-left: 30px;
  margin-top: 20px;
}
.fileitem{
  margin-left: 30px;
  margin-right: 30px;
  margin-top: 20px;
  
  box-shadow: 0 0 5px 1px #999;    
  padding-left:30px;
}
.imagebox{
  display: flex;
  flex-wrap: wrap;
}
.el-input{
  width: 300px;
}
.mesimg{
  width: 30px;
  height: 30px;
  margin-left: auto;
  margin-right: 10px;
}
</style>
