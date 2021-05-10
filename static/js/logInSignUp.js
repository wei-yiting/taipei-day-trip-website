// ================================================
// ============ Check if Logged In ================
// ================================================
fetch(`${window.origin}/api/user`)
.then(res => res.json())
.then(data => {
    if(data.data){
        document.getElementById('logInSignUp').classList.add('hide');
        document.getElementById('logOut').classList.remove('hide');
    }
})
.catch(err => {
    console.log(`fetch error : ${err}`)
})


// ==========================================
// ============ pop up modal ================
// ==========================================

const logInSignUp = document.getElementById('logInSignUp');
const signUpLink = document.getElementById('signUpLink');
const logInLink = document.getElementById('logInLink');
const logIn = document.getElementById('logIn');
const signUp = document.getElementById('signUp');
const signUpMessage = document.getElementById('signUpMessage');
const logInMessage = document.getElementById('logInMessage');


function clearMessage(element){
    element.classList.remove('error');
    element.classList.remove('success');
    element.textContent = '';
}

function slideIn(element){
    element.classList.add('slide-in');
} 

function hide(element){
    element.classList.remove('slide-in');
    element.classList.remove('show');

    // clear existed input
    const allInput = element.querySelectorAll('input');
    console.log(allInput);
    for (let input of allInput){
        input.value='';
    }
}

function show(element){
    element.classList.add('show');
    document.body.addEventListener('click',(evt)=>{
        if( !evt.target.closest('li#logInSignUp') && !evt.target.closest ('div.pop-up-modal')){
            hide(element);
            clearMessage(element.querySelector('span'));
        }
    })
}

logInSignUp.addEventListener('click', () => {
    slideIn(logIn);
    show(logIn);
})

signUpLink.addEventListener('click', () => {
    clearMessage(logInMessage);
    hide(logIn);
    show(signUp);
})

logInLink.addEventListener('click', () => {
    clearMessage(signUpMessage);
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


// ==============================================
// ============ Log In / Sign up ================
// ==============================================
function showMessage(error_type, targetElement){
    switch(error_type){
        case 'a':
            targetElement.textContent = "請先登出";
            break;
        case 'b':
            targetElement.textContent = "這個 Email 已被使用"
            break;
        case 'c':
            targetElement.textContent = "所有欄位不可為空白"
            break;
        case 'd':
            targetElement.textContent = "密碼錯誤"
            break;
        case 'e':
            targetElement.textContent = "此 Email 尚未註冊"
            break;
    }
}

// ======= log in =======
const logInForm = document.getElementById('logInForm');
logInForm.addEventListener('submit', evt => {
    evt.preventDefault();

    const logInEmail = document.getElementById('logInEmail');
    const logInPassword = document.getElementById('logInPassword');

    const email = logInEmail.value;
    const password = logInPassword.value;

    const requestBody = JSON.stringify({
        email: email,
        password: password
    });

    let responseStatus;

    fetch(`${window.origin}/api/user`,{
        method:'PATCH',
        headers: new Headers({ 
            'Content-Type': 'application/json'
        }),
        body: requestBody
    })
    .then(res => {
        responseStatus = res.status;
        return res.json();
    })
    .then(data => {
        if(data.ok){
            location.reload();
        }
        else if (data.error && responseStatus === 400){
            logInMessage.classList.add('error');
            error_type = data.message.split(':')[0];
            showMessage(error_type, logInMessage);
        }
        else if(data.error && responseStatus === 500){
            logInMessage.classList.add('error');
            logInMessage.textContent = "很抱歉，伺服器出現錯誤"; 
        }
    })
    .catch(err => {
        console.log(`fetch error : ${err}`)
    })
})


// ======= sign up =======
const signUpForm = document.getElementById('signUpForm');
signUpForm.addEventListener('submit', evt => {
    evt.preventDefault();

    const signUpName = document.getElementById('signUpName');
    const signUpEmail = document.getElementById('signUpEmail');
    const signUpPassword = document.getElementById('signUpPassword');

    const name = signUpName.value.trim();
    const email = signUpEmail.value.trim();
    const password = signUpPassword.value.trim();

    const requestBody = JSON.stringify({
        name: name,
        email: email,
        password: password
    });

    let responseStatus;

    fetch(`${window.origin}/api/user`,{
        method:'POST',
        headers: new Headers({ 
            'Content-Type': 'application/json'
        }),
        body: requestBody
    })
    .then(res => {
        responseStatus = res.status;
        return res.json();
    })
    .then(data => {
        if(data.ok){
            signUpMessage.classList.add('success');
            signUpMessage.textContent = "註冊成功"; 
            const logInLink = document.getElementById('logInLink');
            logInLink.textContent = "點此登入";
        }
        else if(data.error && responseStatus === 400){
            error_type = data.message.split(':')[0];
            signUpMessage.classList.add('error');
            showMessage(error_type, signUpMessage);
        }
        else if(data.error && responseStatus === 500){
            signUpMessage.classList.add('error');
            signUpMessage.textContent = "很抱歉，伺服器出現錯誤"; 
        }

    })
    .catch(err => {
        console.log(`fetch error : ${err}`)
    })
})


// =====================================
// ============ Log Out ================
// =====================================

const logOut = document.getElementById('logOut');

logOut.addEventListener('click', () => {
    fetch('/api/user',{method:'DELETE'})
    .then(res => res.json())
    .then(data => {
        if(data.ok){
            location.reload();
        }
    })
})















