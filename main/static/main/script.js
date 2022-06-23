async function checkExistenceOfUsername(username) {
    const response = await fetch(`/api/users/${username}/exists`);
    if (response.status !== 200) {
        return Promise.reject(new Error("Internal Server Error"))
    }
    const data = await response.json();
    usernameExists = data.username_exists;
    return usernameExists;

}

function showWarning(id) {
    const warning = document.getElementById(id);
    warning.classList.remove("hidden");
}

function hideWarning(id) {
    const warning = document.getElementById(id);
    warning.classList.add("hidden");
}

async function handleUsernameFieldBlur(e) {
    const username = e.target.value;
    if (!username) hideWarning("username-existence-warning");
    else {
        const usernameExists = await checkExistenceOfUsername(username);
        if (usernameExists) showWarning("username-existence-warning");
        else hideWarning("username-existence-warning");
    }
}

function handlePasswordFieldBlur() {
    const password1 = document.querySelector("#signup-form input[name='password1']").value;
    const password2 = document.querySelector("#signup-form input[name='password2']").value;
    if (!password1 || !password2 || password1 === password2) hideWarning("passwords-dont-match-warning");
    else showWarning("passwords-dont-match-warning");
}

function handleSubmitForm(e) {
    const usernameWarning = document.getElementById("username-existence-warning");
    const passwordWarning = document.getElementById("passwords-dont-match-warning")
    if (!usernameWarning.classList.contains("hidden") || !passwordWarning.classList.contains("hidden")) {
        e.preventDefault();
    }
}


window.addEventListener("load", e => {
    const forms = ["signup", "add-username"].map(x => document.getElementById(`${x}-form`));
    const usernameFields = ["signup", "add-username"].map(x =>
        document.querySelector(`#${x}-form input[name='username']`));
    const passwordFields = [1, 2].map(x => document.querySelector(`#signup-form input[name='password${x}']`))
    
    for (const field of usernameFields) {
        if (!field) continue;
        field.addEventListener("blur", handleUsernameFieldBlur);
        field.addEventListener("input", () => hideWarning("username-existence-warning"));
    }

    for (const field of passwordFields) {
        if (!field) continue;
        field.addEventListener("blur", handlePasswordFieldBlur);
        field.addEventListener("input", () => hideWarning("passwords-dont-match-warning"));
    }

    for (const form of forms) {
        if (form) form.addEventListener("submit", handleSubmitForm);
    }
})