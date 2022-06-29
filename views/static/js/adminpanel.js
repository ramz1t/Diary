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
    var name = document.getElementById('name').value.trim();
    var surname = document.getElementById('surname').value.trim();
    if (document.querySelector('input[name="group"]:checked') != null) {
        var group = document.querySelector('input[name="group"]:checked').value;
    } else {
        return
    }
    var response = await fetch('/add_student_key_to_db', {
        method: 'POST',
        headers: {
            'accept': 'application/json',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            'name': name,
            'surname': surname,
            'group': group
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
    var response = await fetch('/add_school_to_db', {
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

async function loadPage(page) {
    if (page === 'load') {
        page = $.cookie("page");
    } else {
        document.cookie = "page=" + page;
    }
    if (page !== undefined) {
        var response = await fetch(`/load_page/${page}`, {
            headers: {
                'accept': 'application/json'
            }
        });
        if (response.ok) {
            var wrapper = document.getElementById('wrapper');
            response = await response.text();
            wrapper.innerHTML = '';
            wrapper.innerHTML = response;
        }
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
    var response = await fetch('/add_class_to_db', {
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
        var text = await response.json();
        alert(text);
    } else {
        alert('error');
    }
}
