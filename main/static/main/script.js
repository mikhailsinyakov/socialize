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
    const signupForm = document.getElementById("signup-form");
    const usernameField = document.querySelector("#signup-form input[name='username']");
    const password1Field = document.querySelector("#signup-form input[name='password1']");
    const password2Field = document.querySelector("#signup-form input[name='password2']");

    usernameField.addEventListener("blur", handleUsernameFieldBlur);
    usernameField.addEventListener("input", () => hideWarning("username-existence-warning"));

    password1Field.addEventListener("blur", handlePasswordFieldBlur);
    password1Field.addEventListener("input", () => hideWarning("passwords-dont-match-warning"));

    password2Field.addEventListener("blur", handlePasswordFieldBlur);
    password2Field.addEventListener("input", () => hideWarning("passwords-dont-match-warning"));


    signupForm.addEventListener("submit", handleSubmitForm);
});