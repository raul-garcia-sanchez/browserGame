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
import ModalSimpleCreator from './components/modalSimpleCreator.vue'

var app2 = createApp({
    el: "#app2",
    delimiters: ["[[", "]]"],
    data() {
        return {
            user: [],
            userRanking: [],
            eventActions: [],
            actions: [],
            allUsers: [],
            loading: false
        };
    },
    async mounted() {
        this.loading = true;
        await this.updateData(true);
        await this.getActions();
        this.disableOutOfManaButtons();
        this.loading = false;
    },
    components: {
        'modal-creator': ModalCreator,
        'modal-simple': ModalSimpleCreator
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
        displayActionModal(action) {
            this.$refs[action.id][0].abrirDialogo();
        },
        async displayAnimation(response) {
            let action = response.action
            let modeAnimation = document.getElementById("animationContainer");
            let containerAnimation = document.getElementById("animationDisplayer");
            if (response.succeed) {
                modeAnimation.classList.remove("hidden");
                switch (action.id) {
                    case 1:
                        containerAnimation.innerHTML = `
                            <div id="glacius">
                                <img id="glaciusImg" src="/static/VisualResources/Glacius/glacius.png" alt="glaciusImg">
                                <img id="wizard_stand" src="/static/VisualResources/Glacius/wizard_stand_mov.gif" alt="stand wizard breathing">
                                <img id="wizard_stand_freeze" src="/static/VisualResources/Glacius/wizard_stand.png" alt="stand wizard">
                                <img id="ice_cube" src="/static/VisualResources/Glacius/ice_cube.png" alt="ice cube">
                                <audio id="actionSound" src="/static/VisualResources/Glacius/glacius.mp3"></audio>
                            </div>
                        `
                        break;
                    case 2:
                        containerAnimation.innerHTML = `
                            <div id="confringo">
                                <img id="fireballImg" src="/static/VisualResources/Confringo/Confringo.gif" alt="fireball">
                                <img id="wizard_stand" src="/static/VisualResources/Confringo/wizard_stand_mov.gif" alt="stand wizard">
                                <img id="burntPlayer" src="/static/VisualResources/Confringo/burnt_player.gif" alt="burnt player">
                                <img id="explosion" src="/static/VisualResources/Confringo/explosion.gif" alt="explosion">
                                <audio id="actionSound" src="/static/VisualResources/Confringo/confringo.mp3"></audio>
                            </div>
                        `;

                        break;
                    case 3:
                        containerAnimation.innerHTML = `
                            <div id="crucio">
                                <img id="crucioImg" src="/static/VisualResources/Crucio/crucio.gif" alt="crucioImg">
                                <img id="wizard_stand" src="/static/VisualResources/Crucio/wizard_stand_mov.gif" alt="stand wizard breathing">
                                <img id="heart_death" src="/static/VisualResources/Crucio/heart_death.gif" alt="heart death">
                                <audio id="actionSound" src="/static/VisualResources/Crucio/crucio.mp3"></audio>
                            </div>
                        `
                        break;
                    case 4:
                        containerAnimation.innerHTML = `
                            <div id="avadaKedabra">
                                <img id="avadaKedabraImg" src="/static/VisualResources/Avada_Kedavra/avada.gif" alt="avadaKedabraImg">
                                <img id="wizard_stand" src="/static/VisualResources/Avada_Kedavra/wizard_stand_mov.gif" alt="stand wizard breathing">
                                <img id="skull" src="/static/VisualResources/Avada_Kedavra/skull.gif" alt="skull">
                                <audio id="actionSound" src="/static/VisualResources/Avada_Kedavra/avada.mp3"></audio>
                            </div>
                        `
                        break
                    case 5:
                        containerAnimation.innerHTML = `
                            <div id="protego">
                                <img id="protegoImg" src="/static/VisualResources/Protego/protego.gif" alt="protegoImg">
                                <img id="wizard_spell" src="/static/VisualResources/Protego/wizard_defend.gif" alt="stand wizard spell">
                                <audio id="actionSound" src="/static/VisualResources/Protego/protego.mp3"></audio>
                            </div>
                        `
                        break
                    case 6:
                        containerAnimation.innerHTML = `
                            <div id="patronus">
                                <img id="wizard_spell" src="/static/VisualResources/Patronus/wizard_spell.gif" alt="stand wizard spell">
                                <img id="patronusImg" src="/static/VisualResources/Patronus/patronus.gif" alt="img patronus">
                                <img id="greenBall" src="/static/VisualResources/Patronus/green-ball.png" alt="green ball">
                                <audio id="actionSound" src="/static/VisualResources/Patronus/patronus.mp3"></audio>
                            </div>
                        `
                        break
                    case 7:
                        containerAnimation.innerHTML = `
                            <div id="aguamenti">
                                <img id="wizard_stand" src="/static/VisualResources/Aguamenti/wizard_spell.gif" alt="stand wizard breathing">
                                <img id="aguamentiImg" src="/static/VisualResources/Aguamenti/aguamenti.gif" alt="aguamentiImg">
                                <img id="exp" src="/static/VisualResources/Aguamenti/exp.gif" alt="expImg">
                                <audio id="actionSound" src="/static/VisualResources/Aguamenti/aguamenti.mp3"></audio>
                            </div>
                        `
                        break
                }

                let actionSound = document.getElementById('actionSound');
                actionSound.play();
                await new Promise (resolve => setTimeout(() => resolve(), 3500));

                modeAnimation.classList.add("hidden");
                containerAnimation.innerHTML = "";

                if (response.hasKilled) {
                    modeAnimation.classList.remove("hidden");
                    containerAnimation.innerHTML = `
                        <div id="death">
                            <img id="wizard_death" src="/static/VisualResources/Death/wizard_death.gif" alt="stand wizard death">
                            <img id="soul" src="/static/VisualResources/Death/soul.gif" alt="soul">
                            <audio id="actionSound" src="/static/VisualResources/Death/death.mp3"></audio>
                        </div>
                    `;
                    let actionSound = document.getElementById('actionSound');
                    actionSound.play();
                    await new Promise (resolve => setTimeout(() => resolve(), 3500));
                    modeAnimation.classList.add("hidden");
                    containerAnimation.innerHTML = "";
                }

                if (response.levelUp) {
                    modeAnimation.classList.remove("hidden");
                    containerAnimation.innerHTML = `
                        <div id="levelup">
                            <img id="wizard_gesture" src="/static/VisualResources/Level_Up/wizard_gesture.gif" alt="stand wizard gesture">
                            <img id="levelUpImg" src="/static/VisualResources/Level_Up/levelUp.png" alt="levelUpImg">
                            <audio id="actionSound" src="/static/VisualResources/Level_Up/levelUp.mp3"></audio>
                        </div>
                    `;
                    let actionSound = document.getElementById('actionSound');
                    actionSound.play();
                    await new Promise (resolve => setTimeout(() => resolve(), 3500));

                    modeAnimation.classList.add("hidden");
                    containerAnimation.innerHTML = "";
                }
            }



            this.resetParamters();
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
                else {
                    this.enableActionButton(button)
                }

            }
        },

        disableActionButton(button) {
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
        enableActionButton(button) {
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
                        if (minutesToReturn > 1) {
                            this.gameOptions.minutes = minutesToReturn + " minuts"
                        }
                        else {
                            this.gameOptions.minutes = minutesToReturn + " minut"
                        }
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


var app4 = createApp({
    el: "#app4",
    delimiters: ["[[", "]]"],
    data() {
        return {
            actions: [],
        };
    },
    mounted() {
        this.getActions();
    },
    methods: {
        getActions: async function () {
            await fetch("../api/get_actions")
                .then((response) => {
                    return response.json();
                })
                .then((response) => {
                    this.actions = response.actions;
                    console.log(this.actions);
                })
                .catch((error) => {
                    console.log("Could not get actions:", error);
                });
        },
    }

})

app4.mount("#app4");
