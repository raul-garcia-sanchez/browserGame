let user, actions, allUsers;

// OnInit
$(document).ready(async () => {
    actions = await getActions();
    user = await getCurrentUser();
    allUsers = await getAllUsers();
    disableOptionsOutOfMana(user, actions);
})

// OnChange in spell selector
$("select[name='spell']").change(() => {
    let idSpellSelected = $("select[name='spell']").val();
    let spellSelected = getActionById(idSpellSelected);

    if (spellSelected.action_type == 1) { // Offensive action
        fillSelectedActionProperties(spellSelected);
        showUsersField();
        disableSubmitButton();
    }
    else { // Other type of action
        hideUsersField();
        fillSelectedActionProperties(spellSelected);
        enableSubmitButton();
    }
})

// OnChange in user selector
$("select[name='user_receiver']").change(() => {
    let idUserSelected = $("select[name='user_receiver']").val();
    if (idUserSelected == "null") {
        disableSubmitButton()
    }
    else {
        enableSubmitButton()
    }
})

// OnClick in confirmAction
$("#btnConfirmAction").click(async () => {
    const idSpellSelected = $("select[name='spell']").val();
    const spellSelected = getActionById(idSpellSelected);
    var response, userTarget
    if (spellSelected.action_type == 1) { // Offensive action
        let idUserSelected = $("select[name='user_receiver']").val();
        userTarget = getUserById(idUserSelected)
        response = await makeAction(spellSelected.id, user.id, idUserSelected);
    }
    else { // Other type of action
        response = await makeAction(spellSelected.id, user.id);
    }
    await resetParameters()
    
    if (response && response.status_code == 200) {
        
        if (spellSelected.action_type == 1) {
            message = (response.action_succeed)  //If action succeeded
                ? `Has encertat l'atac <strong><i>${spellSelected.name}</i></strong> contra el jugador <strong>${userTarget.username}</strong><br>`
                : `Has fallat l'atac <strong><i>${spellSelected.name}</i></strong> contra el jugador <strong>${userTarget.username}</strong><br>`
        }
        else if (spellSelected.action_type == 2) {
            message = (response.action_succeed)  //If action succeeded
                ? `Has realitzat correctament <strong><i>${spellSelected.name}</i></strong> i t'has curat<br>`
                : `No has realitzat correctament <strong><i>${spellSelected.name}</i></strong><br>`
        }
        else if (spellSelected.action_type == 3) {
            message = (response.action_succeed)  //If action succeeded
                ? `Has realitzat correctament <strong><i>${spellSelected.name}</i></strong> i has guanyat punts d'experiència<br>`
                : `No has realitzat correctament <strong><i>${spellSelected.name}</i></strong><br>`
        }


        message += (response.has_killed)
            ? `Has matat al jugador <strong>${userTarget.username}</strong><br>`
            : ``

        message += (response.levelUp)
            ? `Has pujat de nivell a <strong>${user.level}</strong><br>`
            : ``

        if (response.action_succeed) NewError("success", message);
        else NewError("info", message);
    }
    else{
        message = "Error del servidor";
        NewError("error", message)

    }


})

// FUNCTIONS

function disableOptionsOutOfMana(user, actions) {
    mana = user.mana;
    actions.forEach(action => {
        if (action.cost > mana) {
            dif = action.cost - mana;
            $("select[name='spell'] option[value=" + action.id + "]").attr("disabled", true);
            if (dif > 1) {
                $("select[name='spell'] option[value=" + action.id + "]").text($("select[name='spell'] option[value=" + action.id + "]").text().split("(")[0] + "(et falten " + dif + " de manà)");
            }
            else {
                $("select[name='spell'] option[value=" + action.id + "]").text($("select[name='spell'] option[value=" + action.id + "]").text().split("(")[0] + "(et falta " + dif + " de manà)");
            }
        }
    });
}

async function resetParameters() {
    user = await getCurrentUser();
    allUsers = await getAllUsers();
    disableOptionsOutOfMana(user, actions);
    $("select[name='spell']").val("null");
    $("select[name='selectorUsers']").val("null");
    $("#actionProperties").empty();
    disableSubmitButton();
    hideUsersField();
    $("select[name='spell']").removeClass("defendSelect neutralSelect attackSelect")
}

// ALERTS
function NewError(tipoMensaje, Texto) {
    var error = $(`
    <div class="${tipoMensaje} text-center flex justify-between">
        <ul>
            <li> ${Texto}</li>
        </ul>
        <span class="closebtn self-center" onclick="this.parentElement.remove();">&times;</span>
    </div>`);
    $('#mensajes').append(error);
}

function getActionById(action_id) {
    actionSelected = actions.filter(action => action.id == action_id)[0]
    return actionSelected
}
function getUserById(user_id) {
    userSelected = allUsers.filter(user => user.id == user_id)[0]
    return userSelected
}

function enableSubmitButton() {
    $("#btnConfirmAction").attr("disabled", false)
}

function disableSubmitButton() {
    $("#btnConfirmAction").attr("disabled", true)
}

function showUsersField() {
    $("#selectorUsers").removeClass("hidden");
}

function hideUsersField() {
    $("select[name='user_receiver']").val("null");
    $("#selectorUsers").addClass("hidden");
}

function fillSelectedActionProperties(action) {
    $("#actionProperties").removeClass("hidden")
    $("#actionProperties").empty()
    switch (action.action_type) {
        // Ofensiva
        case 1:
            $("select[name='spell']").removeClass("defendSelect neutralSelect")
            $("select[name='spell']").addClass("attackSelect")


            $("#actionProperties").append(`
                        <hr class="border-black mb-3">
                        <h5 class="text-center text-gray-700 font-bold text-2xl">
                            <i class="fa fa-gavel mr-3 text-red-600"></i>
                            Acció ofensiva
                        </h5>

                        <div class="w-40 h-40 imageContainer m-auto"
                            style="background-image: url(/static/${action.action_img})">
                            &nbsp;
                        </div>

                        <ul>
                            <li> <strong>Encanteri:</strong> ${action.name}</li>
                            <li> <strong>Descripci\ó:</strong> ${action.description}</li>
                            <li> <strong>Cost:</strong> ${action.cost} de manà</li>
                            <li> <strong>Dany total:</strong> ${action.points}</li>
                            <li> <strong>Percentatge d'encert:</strong> ${action.success_rate}%</li>
                        </ul>
                        <hr class="border-black mt-3">

                    `)
            break;
        // Defensiva
        case 2:
            $("select[name='spell']").removeClass("attackSelect neutralSelect")
            $("select[name='spell']").addClass("defendSelect")

            $("#actionProperties").append(`
                        <hr class="border-black mb-3">
                        <h5 class="text-center text-gray-700 font-bold text-2xl">
                            <i class="fa-solid fa-shield mr-3 text-green-600"></i> 
                            Acció defensiva
                        </h5>

                        <div class="w-40 h-40 imageContainer m-auto"
                            style="background-image: url(/static/${action.action_img})">
                            &nbsp;
                        </div>
                        
                        <ul>
                            <li> <strong>Encanteri:</strong> <i>${action.name}</i></li>
                            <li> <strong>Descripci\ó:</strong> ${action.description}</li>
                            <li> <strong>Cost:</strong> ${action.cost} de manà</li>
                            <li> <strong>Curació total:</strong> ${action.points}</li>
                            <li> <strong>Percentatge d'encert:</strong> ${action.success_rate}%</li>
                        </ul>
                        <hr class="border-black mt-3">
                    `)
            break;
        // Neutral
        case 3:
            $("select[name='spell']").removeClass("defendSelect attackSelect")
            $("select[name='spell']").addClass("neutralSelect")

            $("#actionProperties").append(`
                        <hr class="border-black mb-3">
                        <h5 class="text-center text-gray-700 font-bold text-2xl">
                            <i class="fa fa-heartbeat  mr-3 text-blue-600"></i>
                            Acció neutral
                        </h5>
                        
                        <div class="w-40 h-40 imageContainer m-auto"
                            style="background-image: url(/static/${action.action_img})">
                            &nbsp;
                        </div>
                        
                        <ul>
                            <li> <strong>Encanteri:</strong> ${action.name}</li>
                            <li> <strong>Descripci\ó:</strong> ${action.description}</li>
                            <li> <strong>Cost:</strong> ${action.cost} de manà</li>
                            <li> <strong>Experi\ència a guanyar:</strong> ${action.exp_given}</li>
                            <li> <strong>Percentatge d'encert:</strong> ${action.success_rate}%</li>
                        </ul>
                        <hr class="border-black mt-3">
                    `)
            break;

    }



}