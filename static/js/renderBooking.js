// ================================================
// ============ Check if Logged In ================
// ================================================
(function checkIfLogIn() {
  fetch(`${window.origin}/api/user`)
    .then((res) => res.json())
    .then((data) => {
      if (!data.data) {
        location.href = "/";
      } else {
        document.getElementById("main").classList.remove("hide-before-log-in");
      }
    })
    .catch((err) => {
      console.log(`fetch error : ${err}`);
    });
})();

// =======================================================
// ============ Render Booking Attraction ================
// =======================================================

async function getBookingData() {
  const res = await fetch(`${window.origin}/api/booking`);
  const data = await res.json();
  const bookingData = data.data;
  return bookingData;
}

// helper function
function createElementWithClass(tagName, className = null) {
  const newElement = document.createElement(tagName);
  if (className) {
    newElement.classList.add(className);
  }
  return newElement;
}

let totalPrice = 0;

function renderBookingAttractions(data) {
  if (!data) {
    document.getElementsByTagName("main")[0].classList.add("main-no-booking");
    document.getElementsByTagName("footer")[0].classList.add("footer-no-booking");
  } else {
    for (let attraction of data) {
      renderSingleAttraction(attraction);
    }
    document.getElementById("bookingPrice").textContent = totalPrice;
  }
}

function renderSingleAttraction(data) {
  document.getElementsByClassName("no-booking")[0].classList.add("hide");
  document.getElementsByClassName("has-booking")[0].classList.remove("hide");

  const bookingAttraction = createElementWithClass("section", "booking-attraction");
  bookingAttraction.dataset.attractionId = data.attraction.id;
  const bookingAttractionInfo = createElementWithClass("div", "booking-attraction-info");
  const attractionImageContainer = createElementWithClass("div", "attraction-image-container");
  const attractionImage = createElementWithClass("img");
  attractionImage.src = data.attraction.image;
  const bookingDetail = createElementWithClass("div", "booking-detail");
  const attractionHeader = createElementWithClass("h3", "body-bold");
  attractionHeader.innerHTML = `台北一日遊：<span>${data.attraction.name}</span>`;
  const bookingDate = createElementWithClass("p", "body-bold");
  bookingDate.innerHTML = `日期：<span class="body-reg">${data.date}</span>`;
  const bookingTime = createElementWithClass("p", "body-bold");
  let time;
  if (data.time === "morning") {
    time = "早上 9 點到下午 4 點";
  } else if (data.time === "afternoon") {
    time = "下午 2 點到晚上 9 點";
  }
  bookingTime.innerHTML = `時間：<span class="body-reg">${time}</span>`;
  const bookingPrice = createElementWithClass("p", "body-bold");
  bookingPrice.innerHTML = `費用：<span class="body-reg">新台幣 ${data.price} 元</span>`;
  const attractionAddress = createElementWithClass("p", "body-bold");
  attractionAddress.innerHTML = `地點：<span class="body-reg">${data.attraction.address}</span>`;
  const deleteIcon = createElementWithClass("img", "delete");
  deleteIcon.src = "../static/images/icon_delete.png";
  deleteIcon.alt = "刪除預定行程";

  bookingDetail.appendChild(attractionHeader);
  bookingDetail.appendChild(bookingDate);
  bookingDetail.appendChild(bookingTime);
  bookingDetail.appendChild(bookingPrice);
  bookingDetail.appendChild(attractionAddress);

  attractionImageContainer.appendChild(attractionImage);

  bookingAttractionInfo.appendChild(attractionImageContainer);
  bookingAttractionInfo.appendChild(bookingDetail);
  bookingAttractionInfo.appendChild(deleteIcon);

  bookingAttraction.appendChild(bookingAttractionInfo);

  document.getElementsByClassName("has-booking")[0].prepend(bookingAttraction);
  totalPrice += data.price;
}

(async () => {
  const bookingData = await getBookingData();
  renderBookingAttractions(bookingData);
  deleteBooking();
})();

// ====================================================
// ============ Get / Render user info ================
// ====================================================

async function getUserInfo() {
  const res = await fetch("/api/user");
  const data = await res.json();
  const userData = data.data;
  return userData;
}

function renderUserInfo(data) {
  document.getElementById("username").textContent = data.name;
  document.getElementById("bookingName").value = data.name;
  document.getElementById("bookingEmail").value = data.email;
}

(async () => {
  const userdata = await getUserInfo();
  renderUserInfo(userdata);
})();

// ============================================
// ============ Delete Booking ================
// ============================================
function deleteBooking() {
  const deleteIcons = document.querySelectorAll(".delete");
  for (let deleteIcon of deleteIcons) {
    deleteIcon.addEventListener("click", () => {
      const attractionId = parseInt(deleteIcon.parentElement.parentElement.dataset.attractionId);
      const requestBody = JSON.stringify({ attractionId: attractionId });
      console.log(requestBody);
      fetch("/api/booking", {
        method: "DELETE",
        headers: new Headers({
          "Content-Type": "application/json",
        }),
        body: requestBody,
      })
        .then((res) => res.json())
        .then((data) => {
          if (data.ok) {
            console.log("delete!!");
            window.location.reload();
          } else if (data.error) {
            console.log(data.message);
          }
        })
        .catch((err) => {
          console.log(`fetch error : ${err}`);
        });
    });
  }
}

// ==========================================
// ============ Enable order ================
// ==========================================
