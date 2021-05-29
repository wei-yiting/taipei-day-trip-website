// setup SDK
TPDirect.setupSDK(20405, "app_FhMCb4l1iWNNE63mv1IyPd0gBoqveM6PFfcVA13n1LKSEYx4opOYaoh9YDed", "sandbox");

//==== TPDirect.card.setup=======
let config = {
  // Display ccv field
  fields: {
    number: {
      // css selector
      element: "#card-number",
      placeholder: "**** **** **** ****",
    },
    expirationDate: {
      // DOM object
      element: document.getElementById("card-expiration-date"),
      placeholder: "MM / YY",
    },
    ccv: {
      element: "#card-ccv",
      placeholder: "ccv",
    },
  },
  styles: {
    // Style all elements
    input: {
      color: "gray",
      "font-size": "16px",
    },
    // style focus state
    ":focus": {
      color: "black",
    },
    // style valid state
    ".valid": {
      color: "#55aaaa",
    },
    // style invalid state
    ".invalid": {
      color: "#be7749",
    },
  },
};

TPDirect.card.setup(config);

//======= on Update ========

// helper function
function showSuccessIcon(inputField) {
  const formControl = inputField.parentElement;
  formControl.classList.add("success");
}

function removeSuccessIcon(inputField) {
  const formControl = inputField.parentElement;
  formControl.classList.remove("success");
}

function showErrorIcon(inputField) {
  const formControl = inputField.parentElement;
  formControl.classList.add("error");
}

function removeErrorIcon(inputField) {
  const formControl = inputField.parentElement;
  formControl.classList.remove("error");
}

TPDirect.card.onUpdate(function (update) {
  // update.canGetPrime === true
  // --> you can call TPDirect.card.getPrime()
  if (update.canGetPrime) {
    document.getElementById("confirmBtn").disabled = false;
    // submitButton.removeAttribute('disabled')
  } else {
    document.getElementById("confirmBtn").disabled = true;
  }
  const cardNumberField = document.getElementById("card-number");
  const cardExpiryField = document.getElementById("card-expiration-date");
  const cardCCVField = document.getElementById("card-ccv");

  if (update.status.number === 2) {
    // card number incorrect
    removeSuccessIcon(cardNumberField);
    showErrorIcon(cardNumberField);
  } else if (update.status.number === 0) {
    // card number correct
    removeErrorIcon(cardNumberField);
    showSuccessIcon(cardNumberField);
  } else {
    removeSuccessIcon(cardNumberField);
    removeErrorIcon(cardNumberField);
  }

  if (update.status.expiry === 2) {
    removeSuccessIcon(cardExpiryField);
    showErrorIcon(cardExpiryField);
  } else if (update.status.expiry === 0) {
    removeErrorIcon(cardExpiryField);
    showSuccessIcon(cardExpiryField);
  } else {
    removeSuccessIcon(cardExpiryField);
    removeErrorIcon(cardExpiryField);
  }

  if (update.status.ccv === 2) {
    removeSuccessIcon(cardCCVField);
    showErrorIcon(cardCCVField);
  } else if (update.status.ccv === 0) {
    removeErrorIcon(cardCCVField);
    showSuccessIcon(cardCCVField);
  } else {
    removeSuccessIcon(cardCCVField);
    removeErrorIcon(cardCCVField);
  }
});

TPDirect.card.getTappayFieldsStatus();

// ====== get prime ======

// get Total Price
async function getTotalPrice() {
  try {
    const res = await fetch(`${window.origin}/api/booking`);
    const data = await res.json();
    const allBookings = data.data;
    let totalPrice = 0;
    if (!data.data) {
      return totalPrice;
    } else {
      allBookings.forEach((booking) => {
        totalPrice += booking.price;
      });
      return totalPrice;
    }
  } catch (err) {
    console.log(`fetch error : ${err}`);
  }
}

async function getBookingTrips() {
  try {
    const res = await fetch(`${window.origin}/api/booking`);
    const data = await res.json();
    const allBookings = data.data;
    const allTrips = [];
    if (!data.data) {
      return allTrips;
    } else {
      allBookings.forEach((booking) => {
        const trip = {};
        trip.attraction = booking.attraction;
        trip.date = booking.date;
        trip.time = booking.time;
        allTrips.push(trip);
      });
      return allTrips;
    }
  } catch (err) {
    console.log(`fetch error : ${err}`);
  }
}

//build HTTP request body
async function buildRequestBody(prime) {
  const request = {};
  const order = {
    price: await getTotalPrice(),
    trip: await getBookingTrips(),
  };
  const contact = {
    name: document.getElementById("bookingName").value,
    email: document.getElementById("bookingEmail").value,
    phone: document.getElementById("bookingPhone").value,
  };
  request.prime = prime;
  request.order = order;
  request.contact = contact;
  return request;
}

// send data to server
async function sendTransactionData(requestData) {
  const res = await fetch(`${window.origin}/api/orders`, {
    method: "POST",
    headers: new Headers({
      "Content-Type": "application/json",
    }),
    body: JSON.stringify(requestData),
  });
  const data = await res.json();
  const paymentStatus = data.data.payment.status;
  const orderNumber = data.data.number;

  if (paymentStatus !== 0) {
    alert("很抱歉，本筆交易失敗\n請確認填寫資料無誤後再試一次");
    return;
  }

  location.href = `/thankyou?number=${orderNumber}`;
}

// tappay onsubmit
function onSubmit(event) {
  event.preventDefault();

  // 取得 TapPay Fields 的 status
  const tappayStatus = TPDirect.card.getTappayFieldsStatus();

  // 確認是否可以 getPrime
  if (tappayStatus.canGetPrime === false) {
    alert("Something went wrong, transaction failed...");
    return;
  }

  // Get prime
  TPDirect.card.getPrime(async (result) => {
    if (result.status !== 0) {
      alert("Something went wrong, transaction failed...");
      return;
    }
    const prime = result.card.prime;
    console.log(prime);
    const requestBody = await buildRequestBody(prime);
    await sendTransactionData(requestBody);
  });
}

document.getElementById("confirmBtn").addEventListener("click", onSubmit);
