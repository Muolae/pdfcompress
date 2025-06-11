<template>
    <div class="imagebox" @click="changepriority">
      <div class="priority">
        <h1 style="border:none;">{{pri}}</h1>
      </div>
      <el-image style="width: 100px; height: 100px" :src="info" fit="cover" />
    </div>
    
  </template>
    
<script setup>
import { ref,onMounted } from 'vue';
const url =require('@/assets/6c.jpg')
const props = defineProps({
    info:{
        type: Object,
        default: () => require('@/assets/6c.jpg')
    },
    modelValue:{
        type: Number,
        default: 5
    }
})
const  pri  = ref(props.value)
const emit = defineEmits(['update:modelValue'])
const changepriority=()=>{
    pri.value++;
    if(pri.value>9)pri.value=1;

    emit('update:modelValue',  pri.value)
}
onMounted(()=>{
    pri.value=props.modelValue
})

</script>
    
    <style scoped>
   .imagebox{
    width: 100px;
    height: 100px;
    border: 4px solid #e0dddd;
   }
   .imagebox:hover{
    border: 4px solid skyblue;
   }
   .imagebox:hover .priority{
    background: rgba(255, 255, 255, 0.4);
   }
   .priority{
    z-index: 99;
    position: absolute;
    width: 100px;
    height: 100px;
    justify-content: center;
    align-items: center;
    display:flex;
    background: rgba(255, 255, 255, 0.1);
   }
  
    </style>
    