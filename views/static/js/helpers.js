async function callServer(url, data, method) {
    return await fetch(url, {
        method: method,
        headers: {
            'accept': 'application/json',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    });
}

function executeScripts(page) {
    if (page === 'manage_groups') {
        loadSchedule('load', '0');
    } else if (page === 'my_diary') {
        loadDiary('load');
    } else if (page === 'group_book') {
        openClassBook('load')
    } else if (page === 'teacher_homework') {
        load_hw('load')
    }
}

function writeStorage(data) {
    for (let i = 0; i < data.length; i++) {
        localStorage.setItem(data[i][0], data[i][1]);
    }
}

function logout() {
    const type = localStorage.getItem('type');
    document.cookie = "access_token=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;";
    localStorage.clear();
    localStorage.setItem('type', type);
    window.open(`/${type}/login`, '_self');
}

function checkCredentials(status) {
    const timeout = 2000;
    if (status === 401) {
        Swal.fire({
            text: 'Your session has expired, please log in again',
            timer: timeout
        });
        setTimeout(logout, timeout)
        throw 'credentials error 401'
    }

}


function markComment(mark){
    mark = mark.replaceAll("'", '"')
    mark = JSON.parse(mark)
    Swal.fire({
        text: `Time: ${mark['time']}\n Class date: ${mark['date']}\n Comment: ${mark['comment']}`,
        position: 'top',
        confirmButtonColor: '#004d00',
        title: 'Information'
    })
}


function hmComment(hw_single){
    hw_single = hw_single.replaceAll("'", '"')
    hw_single = JSON.parse(hw_single)
    Swal.fire({
        text: hw_single['time'],
        position: 'top',
        confirmButtonColor: '#004d00',
        title: 'Information'
    })
}



async function changePassword() {
    var type = $.cookie("type");
    var new_pass = document.getElementById("New_pass").value;
    var old_pass = document.getElementById("Old_pass").value;
    var repeat_new_pass = document.getElementById("Repeat_new_pass").value;
    if (new_pass !== repeat_new_pass) {
        document.getElementById("New_pass").classList.add('is-invalid');
        document.getElementById("Repeat_new_pass").classList.add('is-invalid');
        return;
    }
    var response = await fetch('/change_user_password', {
        method: 'POST',
        headers: {
            'accept': 'application/json',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            'new_password': new_pass,
            'old_password': old_pass,
            'type': type
        })
    });
    var text = await response.json();
    alert(text);
}

async function changeEmail() {
    var type = $.cookie("type");
    var new_email = document.getElementById('New_email').value;
    var old_email = document.getElementById('Old_email').value;
    var response = await fetch('/change_user_email', {
        method: 'POST',
        headers: {
            'accept': 'application/json',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            'type': type,
            'new_email': new_email,
            'old_email': old_email
        })

    });
    var text = await response.json();
    alert(text);
}

async function loadPage(type, page) {
    const params = new Proxy(new URLSearchParams(window.location.search), {
        get: (searchParams, prop) => searchParams.get(prop),
    });
    let user_id = localStorage.getItem('user_id');
    if (page === 'load') {
        page = params.page;
    } else {
        var searchParams = new URLSearchParams(window.location.search)
        searchParams.set("page", page);
        var newRelativePathQuery = window.location.pathname + '?' + searchParams.toString();
        history.pushState(null, '', newRelativePathQuery);
    }
    if (page !== null) {
        const wrapper = document.getElementById('wrapper');
        wrapper.innerHTML = `<div class="content-wrapper"><div class="flex-row"><h1>Loading...</h1>
                            <div class="spinner-border text-primary" style="color: var(--diary-color)" role="status">
                                <span class="visually-hidden">Loading...</span></div>
                            </div>
                            </div>
                            `;
        let data = {
            'user_id': user_id
        };
        let response = await callServer(`/load_page/?page=${page}&type=${type}`, data, 'PATCH');
        if (response.ok) {
            wrapper.innerHTML = '';
            response = await response.text();
            wrapper.innerHTML = '';
            wrapper.innerHTML = response;
        } else {
            checkCredentials(response.status)
        }
        executeScripts(page);
    }
}

function deleteFromDB(id, model) {
    const swalWithBootstrapButtons = Swal.mixin({
        customClass: {
            confirmButton: 'btn btn-success',
            cancelButton: 'btn btn-danger'
        },
        buttonsStyling: false
    })
    swalWithBootstrapButtons.fire({
        title: 'Are you sure?',
        text: "You won't be able to revert this!",
        icon: 'warning',
        showCancelButton: true,
        confirmButtonText: 'Yes, delete',
        padding: '0 0 1.25em',
        cancelButtonText: 'No, cancel',
        reverseButtons: true
    }).then((result) => {
        if (result.isConfirmed){
            callServer(`/${model}/delete?id=${id}`, {}, 'POST').then(async (response) => {
                checkCredentials(response.status);
                await alertError(response);
                window.location.reload(true)
    })
        }
        else {
            swalWithBootstrapButtons.fire(
                'Cancelled',
                'Data is safe :)',
                'error'
            )
        }
    })

}

function hideShow() {
    var input_fields = $('.pass_input');
    var eyes = $('.eye-btn');
    if(input_fields[0].type === 'password') {
        for (let i = 0; i < input_fields.length; i++) {
            input_fields[i].type = 'text';
            eyes[i].classList.replace('bi-eye-slash', 'bi-eye');
        }
    }
    else{
        for (let i = 0; i < input_fields.length; i++) {
            input_fields[i].type = 'password';
            eyes[i].classList.replace('bi-eye', 'bi-eye-slash');
        }
    }
}