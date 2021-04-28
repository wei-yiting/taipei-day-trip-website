const attractionsContainer = document.getElementById('attractionsContainer');
const searchForm = document.getElementById('searchForm');
const searchKeyword = document.getElementById('searchKeyword');

let nextPage = 0;
let attractionsArray = [];
let readyToLoadAgain = false;
let keyword = null;
let totalAttractionsNum = 0;
let createdAttractonBoxesNum = 0;


// =========== initial load and event listener ========

// initial load
loadAttractions();


// infinite scroll : listen of scroll event
if(nextPage !== null){
    window.addEventListener('scroll',()=>{
        if((window.innerHeight + window.scrollY) >= (document.body.getBoundingClientRect().bottom) && readyToLoadAgain){
            loadAttractions(keyword);
            readyToLoadAgain = false;
        }
    })
}

// attraction keyword search : submit search form
searchForm.addEventListener('submit',(evt)=>{
    evt.preventDefault();
    attractionsContainer.innerHTML = '';
    nextPage = 0;
    totalAttractionsNum = 0;
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


// fetch attractions api and get (called in loadAttractions function)
async function getAttractionsData(pageNum, keyword=null){
    let apiUrl;
    if(keyword){
        apiUrl = `/api/attractions?page=${pageNum}&keyword=${keyword}`;
    }else{
        apiUrl = `/api/attractions?page=${pageNum}`;
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
    totalAttractionsNum += attractionsArray.length;
    if(attractionsArray.length){
        for(let attraction of attractionsArray){
            const attractionBox = createAttractionItem(attraction);
            attractionsContainer.appendChild(attractionBox);
        }
    }
    else if(!(totalAttractionsNum)){
        const message = document.createElement('span');
        message.textContent = "未找到符合關鍵字的景點";
        attractionsContainer.appendChild(message);
    }
    createdAttractonBoxesNum = attractionsContainer.childElementCount;
    itemCreatedCalc();
}


// create single attraction item (called in showAttractions function)
function createAttractionItem(attraction){

    const attractionBox = document.createElement('article');
    attractionBox.classList.add('attraction-box');
    
    const linkContainer = document.createElement('a');
    linkContainer.href = `/attraction/${attraction.id}`
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

    return attractionBox;
}


// check if all container box in a page is created (called in createAttractionItem function )
function itemCreatedCalc(){
    if(createdAttractonBoxesNum === totalAttractionsNum){
        readyToLoadAgain = true;
    }
}
