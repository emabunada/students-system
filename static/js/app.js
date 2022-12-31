let searchForm = document.querySelector('.search-form');
let menu = document.querySelector('.navbar');

document.querySelector('#search-btn').onclick = function()  {
    searchForm.classList.toggle('active');
    menu.classList.remove('active');
}


document.querySelector('#menu-btn').onclick = function()  {
    menu.classList.toggle('active');
    searchForm.classList.remove('active');
}

window.onscroll=function() {
    searchForm.classList.remove('active');
    menu.classList.remove('active');
}