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
