<template>
    <div class="dialog-wrapper" v-show="showDialog">
        <div class="dialog">
            <h2 class="text-center mb-3">
                {{ dialogTitle }}
            </h2>
            <div>
                <hr class="border-black mb-3">
                <h5 class="text-center text-gray-700 font-bold text-2xl">
                    <i class="fa fa-gavel mr-3 text-red-600"></i>
                    Acció ofensiva
                </h5>
                <div class="w-40 h-40 imageContainer m-auto"
                    v-bind:style="{ backgroundImage: 'url(/static/' + [[action.action_img]] + ') !important' }">
                    &nbsp;
                </div>
                <ul>
                    <li> <strong>Encanteri:</strong> {{ action.name }}</li>
                    <li> <strong>Descripció:</strong> {{ action.description }}</li>
                    <li> <strong>Cost:</strong> {{ action.cost }} de manà</li>
                    <li> <strong>Dany total:</strong> {{ action.points }}</li>
                    <li> <strong>Percentatge d'encert:</strong> {{ action.success_rate }}%</li>
                </ul>
                <hr class="border-black mt-3">
            </div>
            <form class="mt-3">
                <label class="text-center" for="userToAttack">Objectiu</label>
                <select @change="checkIfUserSelected()" name="userToAttack" :id="'userToAttack_' + action.id"
                    class="text-center text-lg italic w-full px-4 py-2 text-gray-700 
                bg-white border border-gray-400 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-red-100 focus:border-red-500">
                    <option value="null" selected disabled> -- Selecciona objectiu -- </option>
                    <option v-for="(user) in users" :key="user.id" v-bind:value="user.id">{{ user.username }}</option>
                </select>
            </form>
            <div class="dialog-buttons flex justify-around w-full">
                <button id="closeForm" @click="cerrarDialogo()">Cancelar</button>
                <button type="button" :id="'sendForm_' + action.id" @click="enviarFormulario()" disabled>Enviar</button>
            </div>
        </div>
    </div>
</template>

<script>
import axios from 'axios'
import Cookies from 'js-cookie'

export default {
    name: 'ModalCreator',
    mounted() {
        this.csrfToken = Cookies.get('csrftoken')
    },
    props: {
        action: {
            type: Object,
            required: true
        },
        users: {
            type: [Object],
            required: true
        },
        dialogTitle: {
            type: String,
            default: 'Formulario'
        },
        user_transmitter: {
            type: Object,
            required: true
        }
    },
    data() {
        return {
            showDialog: false
        }
    },
    methods: {
        checkIfUserSelected() {
            let selectuser = document.getElementById('userToAttack_' + this.action.id);
            let userSelected = selectuser.value;
            if (userSelected) {
                let buttonSubmit = document.getElementById("sendForm_" + this.action.id);
                buttonSubmit.disabled = false;
                buttonSubmit.style.cursor = "pointer";
                buttonSubmit.style.backgroundColor = "green";
            }
        },
        abrirDialogo() {
            this.showDialog = true
        },
        cerrarDialogo() {
            this.showDialog = false
            // this.updateData(false);
            this.$emit('modal-closed');

        },
        getUserById(id_user_receiver) {
            const user_receiver = this.users.find((user) => {
                return user.id == id_user_receiver;
            });
            return user_receiver
        },

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

        enviarFormulario() {
            let selectUser = document.getElementById('userToAttack_' + this.action.id);
            let userSelected = selectUser.value;
            let userTarget = this.getUserById(userSelected)
            var dataToSend = {
                action_id: this.action.id,
                id_user_transmitter: this.user_transmitter.id,
                id_user_receiver: userSelected
            };

            axios.post('/api/make_action', dataToSend, {
                headers: { 'X-CSRFToken': this.csrfToken },
            })
                .then(response => {
                    var message = "";
                    message = (response.data.action_succeed)  //If action succeeded
                            ? `Has encertat l'atac <strong><i>${this.action.name}</i></strong> contra el jugador <strong>${userTarget.username}</strong><br>`
                            : `Has fallat l'atac <strong><i>${this.action.name}</i></strong> contra el jugador <strong>${userTarget.username}</strong><br>`
                    
                    message += (response.data.has_killed)
                        ? `Has matat al jugador <strong>${userTarget.username}</strong><br>`
                        : ``

                    message += (response.data.levelUp)
                        ? `Has pujat de nivell a <strong>${this.user_transmitter.level}</strong><br>`
                        : ``

                    if (response.data.action_succeed) this.newError("success", message);
                    else this.newError("info", message);

                    this.cerrarDialogo()
                })
                .catch(error => {
                    console.log(error)
                    let message = "Error del servidor";
                    this.newError("error", message)
                })
        }
    }
}
</script>
  

<style>
.dialog-wrapper {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.5);
    z-index: 999;
    display: flex;
    justify-content: center;
    align-items: center;
}

.dialog {
    background-color: white;
    padding: 20px;
    max-width: 50%;
    width: 100%;
    max-height: 80%;
    overflow-y: auto;
    border-radius: 5px;
}

.dialog h2 {
    margin-top: 0;
    font-size: 1.5rem;
}

.dialog form {
    display: flex;
    flex-direction: column;
    margin-bottom: 20px;
}

.dialog label {
    margin-bottom: 5px;
    font-weight: bold;
}

.dialog input {
    padding: 5px;
    margin-bottom: 10px;
    border-radius: 3px;
    border: 1px solid gray;
}

.dialog-buttons button {
    margin-left: 10px;
    padding: 5px 10px;
    border-radius: 3px;
    border: none;
    color: white;
    font-weight: bold;
}

.dialog-buttons button:first-child {
    background-color: gray;
    cursor: pointer;

}

.dialog-buttons button:last-child {
    background-color: rgb(63, 92, 63);
    /* background-color: green; */
}
</style>