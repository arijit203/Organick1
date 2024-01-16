// let searchForm = document.querySelector('.search-form');

//     document.querySelector("#search-btn").onclick = () => {
    
//     searchForm.classList.toggle('active');
// }


// let cart=document.querySelector('.shopping-cart');

// document.querySelector("#cart-btn").onclick=()=>{
//     console.log("Hi there");
//     cart.classList.toggle('active');
// }

// let user=document.querySelector('.login-form');

// document.querySelector("#user-btn").onclick=()=>{
//     console.log("Hi there");
//     user.classList.toggle('active');
// }


document.addEventListener('DOMContentLoaded', function () {
    var userForm = document.querySelector('.login-form');
    var userButton = document.getElementById('user-btn');
    var shoppingCart = document.querySelector('.shopping-cart');
    var searchForm = document.querySelector('.search-form');

    // Toggle user form visibility on user button click
    userButton.addEventListener('click', function (event) {
        event.stopPropagation(); // Prevent the click from closing the form immediately
        userForm.classList.toggle('active');
        shoppingCart.classList.remove('active');
        searchForm.classList.remove('active');
    });

    // Close user form when clicking anywhere outside the form
    document.body.addEventListener('click', function () {
        userForm.classList.remove('active');
    });

    // Prevent clicks inside the user form from closing it
    userForm.addEventListener('click', function (event) {
        event.stopPropagation();
    });
});   


document.addEventListener('DOMContentLoaded', function () {
    var shoppingCart = document.querySelector('.shopping-cart');
    var cartButton = document.getElementById('cart-btn');
    var userForm = document.querySelector('.login-form');
    var searchForm = document.querySelector('.search-form');


    // Toggle shopping cart visibility on cart button click
    cartButton.addEventListener('click', function (event) {
        event.stopPropagation(); // Prevent the click from closing the cart immediately
        shoppingCart.classList.toggle('active');
        userForm.classList.remove('active');
        searchForm.classList.remove('active');
    });

    // Close shopping cart when clicking anywhere outside the cart
    document.body.addEventListener('click', function () {
        shoppingCart.classList.remove('active');
    });

    // Prevent clicks inside the shopping cart from closing it
    shoppingCart.addEventListener('click', function (event) {
        event.stopPropagation();
    });
});

document.addEventListener('DOMContentLoaded', function () {
    var searchForm = document.querySelector('.search-form');
    var searchButton = document.getElementById('search-btn');
    var shoppingCart = document.querySelector('.shopping-cart');
    var userForm = document.querySelector('.login-form');

    // Toggle search form visibility on search button click
    searchButton.addEventListener('click', function (event) {
        event.stopPropagation(); // Prevent the click from closing the form immediately
        searchForm.classList.toggle('active');
        shoppingCart.classList.remove('active');
        userForm.classList.remove('active');
    });

    // Close search form when clicking anywhere outside the form
    document.body.addEventListener('click', function () {
        searchForm.classList.remove('active');
    });

    // Prevent clicks inside the search form from closing it
    searchForm.addEventListener('click', function (event) {
        event.stopPropagation();
    });
});


let slides=document.querySelectorAll('.home .slides-container .mini_header');
let index=0;

function next(){
    slides[index].classList.remove('active');
    index=(index+1) % slides.length;
    slides[index].classList.add('active');
}

function prev(){
    slides[index].classList.remove('active');
    index=(index-1+slides.length)%slides.length;
    slides[index].classList.add('active');
}

