<template>
    <div class="root">
        <h1>WORDLE</h1>
        <div class="wrapper">
            <div :class="[item.color, 'item']" 
                v-for="item in items" :key="item.key"
            >
                {{ item.text }}
            </div>
            <button class="btn">Проверить</button>
        </div>
    </div>
</template>

<script>

export default {
    name: 'GameView',
    data(){
        return{
            items: Array.from({ length: 30 }, (_, index) => ({
                key: index,
                text: "",
                color: "common"
            }))
        }
    }
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
