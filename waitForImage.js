// Esconder o header e o footer
document.getElementById('atIdViewHeader').style.display = 'none';
document.querySelector('footer[jsname="yePe5c"]').style.display = 'none';

var checkImages = function() {
    var images = document.images;
    for (var i = 0; i < images.length; i++) {
        if (!images[i].complete) {
            return false;
        }
    }
    return true;
};

var waitForImages = function() {
    if (!checkImages()) {
        setTimeout(waitForImages, 100);
    } else {
        window.status = "ready";
    }
};

waitForImages();
