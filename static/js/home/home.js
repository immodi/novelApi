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
        let fileId = parseInt(element.classList[0])
        let fileName = document.querySelector(`#fileName${fileId}`).innerHTML
        requestFile(fileId, fileName)
    })
});

async function requestFile(fileId, fileName) {
    var formData = new FormData();
    formData.append('file_id', fileId);
    const res = await axios({
        method: 'POST',
        url: '/download',
        data: formData
    }).then((response) => {
        // console.log(response.data)
        if (response.data["done"]) {
            download(fileId, fileName)
        }
    })   
}

function download(fileId, fileName) {
    let a = document.createElement('a'); 
    a.classList.add("d-none")
    a.href = `/download?file_id=${fileId}`; 
    a.download = fileName; 
    document.body.prepend(a); 
    a.click()
}