<template>
    <div class="root">
        <h1>WORDLE</h1>
        <div class="wrapper">
            <div :class="[item.color, 'item']" v-for="item in items" :key="item.key">
                {{ item.text }}
            </div>
            <button 
                class="btn" v-if="game_status=='not finished'" 
                v-on:click="submit()">Проверить</button>
            <button :class="['btn', game_status]" v-else v-on:click="retry()">
                Начать заново
            </button>
        </div>
    </div>
</template>

<script>
import axios from 'axios'
import { toast } from 'vue3-toastify';
import 'vue3-toastify/dist/index.css';

export default {
name: 'GameView',
data(){
    return{
    token: "",
    game_status: "not finished",
    currentKey: 0,
    items: Array.from({ length: 30 }, (_, index) => ({
        key: index,
        text: "",
        color: "common"
    }))
    }
},
methods: {
    getCurrentItem(){
    return this.items.find(item => item.key === this.currentKey)
    },
    getCurrentWord(){
    let word = ""
    for (let i = this.currentKey-4; i < this.currentKey+1; i++) 
        word += this.items.find(item => item.key === i).text
    return word
    },
    getItemFromIndex(i){
    return this.items.find(item => item.key === i)
    },
    isLetter(keyCode){
    return (([219, 221, 186, 222, 190, 191, 188, 192].includes(keyCode)) || 
    (keyCode <= 90 && keyCode >= 65))
    },
    showToast(type, message){
    switch (type) {
        case 'warning':
        toast.warning(message,{
            timeout: 2000,
            closeOnClick: true,
            pauseOnHover: false,
            position: 'bottom-right'
        })
        break
        case 'success':
        toast.success(message,{
            timeout: 2000,
            closeOnClick: true,
            pauseOnHover: false,
            position: 'bottom-right'
        })
        break
        case 'error':
        toast.error(message,{
            timeout: 2000,
            closeOnClick: true,
            pauseOnHover: false,
            position: 'bottom-right'
        })
        break
    }
    },
    startGame(){
    axios.get('http://127.0.0.1:8000/create_room')
        .then(response => {
        window.localStorage.setItem('wordle_token', response.data)
        this.token = response.data
        this.showToast("success", "Игра началась!")
        })
        .catch(error => {
        console.error(error);
        });
    },
    submit(){
    if (this.game_status != "not finished") {
        this.showToast("warning", 'Игра уже завершена')
        return
    }
    if(this.currentKey%5==4 && this.getCurrentItem().text != ""){
        let word = this.getCurrentWord()
        const data = {
        token: this.token,
        word: word,
        }
        axios.post('http://127.0.0.1:8000/add_word', data)
        .then(response => {
            if ('message' in response.data)
            this.showToast(
                response.data.message.type, 
                response.data.message.text
            )
            this.game_status = response.data.game_status
            let word_object = response.data.word
            if (word_object.length == 5){
            for (let i = 0; i < word_object.length; i++){
                let letter_object = word_object[i]
                let item = this.getItemFromIndex(letter_object.position)
                item.color = letter_object.color
            }
            this.currentKey++
            }
        })
        .catch(error => {
            console.error(error);
        });
    }
    else
        this.showToast("warning", 'В слове не хватает букв!')
    },
    retry(){
    axios.get('http://127.0.0.1:8000/retry_game', {
        params: {
        token: this.token,
        }
    })
    .then(response => {
        this.game_status = "not finished"
        this.currentKey = 0
        for (let i = 0; i < 30; i++){
        let item = this.getItemFromIndex(i)
        item.color = "common"
        item.text = ""
        }
        this.showToast("success", "Игра началась!")
    })
    .catch(error => {
        console.error(error);
    });
    },
    onKeyDown(e) {
    // Backspace handler
    if (this.game_status != "not finished") {
        this.showToast("warning", "Игра уже завершена")
        return
    }
    if(e.keyCode == 8){
        let item = this.getCurrentItem()
        if(this.currentKey%5==0 || (this.currentKey%5==4 && item.text != "")) {
        item.text = ""
        return
        }
        this.currentKey--
        item = this.getCurrentItem()
        item.text = ""
    }
    // Letters handler
    if(this.isLetter(e.keyCode)){
        const item = this.getCurrentItem()
        if(this.currentKey%5==4 && item.text != "") return
        item.text = e.key
        if(this.currentKey%5==4) return
        this.currentKey++
    }
    // Enter handler
    if(e.keyCode == 13){
        this.submit()
    }
    },
},
created() {
    document.addEventListener('keydown', this.onKeyDown.bind(this))
    let token = window.localStorage.getItem('wordle_token')
    if(token==null) this.startGame()
    else {
    this.token = token
    let data = {
        token: token
    }
    axios.post('http://127.0.0.1:8000/get_room_data', data)
        .then(response => {
            let words = response.data.words
            this.game_status = response.data.game_status
            for (let i=0; i < words.length; i++){
            let letters = words[i].word
            for (let i=0; i < letters.length; i++){
                let letter_object = letters[i]
                let item = this.getItemFromIndex(letter_object.position)
                item.color = letter_object.color
                item.text = letter_object.letter
                this.currentKey++
            }
            }
        })
        .catch(error => {
            console.error(error);
        });
    }
},
}
</script>
<style scoped>
.btn{
margin-top: 50px;
width: 100%;
height: 50px;
border: none;
font-size: 20px;
background: #ccc;
}

.Win{
    background: #70eb80;
    color: #fff;
}

.Lose{
    background: #b92a2a;
    color: #fff;
}

.root{
text-align: center;
margin-top: 40px;
}
.wrapper{
width: 350px;
margin: 0 auto;
margin-bottom: 100px;
align-items: center;
}
.item {
position: relative;
width: 60px;
height: 60px;
float: left;
margin: 5px;
cursor: pointer;
display: flex;
justify-content: center;
align-items: center;
font-size: 25px;
}

.green{
background: #70eb80;
color: #fff;
}

.gray{
background: #616161;
color: #a59b9b;
}

.yellow{
background: #e2bf24;
color: #fff;
}

.common{
background: #ccc;
color: black;
}

h1{
margin-bottom: 50px;
}

</style>
