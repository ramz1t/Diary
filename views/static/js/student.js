function loadDiary(day) {
    if (day === 'load') {
        let objToday = new Date();
        if (objToday.getDay() === 0 || objToday.getDay() === 6) {
            changeDates('next');
            day = 'mon';
        } else {
            let weekday = ['', 'mon', 'tue', 'wed', 'thu', 'fri', ''];
	        day = weekday[objToday.getDay()];
        }
    }
    const date = document.getElementById(day).dataset.date;
    callServer(`/load_diary?date=${date}`).then(async (response) => {
        const diary_data = await response.json();
        let diary = document.getElementById('diary-wrapper');
        diary.innerHTML = `<h3>${diary_data['title']}</h3>`;
        if (!diary_data.has_classes) {
            diary.innerHTML += 'No classes today!';
            return;
        }
        let inner = '';
        diary_data['classes'].forEach((el) => {
            inner = `
            <div class="flex-row space-between justify-center diary-class p-10 border-radius white">
                <div class="flex-row">
                    <h3 class="p-5 lesson-n">${el.number}</h3>
                    <div class="splitter"></div>
                    <div class="lesson-info">
                        <h6>${el.subject}</h6>
                        <p class="initials grey">${el.teacher}</p>
                    </div>
                    <div class="splitter"></div>
                    <p id="hw" class="p-10" onclick="comment('Homework was added on ${el.hw['made']}')">
                    ${el.hw['body'] !== null ? el.hw['body'] : ''}
                    </p>
                </div>
                <div class="flex-row">
                    ${el.hw['exec_time'] === null ? '' : `
                    <div class="flex-row round-border p-5 allign-center" style="gap: 0.2rem; margin-right: 15px;">
                        <i class="bi bi-clock"></i>
                        <p>${el.hw['exec_time']}</p>
                        <p>min.</p>
                    </div>`}
                    <div class="flex-row">
                        <div class="splitter"></div>
                        <h3 onclick="comment('Mark was added on ${el.mark_time}')" id="mark" class="p-5 mark pointer">${el.mark}</h3>
                    </div>
                </div>
            </div>`;
            diary.innerHTML += inner;
            inner = '';
        });
    })
}

async function changeDates(type) {
    const firstDate = document.getElementById('mon').dataset.date;
    callServer(`/get_dates_for_next_week?date=${firstDate}&type=${type}`).then(async (response) => {
        const data = await response.json()
        for (let i = 0; i < 5; i++) {
            let day = document.getElementById(data[i].name);
            day.innerText = `${data[i].day} ${data[i].name.replace(/^\w/, (c) => c.toUpperCase())}`;
            day.setAttribute('data-date', data[i].date);
        }
    }).then(() => {
        loadDiary('mon');
    });
}


async function setPermissions() {
    const hw = document.getElementById('hw-check').checked;
    const mark = document.getElementById('mark-check').checked;
    callServer(`/edit_tg_permissions?hw=${hw}&mark=${mark}`, {}, 'POST').then(async (response) => {
        if (response.ok) {
            Swal.fire({
                icon: 'success',
                text: 'Saved!',
                position: 'top',
                timer: 3000
            });
        }
        await alertError(response);
        checkCredentials(response.status);
    })
}

function comment(text){
    Swal.fire({
        text: text,
        position: 'top',
        confirmButtonColor: '#004d00',
        title: 'Information'
    })
}