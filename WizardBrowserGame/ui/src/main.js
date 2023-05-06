import { createApp } from "vue";

/* VUE COMPONENT RANKING */
var app = createApp({
  el: "#app",
  delimiters: ["[[", "]]"],
  data() {
    return {
      users: [],
      elemsPage: 100,
      dataPaginate: [],
      actualPage: 1,
    };
  },
  mounted() {
    fetch("../api/get_ranking")
    .then((response) => {
      return response.json();
    })
    .then((data) => {
      this.users = data.ranking;
      this.getDataPage(1);
    })
    .catch((error) => {
      console.log(error);
    });
  },
  methods: {
     getRanking(){
      fetch("../api/get_ranking")
      .then((response) => {
        return response.json();
      })
      .then(async (data) => {
        this.users = await data.ranking;
      })
      .catch((error) => {
        console.log(error);
      });
    },
    totalPages() {
      return Math.ceil(this.users.length / this.elemsPage);
    },
    getDataPage(numPage) {
      this.actualPage = numPage;
      this.dataPaginate = [];
      let ini = numPage * this.elemsPage - this.elemsPage;
      let fin = numPage * this.elemsPage;
      this.getRanking();
      this.dataPaginate = this.users.slice(ini, fin);
      
    },
    getPreviousPage() {
      if (this.actualPage > 1) {
        this.actualPage--;
      }
      this.getDataPage(this.actualPage);
    },
    getNextPage() {
      if (this.actualPage < this.totalPages()) {
        this.actualPage++;
      }
      this.getDataPage(this.actualPage);
    },
    isActive(numPage) {
      return numPage == this.actualPage ? "active" : "";
    },
  },
});

app.mount("#app");

/* VUE COMPONENT LANDING WHEN YOU ARE LOGGED */

var app2 = createApp({
  el: "#app2",
  delimiters: ["[[", "]]"],
  data() {
    return {
      user: [],
      userRanking: []
    };
  },
  mounted() {
    this.updateData();
  },
  methods: {
    updateData: function () {
      fetch("../api/get_user")
        .then((response) => {
          return response.json();
        })
        .then((data) => {
          if (data) {
            fetch("../api/get_ranking")
              .then((response2) => {
                return response2.json();
              })
              .then((data2) => {
                this.user = data.user[0];
                const userRanking = data2.ranking.find((user) => {
                  return user.username === this.user.username;
                });
                this.userRanking = userRanking
                setTimeout(this.updateData,30000)
              })
              .catch((error2) => {
                console.log(error2);
              });
          }
          
          
        })
        .catch((error) => {
          console.log(error);
        });
    },
  },
});

app2.mount("#app2");
