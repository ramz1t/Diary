function choose(type) {
    localStorage.setItem('type', type);
    window.open(`${type}/login`, '_self')
}
