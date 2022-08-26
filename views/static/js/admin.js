async function addGroup() {
    let user_id = localStorage.getItem('user_id');
    let groupName = document.getElementById("groupname").value;
    let data = {
        'name': groupName,
        'user_id': user_id
    }
    let response = await callServer('/execute/group/create', data, 'POST');
    if (response.ok) {
        document.location.reload(true);
    } else {
        checkCredentials(response.status);
        await alertError(response);
    }
}

async function addStudentKey() {
    let user_id = localStorage.getItem('user_id');
    let name = document.getElementById('name').value.trim();
    let surname = document.getElementById('surname').value.trim();
    if (document.querySelector('input[name="group"]:checked') == null) {
        return;
    }
    let group = document.querySelector('input[name="group"]:checked').value;
    let data = {
        'name': name,
        'surname': surname,
        'group': group,
        'user_id': user_id
    }
    let response = await callServer('/execute/studentkey/add_key', data, 'POST');
    if (response.ok) {
        document.location.reload(true);
    } else {
        checkCredentials(response.status);
        await alertError(response);
    }
}

async function addTeacherKey() {
    let user_id = localStorage.getItem('user_id');
    let name = document.getElementById('name').value.trim();
    let surname = document.getElementById('surname').value.trim();
    let data = {
        'user_id': user_id,
        'name': name,
        'surname': surname,
    };
    let response = await callServer('/execute/teacherkey/add_key', data, 'POST')
    if (response.ok) {
        document.location.reload(true);
    } else {
        checkCredentials(response.status);
        await alertError(response);
    }
}

function downloadGroup(group) {
    window.open(`/download_group/${group}`, '_blank')
}

async function downloadTeachers() {
    window.open('/download_teachers', '_blank')
}

async function addSubject() {
    let user_id = localStorage.getItem('user_id');
    let subject = document.getElementById('subject').value;
    if (document.querySelector('input[name="type"]:checked') == null) {
        return;
    }
    let lesson_type = document.querySelector('input[name="type"]:checked').value;
    let data = {
        'user_id': user_id,
        'name': subject,
        'type': lesson_type
    };
    let response = await callServer('/execute/subject/create', data, 'POST');
    if (response.ok) {
        document.location.reload(true);
    } else {
        checkCredentials(response.status);
        await alertError(response);
    }
}

async function addSchool() {
    let city = document.getElementById('city').value;
    let data = {
        'city': city
    };
    let response = await callServer('/execute/school/create', data, 'POST');
    if (response.ok) {
        document.location.reload(true);
    } else {
        checkCredentials(response.status);
        await alertError(response);
    }
}

function setValue(type, value, id) {
    document.getElementById(type).innerHTML = value;
    document.getElementById(type + '_id').innerText = id;
}

function turnGreen(day_i, lesson_i) {
    document.getElementById(`btn-${day_i}-${lesson_i}`).classList.remove('unsaved');
    document.getElementById(`icon-${day_i}-${lesson_i}`).classList.remove('bi-cloud-minus');
    document.getElementById(`icon-${day_i}-${lesson_i}`).classList.add('bi-cloud-check');
}

function turnRed(day_i, lesson_i) {
    document.getElementById(`btn-${day_i}-${lesson_i}`).classList.add('unsaved');
    document.getElementById(`icon-${day_i}-${lesson_i}`).classList.add('bi-cloud-minus');
    document.getElementById(`icon-${day_i}-${lesson_i}`).classList.remove('bi-cloud-check');
}

function checkSave(day_i, lesson_i) {
    let local_class_id = document.getElementById(`lesson-${day_i}-${lesson_i}_id`).innerText;
    let db_class_id = document.getElementById(`lesson-${day_i}-${lesson_i}_db_id`).innerText;
    if (local_class_id !== db_class_id) {
        turnRed(day_i, lesson_i)
    } else {
        turnGreen(day_i, lesson_i)
    }
}

async function addClass() {
    let user_id = localStorage.getItem('user_id');
    let group = document.getElementById('group').innerText.trim();
    let subject = document.getElementById('subject').innerText.trim();
    let teacher = document.getElementById('teacher').innerText.trim();
    if (group === 'Choose group' || subject === 'Choose subject' || teacher === 'Choose teacher') {
        Swal.fire({
            icon: 'question',
            title: 'Sorry',
            text: 'not enough info'
        })
        return;
    }
    let data = {
        'group_id': document.getElementById('group_id').innerText,
        'subject_id': document.getElementById('subject_id').innerText,
        'teacher_id': document.getElementById('teacher_id').innerText,
        'user_id': user_id
    };
    let response = await callServer('/execute/cls/create', data, 'POST');
    if (response.ok) {
        document.location.reload(true);
    } else {
        checkCredentials(response.status);
        await alertError(response);
    }
}

function showDropdown() {
    document.getElementById("class-dropdown").classList.toggle("show");
}

window.onclick = function (event) {
    if (!event.target.matches('.dropbtn')) {
        let dropdowns = document.getElementsByClassName("class-dropdown-content");
        for (let i = 0; i < dropdowns.length; i++) {
            let openDropdown = dropdowns[i];
            if (openDropdown.classList.contains('show')) {
                openDropdown.classList.remove('show');
            }
        }
    }
}

async function addLesson(day_number) {
    let id = localStorage.getItem('user_id');
    let day = document.getElementById(`day-${day_number}`);
    let lesson_number = document.getElementById(`day-${day_number}-lessons-count`).innerText;
    if (lesson_number !== '-1') {
        if (document.getElementById(`btn-${day_number}-${lesson_number}`).classList.contains('unsaved')) {
            Swal.fire({
                icon: 'error',
                title: 'Oops...',
                text: 'last lesson not saved'
            })
            return;
        }
    }
    let data = {
        'day_i': day_number,
        'lesson_i': lesson_number,
        'user_id': id,
        'group_id': localStorage.getItem('schedule_group_id')
    };
    let response = await callServer('/add_lesson', data, 'POST');
    if (response.ok) {
        day.removeChild(day.lastElementChild);
        day.insertAdjacentHTML('beforeend', await response.text());
        document.getElementById(`day-${day_number}-lessons-count`).innerText = parseInt(lesson_number) + 1;
    } else {
        checkCredentials(response.status);
        await alertError(response);
    }
}

async function loadSchedule(group_name, group_id) {
    if (group_name === 'load') {
        group_id = localStorage.getItem('schedule_group_id');
        group_name = localStorage.getItem('schedule_group_name');
    } else {
        localStorage.setItem('schedule_group_name', group_name);
        localStorage.setItem('schedule_group_id', group_id);
    }
    if (group_id !== null && group_name !== null) {
        document.getElementById('group').innerHTML = localStorage.getItem('schedule_group_name');
        let data = {"user_id": localStorage.getItem('user_id'), 'group_id': group_id};
        let response = await callServer(`/load_schedule?group_id=${group_id}`, data, 'PATCH');
        if (response.ok) {
            let wrapper = document.getElementById('schedule-wrapper');
            response = await response.text();
            wrapper.innerHTML = '';
            wrapper.innerHTML = response;
        } else {
            checkCredentials(response.status)
        }
    }
}

async function addLessonToDB(day_i, lesson_i) {
    if (document.getElementById(`lesson-${day_i}-${lesson_i}`).innerText === '') {
        Swal.fire({
                icon: 'error',
                title: 'Oops...',
                text: 'choose lesson'
            })
        return;
    }
    let lesson_id = document.getElementById(`lesson-${day_i}-${lesson_i}_id`).innerText;
    let group_id = localStorage.getItem('schedule_group_id');
    let data = {
        'lesson_id': lesson_id,
        'group_id': group_id,
        'day_number': day_i,
        'lesson_number': lesson_i
    };
    let response = await callServer('/execute/scheduleclass/create', data, 'POST');
    if (response.ok) {
        turnGreen(day_i, lesson_i);
        document.getElementById(`lesson-${day_i}-${lesson_i}_db_id`).innerText = lesson_id;
    } else {
        checkCredentials(response.status);
    }
}

async function deleteLesson(day_i) {
    let lesson_counter = document.getElementById(`day-${day_i}-lessons-count`);
    let day = document.getElementById(`day-${day_i}`);
    let group_id = localStorage.getItem('schedule_group_id');
    let data = {
        'day_number': day_i,
        'lesson_number': lesson_counter.innerText,
        'group_id': group_id
    };
    let response = await callServer('/execute/scheduleclass/delete', data, 'POST');
    if (response.ok) {
        day.removeChild(day.children[day.childElementCount - 2]);
        lesson_counter.innerText = parseInt(lesson_counter.innerText) - 1;
        if (day.childElementCount === 1) {
            let footer = document.getElementById(`footer-${day_i}`);
            footer.removeChild(footer.lastElementChild);
            footer.lastElementChild.setAttribute('style', 'width: 100%');
        }
    } else {
        checkCredentials(response.status);
    }
}

async function searchSchool() {
    let name = document.getElementById('name').value;
    let city = document.getElementById('city').value;
    let data = {
        'name': name,
        'city': city
    };
    let response = await callServer('/search_school', data, 'POST');
    if (response.ok) {
        document.getElementById('result-wrapper').innerHTML = await response.text();
    } else {
        checkCredentials(response.status);
        await alertError(response);
    }
}

async function linkSchool(school_id, school_number) {
    if (!window.confirm(`Are you sure to link profile to school ${school_number}?`)) {
        return;
    }
    let user_id = localStorage.getItem('user_id');
    let data = {
        'user_id': user_id,
        'school_id': school_id
    };
    let response = await callServer('/execute/admin/link_school', data, 'POST');
    if (response.ok) {
        Swal.fire({
            icon: 'success',
            title: 'Done',
            text: 'Linked'
        })
        window.location.reload(true);
    } else {
        checkCredentials(response.status);
        await alertError(response);
    }
}

function upgradeGroups() {
    if (!window.confirm('Are you sure')) return;
    let data = {'user_id': localStorage.getItem('user_id')}
    callServer('/upgrade_groups', data, 'POST').then((response) => {
        if (response.ok) {
            window.location.reload(true);
        }
        else {
            Swal.fire({
                icon: 'error',
                title: 'Oops...',
                text: 'Error!'
            })
        }
    })
}
