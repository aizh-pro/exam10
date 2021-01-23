async function makeRequest(url, method='GET') {
    let response = await fetch(url, {method});

    if (response.ok) {  // нормальный ответ
        return await response.text();
    } else {            // ошибка
        let error = new Error(response.statusText);
        error.response = response;
        throw error;
    }
}

async function onLike(event) {
    event.preventDefault();
    let likeBtn = event.target;
    let url = likeBtn.href;

    try {
        let response = await makeRequest(url);
        console.log(response);
        const counter = likeBtn.parentElement.getElementsByClassName('counter')[0];
        counter.innerText = response;
    }
    catch (error) {
        console.log(error);
    }

    likeBtn.classList.add('hidden');
    const unlikeBtn = likeBtn.parentElement.getElementsByClassName('unlike')[0];
    unlikeBtn.classList.remove('hidden');
}

async function onUnlike(event) {
    event.preventDefault();
    let unlikeBtn = event.target;
    let url = unlikeBtn.href;

    try {
        let response = await makeRequest(url);
        console.log(response);
        const counter = unlikeBtn.parentElement.getElementsByClassName('counter')[0];
        counter.innerText = response;
    }
    catch (error) {
        console.log(error);
    }

    unlikeBtn.classList.add('hidden');
    const likeBtn = unlikeBtn.parentElement.getElementsByClassName('like')[0];
    likeBtn.classList.remove('hidden');
}

window.addEventListener('load', function() {
    const likeButtons = document.getElementsByClassName('like');
    const unlikeButtons = document.getElementsByClassName('unlike');

    for (let btn of likeButtons) {btn.onclick = onLike}
    for (let btn of unlikeButtons) {btn.onclick = onUnlike}
});

$(document).ready(function() {
  $('#productos').on('change', function(e) {
     //Call the POST
     e.preventDefault();
     var csrftoken = getCookie('csrftoken');
     var value = $('#productos').val();

     $.ajax({
        url: window.location.href,
        type: "POST",
        data: {
            csrfmiddlewaretoken : csrftoken,
            value : value
        },
        success : function(json) {
            console.log(json);
            drop(json);
        },
        error : function(xhr,errmsg,err){
            console.log(xhr.status+": "+xhr.responseText)
        }
     });
  });
});