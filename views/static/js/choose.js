function choose(type) {
    document.cookie = "type=" + type;
    window.open('/login', '_self')
}