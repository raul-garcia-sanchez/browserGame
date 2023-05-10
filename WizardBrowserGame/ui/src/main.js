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
import ModalCreator from './components/modalCreator.vue'
import axios from 'axios'
import Cookies from 'js-cookie'

var app2 = createApp({
    el: "#app2",
    delimiters: ["[[", "]]"],
    data() {
        return {
            user: [],
            userRanking: [],
            eventActions: [],
            actions: [],
            allUsers: []
        };
    },
    async mounted() {
        await this.updateData(true);
        await this.getActions();
        this.csrfToken = Cookies.get('csrftoken');
        this.disableOutOfManaButtons();
    },
    components: {
        'modal-creator': ModalCreator,
    },
    methods: {
        newError(tipoMensaje, texto) {
            const error = document.createElement('div');
            error.className = `${tipoMensaje} text-center flex justify-between`;
            error.innerHTML = `
                <ul>
                <li>${texto}</li>
                </ul>
                <span class="closebtn self-center" onclick="this.parentElement.remove();">&times;</span>
            `;
            const mensajes = document.getElementById('mensajes');
            mensajes.appendChild(error);
        },
        enviarFormulario(actionSelected) {
            var dataToSend = {
                action_id: actionSelected.id,
                id_user_transmitter: this.user.id,
                id_user_receiver: this.user.id
            };

            axios.post('/api/make_action', dataToSend, {
                headers: { 'X-CSRFToken': this.csrfToken },
            })
                .then(response => {
                    var message = "";
                    if (actionSelected.action_type == 2) {
                        message = (response.data.action_succeed)  //If action succeeded
                            ? `Has realitzat correctament <strong><i>${actionSelected.name}</i></strong> i t'has curat<br>`
                            : `No has realitzat correctament <strong><i>${actionSelected.name}</i></strong><br>`
                    }
                    else if (actionSelected.action_type == 3) {
                        message = (response.data.action_succeed)  //If action succeeded
                            ? `Has realitzat correctament <strong><i>${actionSelected.name}</i></strong> i has guanyat punts d'experiència<br>`
                            : `No has realitzat correctament <strong><i>${actionSelected.name}</i></strong><br>`
                    }

                    message += (response.data.levelUp)
                        ? `Has pujat de nivell a <strong>${Number(this.user.level) + 1 }</strong><br>`
                        : ``

                    if (response.data.action_succeed) this.newError("success", message);
                    else this.newError("info", message);

                    this.resetParamters();
                })
                .catch(error => {
                    console.log(error)
                    let message = "Error del servidor";
                    this.newError("error", message)
                })
        },
        displayActionModal(action) {
            this.$refs[action.id][0].abrirDialogo();
        },
        resetParamters: async function () {
            await this.updateData(false);
            await this.disableOutOfManaButtons();
        },
        disableOutOfManaButtons() {
            let buttons = document.getElementsByClassName("btnImage");
            for (let button of buttons) {
                let idButtonAction = button.id
                let actionOfButton = this.getActionById(idButtonAction.split("_")[1])
                if (actionOfButton.cost > this.user.mana) {
                    this.disableActionButton(button)
                }
                else{
                    this.enableActionButton(button)
                 }

            }
        },

        disableActionButton(button){
            var imageUrl = button.style.backgroundImage.slice(4, -1).replace(/['"]/g, "");
            var image = new Image();
            image.src = imageUrl;
            const canvas = document.createElement('canvas');
            const context = canvas.getContext('2d');
            canvas.width = image.width;
            canvas.height = image.height;
            context.drawImage(image, 0, 0);
            var dataUrl = canvas.toDataURL();
            button.style.backgroundImage = `url(${dataUrl})`;
            button.style.filter = 'grayscale(100%)';

            button.style.cursor = "default";
            button.disabled = true;
        },
        enableActionButton(button){
            button.disabled = false;
            button.style.cursor = "pointer"
            button.style.filter = 'none';
        },
        getActionById(idAction) {
            const actionToReturn = this.actions.find((action) => {
                return action.id == idAction;
            });
            return actionToReturn
        },
        getActions: async function () {
            await fetch("../api/get_actions")
                .then((response) => {
                    return response.json();
                })
                .then((response) => {
                    this.actions = response.actions;
                })
                .catch((error) => {
                    console.log("Could not get actions:", error);
                });
        },
        updateData: async function (shouldTimeout) {
            await fetch("../api/get_resources")

            await fetch("../api/get_user")
                .then((response) => {
                    return response.json();
                })
                .then((data) => {
                    if (data) {
                        this.user = data.user;
                        fetch("../api/get_ranking")
                            .then((response2) => {
                                return response2.json();
                            })
                            .then((data2) => {

                                const userRanking = data2.ranking.find((user) => {
                                    return user.username === this.user.username;
                                });

                                this.allUsers = data2.ranking.filter(user => {
                                    if (
                                        (user.level === userRanking.level ||
                                        (user.level - 1) === userRanking.level ||
                                        (user.level + 1) === userRanking.level)
                                        && (user.id != this.user.id) 
                                        && !(user.is_staff) 
                                        && (user.level > 0)
                                    ) {
                                        return true
                                    }
                                });
                                this.userRanking = userRanking;
                                fetch("../api/get_events")
                                    .then((response3) => {
                                        return response3.json();
                                    })
                                    .then((data3) => {
                                        this.eventActions = data3.actions;
                                        this.eventActions.forEach((action) => {
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
                                        })
                                    })
                                    .finally(() => {
                                        if (shouldTimeout) {
                                            setTimeout(async () => {
                                                await this.updateData(true);
                                                this.disableOutOfManaButtons();
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
