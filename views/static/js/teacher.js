function openClassBook() {
    const group_id = localStorage.getItem('book_group_id');
    const class_id = localStorage.getItem('book_class_id');
    callServer(`/class_book?group_id=${group_id}&class_id=${class_id}`).then(async (response) => {
        const book = await response.json();
        document.getElementById('group').innerText = book.name;
        document.getElementById('subject').innerText = book.subject;
        let book_wrapper = document.getElementById('book-wrapper');
        let table = document.createElement('table');
        let first_row = document.createElement('tr');
        first_row.innerHTML = `<th class="square absolute">№</th><th class="book-student-ns absolute">Student</th>`
        for (let i = 0; i < book.dates.length; i++) {
            first_row.innerHTML += `<th class="square">${book.dates[i].short}</th>`
        }
        first_row.innerHTML += '<th class="square">AVG</th>'
        table.appendChild(first_row);
        for (let i = 0; i < book.students.length; i++) {
            let row = document.createElement('tr');
            row.innerHTML = ''
            row.innerHTML += `<th class="square absolute">
                              ${book.students[i].number}</th>
                              <td class="book-student-ns absolute">
                              ${book.students[i].surname} ${book.students[i].name}
                              </td>`
            for (let j = 0; j < book.dates.length; j++) {
                // mark cells
                row.innerHTML += `<td class="pointer mark-click-target-area" 
                                    data-student-id ="${book.students[i].id}" 
                                    data-date = "${book.dates[j].long}"
                                    data-initials = "${book.students[i].surname} ${book.students[i].name}">
                                  </td>`
            }
            row.innerHTML += `<td>${book.students[i].marks.avg}</td>`
            table.appendChild(row)
        }
        book_wrapper.appendChild(table);
    })
}

document.addEventListener('click', addMark)

function addMark(e) {
    const modalWindow = document.getElementById('modal-container');
    if (e.target.classList.contains('mark-click-target-area')) {
        const studentId = parseInt(e.target.dataset.studentId);
        const date = e.target.dataset.date;
        const name = e.target.dataset.initials;
        const y = e.clientY + window.scrollY;
        const x = e.clientX + window.scrollX;
        modalWindow.style.left = `${x}px`;
        modalWindow.style.top = `${y}px`;
        document.getElementById('student_name').innerText = name;
        document.getElementById('mark_date').innerText = date;
    }
}