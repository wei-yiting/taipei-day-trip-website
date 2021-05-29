const models = {
  getUserData: async function () {
    try {
      const res = await fetch("/api/user");
      const data = await res.json();
      const userData = data.data;
      return userData;
    } catch (err) {
      console.log(`fetch error : ${err}`);
    }
  },
  getOrderData: async () => {
    const orderNum = location.href.split("=").pop();
    try {
      const res = await fetch(`/api/orders/${orderNum}`);
      const data = await res.json();
      return data.data;
    } catch (err) {
      console.log(`fetch error : ${err}`);
    }
  },
};

const views = {
  renderLogIn: (data) => {
    if (!data) {
      location.href = "/";
    } else {
      document.getElementById("main").classList.remove("hide-before-log-in");
    }
  },
};

const controllers = {};

getOrderInfo();
