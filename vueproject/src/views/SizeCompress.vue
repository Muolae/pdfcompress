<template>
    <h1>PDF文件定量压缩</h1>
    <el-text>将PDF文件压缩到您指定的大小,并且达到最小的质量损失.</el-text>
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
        <el-progress :percentage="process" :stroke-width="15" :striped-flow="true" :duration="0" striped/>
    </div>
    <div v-if="step>0">
      <el-switch v-model="onssim" />
      <el-text style="margin-left: 10px;">计算输出文件的SSIM值</el-text>
      <QuestionFilled style="width: 16px;margin-top: 8px;" @click="ssimtip"/>
    </div>
    

    <PdfItem :info="filedata" v-model="limitsize" @compress="checkinput" @delfile="delfile('input')" v-if="step>0"></PdfItem>
    <PdfItem :info="filedata2" @compress="downloadfile" @delfile="delfile('output')" v-if="step>1"></PdfItem>
    
  </template>
  
<script setup>
  import { UploadFilled } from '@element-plus/icons-vue'
  import { ElMessageBox } from 'element-plus'
    import {QuestionFilled} from '@element-plus/icons-vue'
  import PdfItem from '@/components/PdfItem.vue';
  import { ref,onMounted,computed } from 'vue';
  import axios from 'axios';
  import {useStore} from 'vuex';
  //data
  
  const step=ref(0)//0:未上传文件 1:已经上传文件 2:完成压缩
  var filedata=ref(["已经上传的文件","test.pdf","文件大小","4.5MB","最小压缩大小","2.1MB",true])
  var filedata2=ref(["完成压缩的文件","test-compress.pdf","文件大小","2.4MB","平均PSNR","21.0",false,0.83])
  //建立或者检查socket连接
  const store = useStore();
  var process=computed(() => {
	    return store.state.process
	})
  var mes=computed(() => {
	    return store.state.mes
	})
  const filestate={}
  var limitsize=0
  const onssim=ref('false')
  var upfilename = ""
  const parsefile=()=>{
    axios.get(store.state.url+'/parsefile', {
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
        //处理接收到的这部分数据
        filestate.fileMaxSize = response.data.filesize
        filestate.fileMinSize = response.data.emptysize
        filedata.value[5]=filestate.fileMinSize+response.data.imgact*0.001
        filestate.fileImgSize = response.data.imgsize
        filestate.imgact = response.data.imgact
        filestate.compressedSize = response.data.filesize
        filestate.state = 3
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
  //文件上传函数
  const submitUpload = (UploadFile) => {
      console.log("文件变化",UploadFile)
      if(!String(UploadFile.name).endsWith('.pdf')){
        ElMessageBox.alert(
      "<strong>文件格式不符合要求</strong>\
      <br/><span>请上传pdf格式的文件</span>",
      '提示',
      {
        dangerouslyUseHTMLString: true,
        showClose:false
      }
      ) 
      return;
      }
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
        filedata.value=["已经上传的文件",UploadFile.name,"文件大小(KB)",UploadFile.size/1024,"预计最小压缩大小","正在计算",true]   
        parsefile()
        step.value=1
        //文件上传完成,建立ws连接
        // this.buildWebSocket()
      })
      .catch(error => {
        store.commit("setmes","上传失败")
        console.log(error)
      });
}
const checkinput=()=>{
  console.log(limitsize)
  if(limitsize<filedata.value[5]){
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
//启动压缩:获取参数,发起请求
const start_compress=()=>{
  axios.get(store.state.url+'/compresstosize', {
      headers: {
          'Accept': 'application/json'
      },
      params: {
          uid: store.state.userid, // 查询参数
          filename: upfilename,
          compressrate: 95,
          maxsize: limitsize,
          imgrate: (limitsize - filestate.fileMinSize) / filestate.imgact,
          emptysize: filestate.fileMinSize,
          ssimon:onssim.value,
          target:limitsize
      }
    })
      .then(response => {
        step.value=2
          console.log('Response data:', response.data);
          filedata2.value=["完成压缩的文件",upfilename,"文件大小",response.data.size,"平均PSNR",response.data.PSNR,false,response.data.SSIM]
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
const testf=()=>{
  console.log(1,limitsize)
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
const ssimtip=()=>{
  ElMessageBox.alert(
      "<strong>SSIM(结构衡量指标)是一个评估图片质量损失的参数</strong>\
      <br/><span>与PSNR相比,SSIM更加符合人眼感受</span>\
      <br/><span>SSIM高于0.9说明图像失真几乎不可察觉非常接近原始图像</span>\
      <br/><span>在0.7—0.9通常表示图像存在可以接受的轻微失真</span>\
      <br/><span>在0.7说明图像质量差,0.5以下说明图像质量几乎不可接受</span>\
      <br/><strong>开启此选项时,系统会计算压缩后PDF文件中的图片平均SSIM,但是会导致压缩时间大幅增加,请耐心等待</strong>",
      'SSIM',
      {
        dangerouslyUseHTMLString: true,
        showClose:false
      }
    )
}
const delfile=(isinput)=>{
  console.log("delete function")
  let params={  filename: upfilename,loc:isinput}
  axios.delete(store.state.url+'/delfile', {
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
.mesimg{
  width: 30px;
  height: 30px;
  margin-left: auto;
  margin-right: 10px;
}
</style>
  