<template>
    <div class="dialog-wrapper" v-show="showDialog">
        <div class="dialog">
            <h2>{{ dialogTitle }}</h2>
            <form>
                <label for="userToAttack">Selecciona usuari a atacar</label>
                <select name="userToAttack" id="userToAttack">
                    <option value="null" selected> -- Selecciona objectiu -- </option>
                    <option v-for="user in users" v-bind:key="user.id">{{ user.username }}</option>
                </select>
            </form>
            <div class="dialog-buttons">
                <button @click="cerrarDialogo">Cancelar</button>
                <button @click="enviarFormulario">Enviar</button>
            </div>
        </div>
    </div>
</template>

<script>
import axios from 'axios'

export default {
    name: 'modalCreator',

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
        }
    },
    data() {
        return {
            showDialog: false
        }
    },
    methods: {
        logDeTest(){
            console.log('Funcionando')
        },
        abrirDialogo() {
            this.showDialog = true
        },
        cerrarDialogo() {
            this.showDialog = false
        },
        enviarFormulario() {
            axios.post('/api/make_action', this.formData)
                .then(response => {
                    console.log(response.data)
                    this.showDialog = false
                })
                .catch(error => {
                    console.log(error)
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
    max-width: 500px;
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

.dialog-buttons {
    display: flex;
    justify-content: flex-end;
}

.dialog-buttons button {
    margin-left: 10px;
    padding: 5px 10px;
    border-radius: 3px;
    border: none;
    color: white;
    font-weight: bold;
    cursor: pointer;
}

.dialog-buttons button:first-child {
    background-color: gray;
}

.dialog-buttons button:last-child {
    background-color: green;
}</style>