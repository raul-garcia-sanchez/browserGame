async function getCurrentUser() {
    let currentUser
    await $.get("/api/get_user", function (data) {
        currentUser = data.user;
    });
    return currentUser
}

async function getAllUsers(){
    let allUsers
    await $.get("/api/get_ranking", function (data) {
        allUsers = data.ranking;
    });
    return allUsers
}

async function getActions() {
    let allActions
    await $.get("/api/get_actions", function (data) {
        allActions = data.actions;
    });
    return allActions
}

async function makeAction(action_id, id_user_transmitter, id_user_receiver = null) {
    
    id_user_receiver ||= id_user_transmitter;
    // Creamos un objeto con los datos a enviar
    var dataToSend = {
        action_id: action_id,
        id_user_transmitter: id_user_transmitter,
        id_user_receiver: id_user_receiver
    };
    var csrftoken = $.cookie("csrftoken");
    // Realizamos la llamada a la API
    return $.ajax({
        url: '/api/make_action',
        type: 'POST',
        headers: {'X-CSRFToken': csrftoken},
        contentType: 'application/json', // Especificamos el tipo de contenido
        data: JSON.stringify(dataToSend),
        success: function (response) {
            // Manejamos la respuesta de la API aquí
            return response
        },
        error: function (xhr, status, error) {
            // Manejamos los errores de la llamada aquí
            return false
        }
    });
}