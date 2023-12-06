const form = document.querySelector("#form")
const button = document.querySelector("#submitButton")


button.addEventListener("click", () => {
    button.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Loading...'
    button.disabled = true;
    form.submit()
})
