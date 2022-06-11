async function addGroup() {
    var groupName = document.getElementById("groupname").value;
    var response = await fetch('/add_group', {
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
        alert('group added');
    } else {
        alert('error');
    }
}


async function addKey() {
    var name = document.getElementById('name').value;
    var surname = document.getElementById('surname').value;
    var group = document.getElementById('group').value;
    var schoolid = document.getElementById('schoolid').value;
    var response = await fetch('/add_key', {
                            method: 'POST',
                            headers: {
                                'accept': 'application/json',
                                'Content-Type': 'application/json'
                            },
                            body: JSON.stringify({
                                'name': name,
                                'surname': surname,
                                'group': group,
                                'school_id': schoolid
                            })
                        });
    if (response.ok) {
        window.open('/admin', '_self')
    } else {
        alert('error');
    }
}

function download(value) {
    window.open(`download/${value}`)
}
