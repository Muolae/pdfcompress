<template>
  <h1>控制图片质量损失</h1>
    <el-text>基于图片质量损失(PSNR)的PDF压缩,确保您的图片质量</el-text>
    <el-upload
      class="upload-demo"
      drag
      :multiple="false"
      accept=".pdf,application/pdf"
      :auto-upload="false"
      :on-change="submitUpload"
      :show-file-list="false"
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
    <h4 class="title1">已经上传的文件</h4>
    <el-descriptions
      class="margin-top"
      style="margin-top:20px;"
      :title="已经上传的文件"
      :column="1"
      :size="size"
      border
      v-if="step>0"
    >
      <el-descriptions-item>
        <template #label>
          <div class="cell-item">
            
            文件名
          </div>
        </template>
       {{ upfileinfo.name }}
      </el-descriptions-item>
      <el-descriptions-item>
        <template #label>
          <div class="cell-item">
            
            文件大小
          </div>
        </template>
       {{ upfileinfo.size }}KB
      </el-descriptions-item>
      <el-descriptions-item>
        <template #label>
          <div class="cell-item">
            预计压缩大小
          </div>
        </template>
       {{ GetEstimateSize }}KB
      </el-descriptions-item>
      
      <el-descriptions-item >
        <template #label>
          <div class="cell-item">
            目标质量(PSNR)
              <el-icon :style="iconStyle" class="icon" @click="tips"><QuestionFilled /></el-icon>
          </div>
        </template>
        <el-slider v-model="value" :marks="marks" :format-tooltip="tipsformat" :max="50" :step="0.1"/>
      </el-descriptions-item>

      <br/>
      <el-descriptions-item >
        <template #label>
          <div class="cell-item">
           
            操作
          </div>
        </template>
        <el-button type="primary" @click="start_compress">压缩</el-button>
        <el-button type="danger" @click="delfile('input')" >删除</el-button>
      </el-descriptions-item>
    </el-descriptions>
    <PdfItem :info="filedata2" @compress="downloadfile" @delfile="delfile('output')" v-if="step>1"></PdfItem>
    
  </template>
  
<script setup>
import { reactive, ref,computed,onMounted } from 'vue'
  import { UploadFilled } from '@element-plus/icons-vue'
  import PdfItem from '@/components/PdfItem.vue';
  import {QuestionFilled} from '@element-plus/icons-vue'
  import axios from 'axios';
  import {useStore} from 'vuex';
  var filedata2=ref(["完成压缩的文件","test-compress.pdf","文件大小","2.4MB","平均PSNR","21.0",false,0.83])
  const store = useStore();
  onMounted(() => {
    store.commit("setmes","选择文件上传")
    if(store.state.wslink==null){//建立连接
      store.commit('buildws')
    }
    else{
      console.log("连接已经建立",store.state.wslink)
    }
  })
  const step=ref(0)
  var process=computed(() => {
	    return store.state.process
	})
  var mes=computed(() => {
	    return store.state.mes
	})
  const GetEstimateSize=computed(()=>{
    let compressRate=0.0004184*Math.exp(0.14269*value.value)-0.00934
    return filestate.fileMinSize+compressRate*filestate.imgact
  })
  var upfilename=ref('test')
  const upfileinfo=ref({
    name:"test.pdf",
    size: 4.1,
    testsize:3
  })
  const onssim=ref(false)
  const value = ref(30)
  const marks = reactive({
    10: {
      style: {
        color: 'red',
      },
      label:'图像质量难以接受'
    },
    20: {
      style: {
        color: '#FFA500',
      },
      label:'图像质量较差'
    },
    30: {
      style: {
        color: '#32CD32',
      },
      label: '有可以察觉的失真'
    },
    40: {
      style: {
        color: '#1989FA',
      },
      label: '几乎无损',
    },
    50: {
      style: {
        color: '#1989FA',
      },
      label: '与原图一致',
    },
  })
  const tipsformat=(value)=>{
    return 'PSNR:'+String(value)
  }
  const iconStyle = computed(() => {
    const marginMap = {
      large: '8px',
      default: '6px',
      small: '4px',
    }
    return {
      marginRight: marginMap.small,
    }
  })

  import { ElMessageBox } from 'element-plus'
  
  const tips = () => {
    ElMessageBox.alert(
      "<strong>PSNR(峰值信噪比)是一个评估图片质量损失的参数</strong>\
      <br/><span>一般情况下:</span>\
      <br/><span>PSNR高于40dB说明图像质量极好,即非常接近原始图像</span>\
      <br/><span>在30—40dB通常表示图像质量是好的即失真可以察觉但可以接受</span>\
      <br/><span>在20—30dB说明图像质量差</span>\
      <br/><span>最后PSNR低于20dB图像一般不可接受</span>",
      'PSNR',
      {
        dangerouslyUseHTMLString: true,
        showClose:false
      }
    )
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
  const filestate={
    fileMinSize:0,
    imgact:0
  }
  //启动文件预处理请求
  const parsefile=()=>{
    step.value=1
    axios.get(store.state.url+'/parsefile', {
      headers: {
          'Accept': 'application/json'
      },
      params: {
          uid: store.state.userid, // 查询参数
          filename: upfilename.value
      }
    })
    .then(response => {
        console.log('Response data:', response.data);
        //处理接收到的这部分数据
        filestate.fileMaxSize = response.data.filesize
        filestate.fileMinSize = response.data.emptysize
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
        upfilename.value=response.data.filename
        store.commit("setmes","正在解析文件")
        // console.log("un",upfilename)
        console.log("返回消息:",response)
        upfileinfo.value.name=UploadFile.name
        upfileinfo.value.size=UploadFile.size/1024  
        parsefile()
        // step.value=1
      })
      .catch(error => {
        store.commit("setmes","上传失败")
        console.log(error)
      });
}
const start_compress=()=>{
  var that = this
  axios.get(store.state.url+'/compresstopsnr', {
      headers: {
          'Accept': 'application/json'
      },
      params: {
          uid: store.state.userid, // 查询参数
          filename: upfilename.value,
          psnr:value.value,
          ssimon:onssim.value
      }
    })
      .then(response => {
        step.value=2
        console.log('Response data:', response.data);
        const responseData = typeof response.data === 'string' ? JSON.parse(response.data) : response.data;
        // Assign values
        filedata2.value[1] = upfilename.value;
        filedata2.value[3] = responseData.size;
        filedata2.value[5] = responseData.PSNR;
        filedata2.value[7] = responseData.SSIM;
      })
      .catch(error => {
          console.error('Error:', error);
      });
}

const downloadfile=async ()=>{
  try {
      // 发送 GET 请求到后端下载接口
      const response = await fetch(store.state.url+'/download?name=' + upfilename.value);
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
      link.setAttribute('download', upfilename.value);  // 替换为实际文件名

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

<style lang="scss">
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
.title1{
    margin-left: 0px;
    width: 120px;
}
.el-slider{
    width: 700px;
}
.icon{
    margin-top: 12px;
}
.mesimg{
  width: 30px;
  height: 30px;
  margin-left: auto;
  margin-right: 10px;
}
</style>
  