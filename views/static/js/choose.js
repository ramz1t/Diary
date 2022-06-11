function choose(type) {
    document.cookie = "type=" + type;
    window.open(`${type}/login`, '_self')
}
