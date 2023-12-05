const form = document.querySelector("#form")
const button = document.querySelector("#submitButton")
const requestFile = document.querySelectorAll("#requestFile")


button.addEventListener("click", () => {
    button.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Loading...'
    button.disabled = true;
    form.submit()
})

requestFile.forEach(element => {
    element.addEventListener('click', () => {
        let fileId = parseInt(element.classList[2])
        location.replace(`/download?file_id=${fileId}`)
    })
});
