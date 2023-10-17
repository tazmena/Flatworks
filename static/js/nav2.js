// When the user scrolls down 80px from the top of the document, resize the navbar's padding and the logo's font size
window.onscroll = function() {scrollFunction()};

function scrollFunction() {
  if (document.documentElement.scrollTop > 3) {
    document.getElementById("navigation").style.padding = "18px 20px";
    document.getElementById("navbar-left").style.fontSize = "17px";
  } else {
    document.getElementById("navigation").style.padding = "80px 10px";
    document.getElementById("navbar-left").style.fontSize = "35px";
  }
}