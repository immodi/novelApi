const form = document.querySelector("#form")
const button = document.querySelector("#submitButton")
const fileButtons = document.querySelectorAll("#fileButtons")
const progressBar = document.querySelector("#progressBar")

let startTime, endTime;
let imageSize = "";
let image = new Image();
let kboutput = document.getElementById("kbs");
let mboutput = document.getElementById("mbs");
let imageLink = "https://source.unsplash.com/random?topics=nature";
let fileId = ""


button.addEventListener("click", () => {
    button.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Loading...'
    button.disabled = true;
    form.submit()
})

fileButtons.forEach(element => {
    element.addEventListener('click', () => {
        init()
        fileId = element.classList[0]
    })
});

image.onload = async function () {
    endTime = new Date().getTime();
    await fetch(imageLink).then((response) => {
        imageSize = response.headers.get("content-length");
        let speedInMBps = calculateSpeed();
        let fileSizeString = document.querySelector(`#fileSize${fileId}`).innerHTML
        let fileSize = parseFloat(fileSizeString.substring(0, fileSizeString.length-2))
        startBar(fileSize, speedInMBps)
    });
};


function calculateSpeed() {
    let timeDuration = (endTime - startTime) / 1000;
    let loadedBits = imageSize * 8;
    let speedInBBs = (loadedBits / timeDuration).toFixed(2);
    let speedInKBps = (speedInBBs / 1024).toFixed(2);
    let speedInMBps = (speedInKBps / 1024).toFixed(2);
    let speed = parseFloat(speedInMBps) / 8
    return speed
}

const init = async () => {
    startTime = new Date().getTime();
    image.src = imageLink;
};

function startBar(fileSize, speedInMBps) {
    // 3MBps down&process speed in colab
    let originalSizeInMb = fileSize

    let interval = setInterval(() => {
        let percentage = (100 - parseFloat((fileSize / originalSizeInMb) * 100)) * 14
        progressBar.ariaValueNow = `${percentage}`
        progressBar.style.width = `${percentage}%`
        progressBar.innerHTML = `${percentage.toFixed(1)}%`
        fileSize -= speedInMBps
        if (fileSize <= 0 || percentage >= 100) {
            progressBar.innerHTML = '100%'
            clearInterval(interval)
        }
    }, 1000);
    // setTimeout(() => {intervalFunction(fileSize, speedInMBps)}, parseInt(fileSize / 3));
}