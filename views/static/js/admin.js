async function addGroup() {
    var school_id = $.cookie("school_id");
    var groupName = document.getElementById("groupname").value;
    var response = await fetch('/execute/group/create', {
        method: 'POST',
        headers: {
            'accept': 'application/json',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            'name': groupName,
            'school_id': school_id
        })
    });
    if (response.ok) {
        document.location.reload(true);
    } else {
        checkCredentials(response.status);
        await alertError(response);
    }
}

async function addStudentKey() {
    var school_id = $.cookie("school_id");
    var name = document.getElementById('name').value.trim();
    var surname = document.getElementById('surname').value.trim();
    if (document.querySelector('input[name="group"]:checked') != null) {
        var group = document.querySelector('input[name="group"]:checked').value;
    } else {
        return
    }
    var response = await fetch('/execute/studentkey/add_key', {
        method: 'POST',
        headers: {
            'accept': 'application/json',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            'name': name,
            'surname': surname,
            'group': group,
            'school_id': school_id
        })
    });
    if (response.ok) {
        document.location.reload(true);
    } else {
        checkCredentials(response.status);
        await alertError(response);
    }
}

async function addTeacherKey() {
    var school_id = $.cookie("school_id");
    var name = document.getElementById('name').value.trim();
    var surname = document.getElementById('surname').value.trim();
    var response = await fetch('/execute/teacherkey/add_key', {
        method: 'POST',
        headers: {
            'accept': 'application/json',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            'school_id': school_id,
            'name': name,
            'surname': surname,
        })
    });
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
    var school_id = $.cookie("school_id");
    var subject = document.getElementById('subject').value;
    if (document.querySelector('input[name="type"]:checked') != null) {
        var lesson_type = document.querySelector('input[name="type"]:checked').value;
    } else {
        return
    }
    var response = await fetch('/execute/subject/create', {
        method: 'POST',
        headers: {
            'accept': 'application/json',
            'Content-Type': 'application/json'
        },

        body: JSON.stringify({
            'school_id': school_id,
            'name': subject,
            'type': lesson_type
        })
    });
    if (response.ok) {
        document.location.reload(true);
    } else {
        checkCredentials(response.status);
        await alertError(response);
    }
}

async function addSchool() {
    var city = document.getElementById('city').value;
    var response = await fetch('/execute/school/create', {
        method: 'POST',
        headers: {
            'accept': 'application/json',
            'Content-Type': 'application/json'
        },

        body: JSON.stringify({
            'city': city
        })
    });
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

async function addClass() {
    var school_id = $.cookie("school_id");
    var group = document.getElementById('group').innerText.trim();
    var subject = document.getElementById('subject').innerText.trim();
    var teacher = document.getElementById('teacher').innerText.trim();
    if (group === 'Choose group' || subject === 'Choose subject' || teacher === 'Choose teacher') {
        alert('not enough info');
        return;
    }
    var response = await fetch('/execute/cls/create', {
        method: 'POST',
        headers: {
            'accept': 'application/json',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            'group_id': document.getElementById('group_id').innerText,
            'subject_id': document.getElementById('subject_id').innerText,
            'teacher_id': document.getElementById('teacher_id').innerText,
            'school_id': school_id
        })
    });
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
        var dropdowns = document.getElementsByClassName("class-dropdown-content");
        var i;
        for (i = 0; i < dropdowns.length; i++) {
            var openDropdown = dropdowns[i];
            if (openDropdown.classList.contains('show')) {
                openDropdown.classList.remove('show');
            }
        }
    }
}

function chooseGroup(group, id) {
    document.getElementById('group').innerHTML = group;
    document.cookie = "group=" + id;
    loadSchedule(group, id)
}

async function addLesson(day_number) {
    var school_id = $.cookie("school_id");
    var day = document.getElementById(`day-${day_number}`);
    var lesson_number = document.getElementById(`day-${day_number}-lessons-count`).innerText;
    if (lesson_number !== '-1') {
        if (document.getElementById(`btn-${day_number}-${lesson_number}`).classList.contains('unsaved')) {
            alert('last lesson not saved');
            return;
        }
    }
    var response = await fetch('/add_lesson', {
        method: 'POST',
        headers: {
            'accept': 'application/json',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            'day_i': day_number,
            'lesson_i': lesson_number,
            'school_id': school_id
        })
    });
    if (response.ok) {
        day.removeChild(day.lastElementChild);
        var text = await response.text();
        day.insertAdjacentHTML('beforeend', text);
        document.getElementById(`day-${day_number}-lessons-count`).innerText = parseInt(lesson_number) + 1;
    } else {
        checkCredentials(response.status);
        await alertError(response);
    }
}

async function loadSchedule(group_name, group_id) {
    if (group_name === 'load') {
        group_id = $.cookie("group");
    } else {
        document.cookie = "group=" + group_id;
    }
    if (group_name !== undefined) {
        console.log('loading', group_name, group_id);
    }
}

async function addLessonToDB(day_i, lesson_i) {
    if (document.getElementById(`lesson-${day_i}-${lesson_i}`).innerText === '') {
        alert('choose lesson');
        return;
    }
    var lesson_id = document.getElementById(`lesson-${day_i}-${lesson_i}_id`).innerText;
    var group_id = $.cookie("group");
    document.getElementById(`btn-${day_i}-${lesson_i}`).classList.remove('unsaved');
    document.getElementById(`icon-${day_i}-${lesson_i}`).classList.remove('bi-cloud-minus');
    document.getElementById(`icon-${day_i}-${lesson_i}`).classList.add('bi-cloud-check');
}

async function deleteLesson(day_i) {
    var day = document.getElementById(`day-${day_i}`);
    day.removeChild(day.children[day.childElementCount - 2]);
    var lesson_counter = document.getElementById(`day-${day_i}-lessons-count`);
    lesson_counter.innerText = parseInt(lesson_counter.innerText) - 1;
    if (day.childElementCount === 1) {
        var footer = document.getElementById(`footer-${day_i}`);
        footer.removeChild(footer.lastElementChild);
        footer.lastElementChild.setAttribute('style', 'width: 100%');
    }
}

async function searchSchool() {
    var name = document.getElementById('name').value;
    var city = document.getElementById('city').value;
    var response = await fetch('/search_school', {
        method: 'POST',
        headers: {
            'accept': 'application/json',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            'name': name,
            'city': city
        })
    });
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
    var user_id = document.getElementById('db_id').innerText;
    var response = await fetch('/execute/admin/link_school', {
        method: 'POST',
        headers: {
            'accept': 'application/json',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            'id': user_id,
            'school_id': school_id
        })
    });
    if (response.ok) {
        alert('linked');
    } else {
        checkCredentials(response.status);
        await alertError(response);
    }
}