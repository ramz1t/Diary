function openClassBook() {
    const group_id = localStorage.getItem('book_group_id');
    const class_id = localStorage.getItem('book_class_id');
    callServer(`/class_book?group_id=${group_id}&class_id=${class_id}`).then(async (response) => {
        const book = await response.json();
        let wrapper = document.getElementById('wrapper');
        document.getElementById('book-name').innerText = book.name
        let book_wrapper = document.getElementById('book-wrapper');
        let table = document.createElement('table');

        for (let i = 0; i < book['students'].length; i++) {
            book_wrapper.innerHTML += `
                <div class='flex-row'>${book['students'][i].number} ${book['students'][i].surname} ${book['students'][i].name}</div>
            `
        }
    })
}