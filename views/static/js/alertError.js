async function alertError(response) {
    if (!response.ok) {
        // alert(await response.text());
        Swal.fire({
            icon: 'error',
            title: 'Oops...',
            text: await response.text()
        })
        throw new Error(`error ${response.status}`)
    }
}