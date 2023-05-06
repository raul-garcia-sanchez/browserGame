        let user, actions;


        $(document).ready(async () => {
            user = await getCurrentUser();
            actions = await getActions();
            disableOptionsOutOfMana(user, actions);

            // Onchange in spell selector
            $("select[name='spell']").change(() => {
                let idSpellSelected = $("select[name='spell']").val();
                let spellSelected = getActionSelectedById(idSpellSelected);

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

            $("select[name='user_receiver']").change(() => {
                let idUserSelected = $("select[name='user_receiver']").val();
                if (idUserSelected == "null") {
                    disableSubmitButton()
                }
                else {
                    enableSubmitButton()
                }
            })
        })



        // Functions
        function disableOptionsOutOfMana(user, actions) {
            mana = user.mana;
            actions.forEach(action => {
                if (action.cost > mana) {
                    dif = action.cost - mana;
                    $("select[name='spell'] option[value=" + action.id + "]").attr("disabled", true);
                    if (dif > 1) {
                        $("select[name='spell'] option[value=" + action.id + "]").text($("select[name='spell'] option[value=" + action.id + "]").text() + "(et falten " + dif + " de manà)");
                    }
                    else {
                        $("select[name='spell'] option[value=" + action.id + "]").text($("select[name='spell'] option[value=" + action.id + "]").text() + "(et falta " + dif + " de manà)");
                    }
                }
            });
        }

        function getActionSelectedById(action_id) {
            actionSelected = actions.filter(action => action.id == action_id)[0]
            return actionSelected
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
            console.log($("#selectorUsers").val());
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
                        <ul>
                            <li> <strong>Encanteri:</strong> ${action.name}</li>
                            <li> <strong>Descripci\ó:</strong> ${action.description}</li>
                            <li> <strong>Cost:</strong> ${action.cost} de manà</li>
                            <li> <strong>Dany total:</strong> ${action.points}</li>
                            <li> <strong>Percentatge d'acert:</strong> ${action.success_rate}%</li>
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
                        <ul>
                            <li> <strong>Encanteri:</strong> <i>${action.name}</i></li>
                            <li> <strong>Descripci\ó:</strong> ${action.description}</li>
                            <li> <strong>Cost:</strong> ${action.cost} de manà</li>
                            <li> <strong>Curació total:</strong> ${action.points}</li>
                            <li> <strong>Percentatge d'acert:</strong> ${action.success_rate}%</li>
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
                        <ul>
                            <li> <strong>Encanteri:</strong> ${action.name}</li>
                            <li> <strong>Descripci\ó:</strong> ${action.description}</li>
                            <li> <strong>Cost:</strong> ${action.cost} de manà</li>
                            <li> <strong>Experi\ència a guanyar:</strong> ${action.exp_given}</li>
                            <li> <strong>Percentatge d'acert:</strong> ${action.success_rate}%</li>
                        </ul>
                        <hr class="border-black mt-3">
                    `)
                    break;

            }



        }