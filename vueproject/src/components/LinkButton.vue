<template>
  <div class="linkbtn" @click="click">
    <img :src="src" class="imgx"/>
    <span class="linktext">{{info}}</span>
  </div>
</template>

<script setup>
  const props = defineProps({
    src:{
            type: String,
            default: '@/assets/QQ.png',
        },
    info:{
        type: String,
        default: 'info',
    }
})
const emit = defineEmits(['update:modelValue'])
const click=()=>{
    emit("beclick")
}
</script>b

<style scoped>
.linkbtn{
    width:auto;
    height: 30px;
    border: 1px solid #1296db;
    display: flex;
    background-color: rgba(255, 255, 255, 0.1);
    align-items: center;
    border-radius: 6px;
    color: #1296db;
    margin-left: 20px;
}
.linkbtn:hover{
    border: 1px solid #fff;
}
.imgx{
    width: 20px;
    height: 20px;
    margin-left: 10px;
}
.linktext{
    margin-left: 10px;
    padding-right: 10px;
}
</style>