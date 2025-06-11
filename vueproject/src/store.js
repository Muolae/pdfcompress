import { createStore } from 'vuex'
import axios from 'axios'
export default createStore({
    state: {
        count: 6,
        wslink: null,
        userid: '',
        process: 0,
        mes: '等待上传文件',
        // url: 'http://47.104.6.104:5000',
        url: 'http://127.0.0.1:5000'

    },
    mutations: {
        increment(state, n) {
            // 变更状态
            state.count += n
        },
        setprocess(state, n) {
            state.process = parseInt(n)
        },
        setmes(state, mes) {
            state.mes = mes
        },
        buildws(state) {
            state.wslink = new WebSocket('ws://' + "127.0.0.1:5000" + '/ws');
            state.wslink.onmessage = (event) => {
                let response = event.data;
                console.log('ws res:', response)
                //获取到ws数据,根据type和wsid获取消息类型和
                let mestype = response.split(':')[0]
                if (mestype == 'id') {//记录uid数据
                    // store.commit('saveid', response.split(':')[1])
                    state.userid = response.split(':')[1]
                }
                else if (mestype == 'reg') {//处理进度条请求
                    state.process = parseInt(response.split(':')[1])

                }
                else if (mestype == 'info') {//处理提示位置
                    state.mes = response.split(':')[1]
                }
            };
        },
        setws(state, onmes) {
            state.wslink.onmessage = onmes
        },
        saveid(state, id) {
            state.userid = id
        }
    },
    actions: {
    },
    modules: {
    }
})

