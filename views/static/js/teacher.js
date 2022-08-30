function openClassBook() {
    const group_id = localStorage.getItem('book_group_id');
    const class_id = localStorage.getItem('book_class_id');
    callServer(`/class_book?group_id=${group_id}&class_id=${class_id}`).then(async (response) => {
        const book = await response.json();
        let wrapper = document.getElementById('wrapper');
        document.getElementById('group').innerText = book.name;
        document.getElementById('subject').innerText = book.subject;
        let book_wrapper = document.getElementById('book-wrapper');
        let table = document.createElement('table');
        let first_row = document.createElement('tr');
        first_row.innerHTML = `<th class="square absolute">№</th><th class="book-student-ns absolute">Student</th>`
        for (let i = 0; i < book['dates'].length; i++) {
            first_row.innerHTML += `<th class="square">${book['dates'][i].short}</th>`
        }
        first_row.innerHTML += '<th class="square">AVG</th>'
        table.appendChild(first_row);
        for (let i = 0; i < book['students'].length; i++) {
            let row = document.createElement('tr');
            row.innerHTML = ''
            row.innerHTML += `<th class="square absolute">
                              ${book['students'][i].number}</th>
                              <td class="book-student-ns absolute">
                              ${book['students'][i].surname} ${book['students'][i].name}
                              </td>`
            for (let j = 0; j < book['dates'].length; j++) {
                row.innerHTML += `<td onclick="addMark('${book['students'][i]['id']}', '${book['dates'][j].long}')"></td>`
            }
            row.innerHTML += `<td>${book['students'][i]['marks']['avg']}</td>`
            table.appendChild(row)
            // book_wrapper.innerHTML += `
            //     <div class='flex-row'>${book['students'][i].number} ${book['students'][i].surname} ${book['students'][i].name}</div>
            // `
        }
        book_wrapper.appendChild(table);
    })
}


function addMark(student_id, date) {
    console.log(student_id, date);
}