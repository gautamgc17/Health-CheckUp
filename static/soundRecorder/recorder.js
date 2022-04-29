const startButton = document.getElementById('startButton');
const pauseButton = document.getElementById('pauseButton');
const stopButton = document.getElementById('stopButton');
const sendButton = document.getElementById('sendButton');
const listenButton = document.getElementById('listenButton');
const body = document.getElementById('body');
const audio = document.getElementById('audi');
const symptoms = document.getElementById('symptoms');
const addSymptoms = document.getElementById('addSymptoms');
const statusShow = document.getElementById('statusShow');
const sendSymptoms = document.getElementById('sendSymptoms');
const textSymptomModal = document.getElementById('exampleModal');
const pseudoSend = document.getElementById('pseudoSend');
const accordionId = document.getElementById('accordionExample');
const advice = document.getElementById('advice');

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

pseudoSend.classList.add('disabled');
textSymptomModal.addEventListener('show.bs.modal', function () {
    sendSymptoms.classList.add('disabled');
})
document.getElementById('SymptomInput').addEventListener('change', (event) => {
    console.log('inputinside');
    console.log(event.target.value)
    if (event.target.value.trim() == '') {
        console.log('inside if');
        sendSymptoms.classList.add('disabled');
    }
    else {
        console.log('inside else')
        sendSymptoms.classList.remove('disabled');
    }
})

sendSymptoms.addEventListener('click', () => {
    const symptomsInput = document.querySelectorAll('.symptoms>input');
    let symptomsToServer = new FormData();
    symptomsInput.forEach((symptom, index) => {
        if (symptom.value.trim() !== '') {
            symptomsToServer.append(`symptoms${index}`, symptom.value);
        }
    })
    symptomsToServer.append('days', document.getElementById('SymptomInput').value);
    axios.post('', symptomsToServer, {
        headers: {
            "Content-Type": 'multipart/form-data',
            "X-CSRFToken": getCookie("csrftoken"),
        },
    })
        .then((response) => {
            accordionId.parentElement.style.display = 'block';
            advice.textContent = advice.textContent + response.data.advice;
            const output = response.data.output;
            console.log(output)
            for (dis in output) {
                const retElement = accordionMaker(dis, output[dis].desc, output[dis].prec)
                document.getElementById("accordionExample").appendChild(retElement);
            }
        })
        .then((error) => {
            console.log(error);
        })

})
let count = 1;
function deleteSymptom(number) {
    toDelete = document.getElementById(`inputGroup-sizing-default${number}`);
    toDelete.parentElement.remove();

}
function makeSymptom() {
    let element = `
    <span class="input-group-text" id="inputGroup-sizing-default${count}"
      >Symptoms</span
    >
    <input
      type="text"
      class="form-control"
      aria-label="Sizing example input"
      aria-describedby="inputGroup-sizing-default${count}"
    /><span class="input-group-text" id="inputGroup-sizing-defaultCancel${count}" onClick=deleteSymptom(${count})
    ><i class="fas fa-times"></i></span
    >
    `
    const element1 = document.createElement('div');
    element1.classList.add('input-group');
    element1.classList.add('my-3');
    element1.classList.add('symptoms');
    element1.innerHTML = element;
    return element1;


}

let userStream;
let recordedChunks = [];
let mediaRecorder;
addSymptoms.addEventListener('click', () => {
    startButton.classList.add('disabled');
    pseudoSend.classList.remove('disabled');
    const newelement = makeSymptom();
    symptoms.appendChild(newelement);

    count++;
})
window.onload = function () {
    navigator.mediaDevices
        .getUserMedia({ audio: true, video: false })
        .then(handleSuccess);


};

sendButton.addEventListener('click', () => {
    let audioToServer = new FormData();
    const audioData = new Blob(recordedChunks, { type: 'audio/webm;' });
    console.log(audioData);
    audioToServer.append('audio', audioData);
    audioToServer.append('days', document.getElementById('SymptomAudio1').value);
    axios.post('', audioToServer, {
        headers: {
            "Content-Type": 'multipart/form-data',
            "X-CSRFToken": getCookie("csrftoken"),
        },
    })
        .then((response) => {
            accordionId.parentElement.style.display = 'block';
            advice.textContent = advice.textContent + response.data.advice;
            const output = response.data.output;
            for (dis in output) {
                const retElement = accordionMaker(dis, output[dis].desc, output[dis].prec)
                document.getElementById("accordionExample").appendChild(retElement);
            }
        })
        .then((error) => {
            console.log(error);
        })

})
startButton.addEventListener('click', () => {
    audio.pause();
    addSymptoms.classList.add('disabled');
    console.log('paused');
    sendSymptoms.classList.add('disabled');
    audio.parentElement.parentElement.style.display = 'none';
    statusShow.textContent = 'RecordAudio';
    audio.parentElement.parentElement.nextElementSibling.style.display = 'none';
    audio.parentElement.parentElement.nextElementSibling.nextElementSibling.style.display = 'none';
    audio.parentElement.parentElement.nextElementSibling.nextElementSibling.nextElementSibling.style.display = 'display'
    recordedChunks = [];
    statusShow.textContent = 'Recording';
    pauseButton.classList.remove('disabled');
    stopButton.classList.remove('disabled');
    startButton.classList.add('disabled');
    mediaRecorder.start();
})
pauseButton.addEventListener('click', () => {
    if (pauseButton.textContent.trim() === 'Pause') {
        console.log(recordedChunks);
        mediaRecorder.pause();
        pauseButton.textContent = 'Resume';
        statusShow.textContent = 'Recording Paused';
    }
    else {
        console.log(recordedChunks);
        mediaRecorder.resume();
        pauseButton.textContent = 'Pause';
        statusShow.textContent = 'Recording Resumed';
    }
})
document.getElementById('SymptomAudio1').addEventListener('change', (event) => {
    if (event.target.value.trim() == '') {
        console.log('inside if');
        sendButton.classList.add('disabled');
    }
    else {
        console.log('inside else')
        sendButton.classList.remove('disabled');
    }
})
listenButton.addEventListener('click', () => {
    // sendButton.classList.remove('disabled');
    listenButton.classList.add('disabled');
    audio.src = URL.createObjectURL(new Blob(recordedChunks));
    audio.parentElement.parentElement.style.display = 'block';
    statusShow.textContent = 'RecordAudio';
    audio.parentElement.parentElement.nextElementSibling.style.display = 'block';
    audio.parentElement.parentElement.nextElementSibling.nextElementSibling.style.display = 'block';
    audio.parentElement.parentElement.nextElementSibling.nextElementSibling.nextElementSibling.style.display = 'none';




});
stopButton.addEventListener("click", function () {
    statusShow.textContent = 'Recording Stopped';
    startButton.classList.remove('disabled');
    pauseButton.classList.add('disabled');
    listenButton.classList.remove('disabled');
    stopButton.classList.add('disabled');
    console.log(recordedChunks);
    mediaRecorder.stop();
    console.log(recordedChunks);

});
// body.addEventListener('load', () => {
//     navigator.mediaDevices
//         .getUserMedia({ audio: true, video: false })
//         .then(handleSuccess);

// })

const handleSuccess = function (stream) {
    console.log('add');
    const options = { mimeType: "audio/webm" };
    recordedChunks = [];
    mediaRecorder = new MediaRecorder(stream, options);

    mediaRecorder.addEventListener("dataavailable", function (e) {
        console.log("hello");
        if (e.data.size > 0) recordedChunks.push(e.data);
    });
    startButton.classList.remove('disabled');
};


function accordionMaker(diseasename, diseasedesc, precArray) {
    const listParent = document.createElement('ul');
    listParent.classList.add('list-group', 'list-group-flush');
    precArray.forEach(list => {
        let listTag = document.createElement('li');
        listTag.classList.add('list-group-item');
        listTag.textContent = list;
        listParent.append(listTag);
    });
    const accordionParent = document.createElement('div');
    accordionParent.classList.add('accordian-item');

    let accordionItem = `
<h2 class="accordion-header" id="heading${diseasename.split(" ").join('').split("(").join('').split(")").join('')}">
  <button
    class="accordion-button"
    type="button"
    data-bs-toggle="collapse"
    data-bs-target="#collapse${diseasename.split(" ").join('').split("(").join('').split(")").join('')}"
    aria-expanded="true"
    aria-controls="collapse${diseasename.split(" ").join('').split("(").join('').split(")").join('')}"
  >
    ${diseasename}
  </button>
</h2>
<div
  id="collapse${diseasename.split(" ").join('').split("(").join('').split(")").join('')}"
  class="accordion-collapse collapse"
  aria-labelledby="heading${diseasename.split(" ").join('').split("(").join('').split(")").join('')}"
  data-bs-parent="#accordionExample"
>
  <div class="accordion-body">
    <div class="row">
      <div class="col-md-6">
        <div class="card">
          <h5 class="card-header">Disease Description</h5>
          <div class="card-body">
            <p class="card-text">${diseasedesc}</p>
          </div>
        </div>
      </div>
      <div class="col-md-6">
        <div class="card">
          <h5 class="card-header">Disease Precautions</h5>
          <div class="card-body">
            <ul class="list-group list-group-flush">
              ${listParent.innerHTML}
            </ul>
          </div>
        </div>
      </div>
    </div>
  </div>
</div>`
    accordionParent.innerHTML = accordionItem;
    return accordionParent;

}