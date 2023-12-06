const form = document.querySelector("#form")
const button = document.querySelector("#submitButton")
const fileButton = document.querySelectorAll("#fileButton")
// const requestFile = document.querySelectorAll("#requestFile")


button.addEventListener("click", () => {
    button.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Loading...'
    button.disabled = true;
    form.submit()
})

fileButton.forEach(element => {
    element.addEventListener('click', (e) => {
        e.preventDefault()
        let fileId = parseInt(element.classList[0])
        let fileName = document.querySelector(`#fileName${fileId}`).innerHTML
        console.log(fileName);
        let fileUrl = `/download?file_id=${fileId}`
        saveAs(fileUrl, fileName);
    })
})

