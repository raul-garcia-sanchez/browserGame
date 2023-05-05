import { createApp } from 'vue'

var app = createApp({
    el: "#app",
    delimiters: ['[[', ']]'],
    data() {
        return {
            users: [],
            elemsPage: 100,
            dataPaginate: [],
            actualPage: 1,
        }
    },
    mounted() {
        fetch('../api/get_ranking').then(response => {
            return response.json()
        })
        .then(data => {
            this.users = data.ranking;
        this.getDataPage(1)
        })
        .catch(error => {
            console.log(error);
        })
        
    },
    methods: {
        totalPages() {
            return Math.ceil(this.users.length / this.elemsPage)
        },
        getDataPage(numPage) {
            this.actualPage = numPage
            this.dataPaginate = []
            let ini = (numPage * this.elemsPage) - this.elemsPage
            let fin = (numPage * this.elemsPage)
            this.dataPaginate = this.users.slice(ini, fin)
            console.log("pagData",this.dataPaginate);
        },
        getPreviousPage() {
            if (this.actualPage > 1) {
                this.actualPage--;
            }
            this.getDataPage(this.actualPage)
        },
        getNextPage() {
            if (this.actualPage < this.totalPages()) {
                this.actualPage++;
            }
            this.getDataPage(this.actualPage)

        },
        isActive(numPage) {
            return numPage == this.actualPage ? 'active' : ''
        }
    }
})

app.mount('#app')