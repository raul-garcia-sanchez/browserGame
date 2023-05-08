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
        getRanking() {
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
            userRanking: [],
            actions: []
        };
    },
    mounted() {
        this.updateData(true);
    },
    methods: {
        updateData: function (shouldTimeout) {
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
                                this.user = data.user;
                                const userRanking = data2.ranking.find((user) => {
                                    return user.username === this.user.username;
                                });
                                this.userRanking = userRanking;
                                fetch("../api/get_events")
                                    .then((response3) => {
                                        return response3.json();
                                    })
                                    .then((data3) => {
                                        this.actions = data3.actions;
                                        this.actions.forEach((action) => {
                                            let newDate = new Date(action.date)
                                            const options = {
                                                day: 'numeric',
                                                month: 'long',
                                                year: 'numeric',
                                                hour: 'numeric',
                                                minute: 'numeric',
                                                hour12: false
                                            }
                                            const formatter = new Intl.DateTimeFormat('ca-ES', options);
                                            action.date = formatter.format(newDate);
                                        });
                                    })
                                    .finally(() => {
                                        if (shouldTimeout) {
                                            setTimeout(() => {
                                                this.updateData(true);
                                            }, 30000);
                                        }
                                    });
                                
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

/* VUE COMPONENT LANDING WHEN YOU ARE NOT LOGGED */

var app3 = createApp({
    el: "#app3",
    delimiters: ["[[", "]]"],
    data() {
        return {
            gameOptions: [],
        };
    },
    mounted() {
        this.getGameOptions();
    },
    methods: {
        getGameOptions() {
            fetch("../api/get_gameOptions")
                .then((response) => {
                    return response.json();
                })
                .then((data) => {
                    this.gameOptions = data.gameOptions[0];
                    const dateStart = new Date(this.gameOptions.game_datetime_start);
                    const dateEnd = new Date(this.gameOptions.game_datetime_end)
                    const options = {
                        day: 'numeric',
                        month: 'long',
                        year: 'numeric',
                        hour: 'numeric',
                        minute: 'numeric',
                        hour12: false
                    }
                    const formatter = new Intl.DateTimeFormat('ca-ES', options);
                    this.gameOptions.game_datetime_start = formatter.format(dateStart);
                    this.gameOptions.game_datetime_end = formatter.format(dateEnd);
                    const dateNow = new Date();
                    let minutesNow = dateNow.getMinutes();
                    let minutesToReturn = this.gameOptions.mins_between_turns - (minutesNow % this.gameOptions.mins_between_turns)
                    if (dateEnd <= dateNow) {
                        this.gameOptions.minutes = "El joc ha acabat"
                    }
                    else if (dateEnd >= dateNow && dateNow >= dateStart) {
                        this.gameOptions.minutes = minutesToReturn + " minuts"
                    }
                    else {
                        this.gameOptions.minutes = "El joc encara no ha començat"
                    }
                    setTimeout(this.getGameOptions, 30000);
                })
                .catch((error) => {
                    console.log(error);
                });
        },
    },
});

app3.mount("#app3");
