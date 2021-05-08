const logInSignUp = document.getElementById('logInSignUp');
const signUpLink = document.getElementById('signUpLink');
const logInLink = document.getElementById('logInLink');
const logIn = document.getElementById('logIn');
const signUp = document.getElementById('signUp');

function show(element){
    element.classList.add('show');
    document.body.addEventListener('click',(evt)=>{
        if( !evt.target.closest('li#logInSignUp') && !evt.target.closest ('div.pop-up-modal')){
            console.log("click outside");
            hide(element);
        }
    })
}

function hide(element){
    element.classList.remove('show');
}

logInSignUp.addEventListener('click', () => {
    show(logIn);
})

signUpLink.addEventListener('click', () => {
    hide(logIn);
    show(signUp);
})

logInLink.addEventListener('click', () => {
    hide(signUp);
    show(logIn);
})


const logInClose = document.getElementById('logInClose');
const signUpClose = document.getElementById('signUpClose');

logInClose.addEventListener('click', ()=>{
    hide(logIn);
})

signUpClose.addEventListener('click', ()=>{
    hide(signUp);
})










