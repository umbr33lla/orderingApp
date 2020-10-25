// Store
// To Add order to customer

let updateBtns = document.getElementsByClassName("update-cart");

for (let i = 0; i < updateBtns.length; i++) {
  updateBtns[i].addEventListener("click", function () {
    let productId = this.dataset.product;
    let action = this.dataset.action;
    let customerQs = document.getElementById("customers");
    let customer = customerQs.options[customerQs.selectedIndex].value;
    updateUserOrder(productId, action, customer);
  });
}

function updateUserOrder(productId, action, customer) {
  let data = {
    productId: productId,
    action: action,
    customer: customer,
  };

  fetch("/update_item/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": getCookie("csrftoken"),
    },
    body: JSON.stringify(data),
  })
    .then((response) => {
      return response.json();
    })
    .then((data) => {});
}

// Cart
// To update order order item

let updateOderItem = document.getElementsByClassName("update-item");

for (let i = 0; i < updateOderItem.length; i++) {
  updateOderItem[i].addEventListener("click", function () {
    let productId = this.dataset.product;
    let action = this.dataset.action;
    debugger;
    updateUserOrderItem(productId, action);
  });
}

function updateUserOrderItem(productId, action) {
  const customer = document.getElementById("customerName").value;

  let data = {
    productId: productId,
    action: action,
    customer: customer,
  };

  fetch("/update_item/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": getCookie("csrftoken"),
    },
    body: JSON.stringify(data),
  })
    .then((response) => {
      return response.json();
    })
    .then((data) => {
      location.reload();
    });
}

function getCookie(name) {
  var cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    var cookies = document.cookie.split(";");
    for (var i = 0; i < cookies.length; i++) {
      var cookie = cookies[i].trim();
      // Does this cookie string begin with the name we want?
      if (cookie.substring(0, name.length + 1) === name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

document.getElementById("cart-icon").addEventListener("click", function () {
  let customerQs = document.getElementById("customers");
  let customerId = customerQs.options[customerQs.selectedIndex].value;
  location.href = "/cart" + "/" + customerId;
});

// Process Orders
