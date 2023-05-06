async function getCurrentUser() {
    let currentUser
    await $.get("/api/get_user ", function (data) {
        currentUser = data.user;
    });
    return currentUser
}

async function getActions() {
    let allActions
    await $.get("/api/get_actions ", function (data) {
        allActions = data.actions;
    });
    return allActions
}