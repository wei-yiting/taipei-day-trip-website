const attractionsContainer = document.getElementById('attractionsContainer');
const searchForm = document.getElementById('searchForm');
const searchKeyword = document.getElementById('searchKeyword');
const ipUrl = "127.0.0.1"

let nextPage = 0;
let attractionsArray = [];
let readyToLoadAgain = false;
let imagesLoadedNum = 0;
let totalImagesToLoad;
let keyword = null;


// =========== initial load and event listener ========

// initial load
loadAttractions();


// infinite scroll : listen of scroll event
if(nextPage !== null){
    window.addEventListener('scroll',()=>{
        if((window.innerHeight + window.scrollY) >= (document.body.getBoundingClientRect().bottom - 400) && readyToLoadAgain){
            loadAttractions(keyword);
            readyToLoadAgain = false;
        }
    })
}

// attraction keyword search : submit search form
searchForm.addEventListener('submit',(evt)=>{
    evt.preventDefault();
    removeAttractions();
    nextPage = 0;
    keyword = searchKeyword.value;
    loadAttractions(keyword);    
})


// ========= function ===========

// load and visualize attractions
// calling getAttractionsData and showAttractions function
async function loadAttractions(keyword=null){
    if(nextPage !== null){
        nextPage = await getAttractionsData(nextPage,keyword);
        showAttractions();
    }
}

// remove attractions gallery (called when a keyword search is submit)
function removeAttractions(){
    while(attractionsContainer.firstChild){
        attractionsContainer.removeChild(attractionsContainer.lastChild);
    }
}

// fetch attractions api and get (called in loadAttractions function)
async function getAttractionsData(pageNum, keyword=null){
    let apiUrl;
    if(keyword){
        apiUrl = `http://${ipUrl}:3000/api/attractions?page=${pageNum}&keyword=${keyword}`;
    }else{
        apiUrl = `http://${ipUrl}:3000/api/attractions?page=${pageNum}`;
    }
    const response = await fetch(apiUrl);
    const data = await response.json();
    nextPage = data.nextPage;
    attractionsArray = data.data;
    return nextPage;
}

// show all attractions in the same page (called in loadAttractions function)
function showAttractions(){
    imagesLoadedNum = 0;
    totalImagesToLoad = attractionsArray.length;
    if(totalImagesToLoad){
        for(let attraction of attractionsArray){
            const attractionBox = createAttractionItem(attraction);
            attractionsContainer.appendChild(attractionBox);
        }
    }
    else if(!(attractionsContainer.firstChild)){
        const message = document.createElement('span');
        message.textContent = "未找到符合關鍵字的景點";
        attractionsContainer.appendChild(message);
    }
}


// create single attraction item (called in showAttractions function)
function createAttractionItem(attraction){

    const attractionBox = document.createElement('article');
    attractionBox.classList.add('attraction-box');
    
    const linkContainer = document.createElement('a');
    linkContainer.href = `http://${ipUrl}:3000/attraction/${attraction.id}`
    linkContainer.setAttribute('target', '_blank');
    
    const attractionImage = document.createElement('img');
    attractionImage.src = attraction.images[0]
    
    const attractionTextContainer = document.createElement('div');
    attractionTextContainer.classList.add('attraction-text-container');
    
    const attractionTitle = document.createElement('p');
    attractionTitle.classList.add('attraction-title');
    attractionTitle.textContent = attraction.name;
    
    const attractionInfo = document.createElement('div');
    attractionInfo.classList.add('attraction-info');
    
    const attractionMrt = document.createElement('p');
    attractionMrt.classList.add('attraction-mrt');
    attractionMrt.textContent = attraction.mrt;
    
    const attractionCategory = document.createElement('p');
    attractionCategory.classList.add('attraction-category');
    attractionCategory.textContent = attraction.category;

    attractionInfo.appendChild(attractionMrt);
    attractionInfo.appendChild(attractionCategory);

    attractionTextContainer.appendChild(attractionTitle);
    attractionTextContainer.appendChild(attractionInfo);

    linkContainer.appendChild(attractionImage);
    linkContainer.appendChild(attractionTextContainer);
    
    attractionBox.appendChild(linkContainer);

    attractionImage.addEventListener('load',imageLoaded);

    return attractionBox;
}

// check if all item in a page is loaded (called in createAttractionItem function )
function imageLoaded(){
    imagesLoadedNum++;
    if(imagesLoadedNum === totalImagesToLoad && nextPage !== null){
        readyToLoadAgain = true;
    }
}

