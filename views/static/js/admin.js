async function addGroup() {
    var groupName = document.getElementById("groupname").value;
    var response = await fetch('/add_group_to_db', {
        method: 'POST',
        headers: {
            'accept': 'application/json',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            'name': groupName
        })
    });
    if (response.ok) {
        document.location.reload(true);
    } else {
        alert('error');
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
        alert('error');
    }
}

async function addTeacherKey() {
    var name = document.getElementById('name').value.trim();
    var surname = document.getElementById('surname').value.trim();
    var response = await fetch('/add_teacher_key_to_db', {
        method: 'POST',
        headers: {
            'accept': 'application/json',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            'name': name,
            'surname': surname,
        })
    });
    if (response.ok) {
        document.location.reload(true);
    } else {
        alert('error');
    }
}

function downloadGroup(group) {
    window.open(`/download_group/${group}`, '_blank')
}

async function downloadTeachers() {
    window.open('/download_teachers', '_blank')
}


async function manageGroups() {
    window.open('/admin/managegroups', '_self')
}

async function addSubject() {
    var subject = document.getElementById('subject').value;
    if (document.querySelector('input[name="type"]:checked') != null) {
        var lesson_type = document.querySelector('input[name="type"]:checked').value;
    } else {
        return
    }
    var response = await fetch('/add_subject_to_db', {
        method: 'POST',
        headers: {
            'accept': 'application/json',
            'Content-Type': 'application/json'
        },

        body: JSON.stringify({
            'name': subject,
            'type': lesson_type
        })
    });
    if (response.ok) {
        document.location.reload(true);
    } else {
        alert('error');
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
        alert('error');
    }
}

function setValue(type, value, id) {
    document.getElementById(type).innerHTML = value;
    document.getElementById(type + '_id').innerText = id;
}

async function addClass() {
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
            'teacher_id': document.getElementById('teacher_id').innerText
        })
    });
    if (response.ok) {
        document.location.reload(true);
    } else {
        var text = await response.json();
        alert(text);
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
    var day = document.getElementById(`day-${day_number}`);
    var lesson_number = document.getElementById(`day-${day_number}-lessons-count`).innerText;
    var response = await fetch('http://127.0.0.1:8003/add_lesson', {
        method: 'POST',
        headers: {
        'accept': 'application/json',
        'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            'day_i': day_number,
            'lesson_i': lesson_number
        })
    });
    if (response.ok) {
        day.removeChild(day.lastElementChild);
        var text = await response.text();
        day.insertAdjacentHTML('beforeend', text);
        document.getElementById(`day-${day_number}-lessons-count`).innerText = parseInt(lesson_number) + 1;
    }
}

async function loadSchedule(group_name, group_id) {
    console.log(group_id, group_name);
    if (group_name === 'load') {
        group_id = $.cookie("group");
    } else {
        document.cookie = "group=" + group_id;
    }
    if (group_name !== undefined) {
        console.log('loading', group_name, group_id);
    }
}
