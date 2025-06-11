<template>
  <el-descriptions
      class="margin-top"
      :title="info[0]"
      :column="3"
      :size="size"
      border
    >
      <el-descriptions-item>
        <template #label>
          <div class="cell-item">
            
            文件名
          </div>
        </template>
        {{ info[1] }}
      </el-descriptions-item>
      <el-descriptions-item>
        <template #label>
          <div class="cell-item">
            
            {{ info[2] }}
          </div>
        </template>
        {{info[3]}}
      </el-descriptions-item>
      <el-descriptions-item>
        <template #label>
          <div class="cell-item">
           
            {{ info[4] }}
          </div>
        </template>
        {{ info[5] }}
      </el-descriptions-item>

      <el-descriptions-item v-if="info[6]" >
        <template #label>
          <div class="cell-item">
            
            目标压缩大小(KB)
          </div>
        </template>
        <el-input v-model="target" type="number" @input="inputsize" placeholder="输入目标文件最大大小" ></el-input>
      </el-descriptions-item>
      <el-descriptions-item v-else >
        <template #label>
          <div class="cell-item">
            平均SSIM
          </div>
        </template>
        <span>{{ info[7] }}</span>
        <!-- <el-input v-model="info[7]" disabled="true"  placeholder="输入目标文件最大大小" ></el-input> -->
      </el-descriptions-item>

      <el-descriptions-item v-if="info[6]">
        <template #label>
          <div class="cell-item">
           
            操作
          </div>
        </template>
        <el-button type="primary" @click="compress">压缩</el-button>
        <el-button type="danger" @click="delfile">删除</el-button>
      </el-descriptions-item>
      <el-descriptions-item v-else>
        <template #label>
          <div class="cell-item">
           
            操作
          </div>
        </template>
        <el-button type="success" @click="compress">下载</el-button>
        <el-button type="danger" @click="delfile">删除</el-button>
      </el-descriptions-item>
    </el-descriptions>
</template>

<script setup>
  import { computed, ref } from 'vue'
  import {
    Iphone,
    Location,
    OfficeBuilding,
    Tickets,
    User,
  } from '@element-plus/icons-vue'
  
  const iconStyle = computed(() => {
    const marginMap = {
      large: '8px',
      default: '6px',
      small: '4px',
    }
    return {
      marginRight: marginMap.default,
    }
  })
  const target=ref(0)
  const emit = defineEmits(['update:modelValue'])
  const inputsize=(e)=>{
    // console.log(e)
     target.value=e
    if(e==null|e=='')e=0;
    emit('update:modelValue', parseInt(e))
  }
  const compress=()=>{
    emit("compress")
  }
  const delfile=()=>{
    emit("delfile")
  }
  const props = defineProps({
    info:{
            type: Array,
            default: () => ["已经上传的文件","test.pdf","文件大小","4.5MB","最小压缩大小","2.1MB",true,0.7],
        },
    modelValue:{
        type: Number,
        default: 0
    }
});
</script>

<style>
.teat{
    width: 280px;
}
</style>