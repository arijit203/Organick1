let searchForm = document.querySelector('.search-form');

document.querySelector("#search-btn").onclick = () => {
    
    searchForm.classList.toggle('active');
}


let cart=document.querySelector('.shopping-cart');

document.querySelector("#cart-btn").onclick=()=>{
    console.log("Hi there");
    cart.classList.toggle('active');
}

let user=document.querySelector('.login-form');

document.querySelector("#user-btn").onclick=()=>{
    console.log("Hi there");
    user.classList.toggle('active');
}


