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
        window.open('/admin/add_group', '_self');
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
        window.open('/admin/add_student_key', '_self');
    } else {
        alert('error');
    }
}

async function addTeacherKey(){
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
        window.open('/admin/add_teacher_key', '_self');
    } else {
        alert('error');
    }
}

function downloadGroup(group) {
    window.open(`/download_group/${group}`, '_blank')
}

async function downloadTeachers(){
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
        window.open('/admin/add_subject', '_self');
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
        window.open('/admin/school', '_self');
    } else {
        alert('error');
    }
}
