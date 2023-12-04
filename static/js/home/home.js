const form = document.querySelector("#form")
const button = document.querySelector("#submitButton")
const downloadForm = document.querySelectorAll("#downloadForm")
const downloadSubmit = document.querySelectorAll("#downloadSubmit")


button.addEventListener("click", () => {
    button.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Loading...'
    button.disabled = true;
    form.submit()
})

downloadSubmit.forEach(element => {
    element.addEventListener('click', (e) => {
        e.preventDefault()
        // let fileId = parseInt(element.classList[0])
        // let fileName = document.querySelector(`#fileName${fileId}`).innerHTML
        // let csrfToken = document.querySelector(`#downloadForm${fileId}`).children['csrfmiddlewaretoken'].value
        // download(fileName, fileId, csrfToken)
        element.parentNode.submit();
    })
});

function download(fileName, fileId, csrfToken) {
    // axios({url: '/download', //your url
}