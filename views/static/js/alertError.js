async function alertError(response) {
    if (!response.ok) {
        Swal.fire({
            icon: 'error',
            title: 'Oops...',
            text: await response.text(),
            position: 'top',
            timer: 3000,
            timerProgressBar: true,
            showConfirmButton: false,
        })
        throw new Error(`error ${response.status}`)
    }
}