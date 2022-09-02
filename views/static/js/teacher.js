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
                const date = book.dates[j].long
                let mark = book.students[i].marks.all[date];
                if (mark === undefined) {
                    mark = '';
                }
                row.innerHTML += `<td id="${book.students[i].id}-${book.dates[j].long}"
                                    class="pointer mark-click-target-area" 
                                    data-student-id ="${book.students[i].id}" 
                                    data-date = "${book.dates[j].long}"
                                    data-initials = "${book.students[i].surname} ${book.students[i].name}">
                                    ${mark}
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
        const y = e.clientY + window.scrollY - (e.clientY + window.scrollY - 105) % 35;
        let x = e.clientX + window.scrollX - (e.clientX + window.scrollX - 260) % 35 + 35;
        if (window.screen.width + window.scrollX - x < 315) {
            x -= 350
        }
        modalWindow.style.left = `${x}px`;
        modalWindow.style.top = `${y}px`;
        const modal = document.getElementById('mark-modal');
        modal.setAttribute('data-modal-date', date);
        modal.setAttribute('data-modal-student-id', studentId);
        document.getElementById('student_name').innerText = name;
        document.getElementById('mark_date').innerText = date;
        modalWindow.classList.remove('none');
    }
}

function placeMark(mark) {
    const modal = document.getElementById('mark-modal');
    modal.setAttribute('data-mark', mark);
    console.log(`${modal.dataset.modalStudentId}-${modal.dataset.modalDate}`);
    const cell = document.getElementById(`${modal.dataset.modalStudentId}-${modal.dataset.modalDate}`);
    cell.innerText = mark;
    cell.classList.add('red');
}

function dismissMark() {
    const modal = document.getElementById('mark-modal');
    const cell = document.getElementById(`${modal.dataset.modalStudentId}-${modal.dataset.modalDate}`);
    cell.innerText = '';
    cell.classList.remove('red');
    document.getElementById('modal-container').classList.add('none');
}

function sendMark() {
    const modal = document.getElementById('mark-modal');
    const date = modal.dataset.modalDate;
    const mark = modal.dataset.mark;
    const studentId = modal.dataset.modalStudentId;
    const data = {'date': date, 'mark': mark, 'student_id': studentId, 'subject_id': localStorage.getItem('book_class_id')}
    callServer('/execute/mark/create', data, 'POST').then((response) => {
        const p = alertError(response);
        checkCredentials(response);
        document.getElementById('modal-container').classList.add('none');
        document.getElementById(`${studentId}-${date}`).classList.remove('red');
    });
}