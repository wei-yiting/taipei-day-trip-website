const attractionsContainer = document.getElementById('attractionsContainer');
const searchForm = document.getElementById('searchForm');
const searchKeyword = document.getElementById('searchKeyword');

let nextPage = 0;
let attractionsArray = [];
let readyToLoadAgain = false;
let keyword = null;


// ========= functions ===========

// load and visualize attractions
async function loadAttractions(keyword=null){
    if(nextPage !== null){
        nextPage = await getAttractionsData(nextPage,keyword);
        showAttractions();
        readyToLoadAgain = true;
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
    if(attractionsArray.length){
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
    
    attractionBox.innerHTML = `
        <a href= "/attraction/${attraction.id}" target="_blank">
            <img src="${attraction.images[0]}" alt="${attraction.name}">
            <div class="attraction-text-container">
                <p class="attraction-title">${attraction.name}</p>
                <div class="attraction-info">
                    <p class="attraction-mrt">${attraction.mrt ? attraction.mrt : "無鄰近捷運站"}</p>
                    <p class="attraction-category">${attraction.category}</p>
                </div>
            </div>
        </a>
    `

    return attractionBox;
}

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
    keyword = searchKeyword.value;
    loadAttractions(keyword);    
})