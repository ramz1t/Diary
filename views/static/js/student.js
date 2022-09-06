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
        for (let i = 0; i < diary_data.classes.length; i++) {
            inner = `
            <div class="flex-row space-between justify-center diary-class p-10 border-radius white">
                <div class="flex-row">
                    <h3 class="p-5 lesson-n">${diary_data['classes'][i].number}</h3>
                    <div class="splitter"></div>
                    <div class="lesson-info">
                        <h6>${diary_data['classes'][i].subject}</h6>
                        <p class="initials grey">${diary_data['classes'][i].teacher}</p>
                    </div>
                    <div class="splitter"></div>
                    <p id="hw" class="p-10">${diary_data['classes'][i].hw}</p>
                </div>
                <div class="flex-row">
                    <div class="splitter"></div>
                    <h3 onclick="alert('Mark was added on ${diary_data.classes[i].mark_time}')" id="mark" class="p-5 mark pointer">${diary_data['classes'][i].mark}</h3>
                </div>
            </div>`;
            diary.innerHTML += inner;
            inner = '';
        }
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