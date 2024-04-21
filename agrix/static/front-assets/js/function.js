// TODO: WORK ON PRODUCT FILTERING

// $(document).ready(function () {
//   $(".filter-checkbox").click(function () {
//     console.log("clicked");
//     let filter_object = {};

//     $(".filter-checkbox").each(function () {
//       let filter_value = $(this).val();
//       let filter_key = $(this).data("filter");
//       // console.log("Filter key is: ",filter_key);
//       // console.log("Filter Value is: ",filter_value);

//       filter_object[filter_key] = Array.from($("input[data-filter=" + filter_key + "]:checked")).map(function (element) {return element.value});
//     });
//     console.log("Filter Object is: ", filter_object);

//     $.ajax({
//         url: "/filter-product",
//         data: filter_object,
//         dataType: "json",
//         beforesend: function () {
//           console.log("filtering products.....");
//         },
//         success: function (response) {
//           console.log("filtered products successfully");
//           console.log(response);
//         //   $("#products").html(data["products"]);
//         }
//     })
//   });
// });
$(document).ready(function () {
  $(".add-to-cart-btn").click(function () {
    let this_value = $(this);
    let index = this_value.attr("data-index");

    let quantity = $(".product-quantity-" + index).val();
    let product_id = $(".product-id-" + index).val();
    let product_title = $(".product-title-" + index).val();
    let product_price = $(".current-price-" + index).text();
    let product_pid = $(".product-pid-" + index).val();
    let product_image = $(".product-image-" + index).val();

    let url = $(this).attr("data-url");

    // console.log("This value is: ", this_value);
    // console.log("Product id is: ", product_id);
    // console.log("Quantity is: ", quantity);
    // console.log("Product title is: ", product_title);
    // console.log("Product price is: ", product_price);
    // console.log("Url is: ", url);
    // console.log("Product pid is: ", product_pid);
    // console.log("Product image is: ", product_image);
    // console.log("Index is: ", index);

    $.ajax({
      url: url,
      data: {
        id: product_id,
        title: product_title,
        pid: product_pid,
        image: product_image,

        qty: quantity,
        price: product_price,
      },
      dataType: "json",
      beforesend: function () {
        console.log("adding to cart.....");
      },
      success: function (response) {
        console.log("added to cart successfully");
        Swal.fire({
          text: response.message,
          icon: response.status, // Assuming response.status contains the icon type
        });
        console.log(response);
        $(".cart-items-count").text(response.totalcartitems);
        this_value.text("✓ Added");
        this_value.attr("disabled", true);
      },
      error: function (response) {
        console.log("error adding to cart");
        console.log(response);
        Swal.fire({
          text: "Error adding to cart",
          icon: "error",
        });
      },
    });
  });

  // Increase Cart Quantity Function
  $(".qty-up").click(function () {
    let product_id = $(this).attr("data-id");
    let url = $(this).attr("data-url");

    // Update the quantity display in the cart table immediately
    let quantityElement = $(`.qty-val`);
    let currentQuantity = parseInt(quantityElement.text());
    let newQuantity = currentQuantity + 1;
    quantityElement.text(newQuantity);

    // Send AJAX request to update quantity on the server
    $.ajax({
      url: url,
      method: "POST",
      headers: { "X-CSRFToken": getCookie("csrftoken") }, // Include the CSRF token in the headers
      data: {
        id: product_id,
        quantity: newQuantity,
      },
      dataType: "json",
      success: function (response) {
        console.log("Quantity increased successfully");
        console.log(response);
        $(".cart-items-count").text(response.totalcartitems);
        // Update the subtotal
        let priceElement = $(`.price-${product_id}`);
        let price = parseFloat(priceElement.attr("data-price"));
        let subtotal = price * newQuantity;
        priceElement.find("h4").text(`Kes ${subtotal.toFixed(2)}`);
      },
      error: function (response) {
        console.log("Error increasing quantity");
        console.log(response);
        // Revert the quantity display in case of error
        quantityElement.text(currentQuantity);
      },
    });
  });

  // Increase Cart Quantity Function
  $(".qty-down").click(function () {
    let product_id = $(this).attr("data-id");
    let url = $(this).attr("data-url");

    let quantityElement = $(`.qty-val`);
    let currentQuantity = parseInt(quantityElement.text());
    let newQuantity = currentQuantity - 1;

    if (newQuantity > 0) {
      // Decrease the quantity
      quantityElement.text(newQuantity);

      // Send AJAX request to update quantity on the server
      $.ajax({
        url: url,
        method: "POST",
        headers: { "X-CSRFToken": getCookie("csrftoken") },
        data: {
          id: product_id,
          quantity: newQuantity,
        },
        dataType: "json",
        success: function (response) {
          console.log("Quantity decreased successfully");
          console.log(response);
          $(".cart-items-count").text(response.totalcartitems);
          let priceElement = $(`.price-${product_id}`);
          let price = parseFloat(priceElement.attr("data-price"));
          let subtotal = price * newQuantity;
          priceElement.find("h4").text(`Kes ${subtotal.toFixed(2)}`);
        },
        error: function (response) {
          console.log("Error decreasing quantity");
          Swal.fire({
            text: "Error decreasing quantity",
            icon: "error",
          });
          console.log(response);
          // Revert the quantity display in case of error
          quantityElement.text(currentQuantity);
        },
      });
    } else {
      // Show confirmation dialog for item removal
      Swal.fire({
        title: "Are you sure?",
        text: "You are about to remove this product from your cart.",
        icon: "warning",
        showCancelButton: true,
        confirmButtonColor: "#3085d6",
        cancelButtonColor: "#d33",
        confirmButtonText: "Yes, remove it!",
      }).then((result) => {
        if (result.isConfirmed) {
          // User confirmed, proceed with removal
          $.ajax({
            url: url,
            method: "POST",
            headers: { "X-CSRFToken": getCookie("csrftoken") },
            data: {
              id: product_id,
              quantity: newQuantity,
            },
            dataType: "json",
            success: function (response) {
              console.log("Product removed from cart successfully");
              $(`.cart-item-${product_id}`).remove();
              console.log(response);
              Swal.fire({
                text: "Item removed from cart successfully",
                icon: "success",
              });
              $(".cart-items-count").text(response.totalcartitems);
            },
            error: function (response) {
              console.log("Error removing product from cart");
              Swal.fire({
                text: "Error removing product from cart",
                icon: "error",
              });
              console.log(response);
            },
          });
        }
      });
    }
  });

  // Function to get the value of a cookie by name
  function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
      const cookies = document.cookie.split(";");
      for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        // Does this cookie string begin with the name we want?
        if (cookie.substring(0, name.length + 1) === name + "=") {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }

  $(".delete_cart").click(function (event) {
    event.preventDefault(); // Prevent the default anchor behavior
    let product_id = $(this).attr("data-id");
    let url = $(this).attr("data-url");
    let button = $(this); // Store a reference to the button

    // Show a confirmation dialog before proceeding
    Swal.fire({
      title: "Are you sure?",
      text: "You are about to remove this product from your cart.",
      icon: "warning",
      showCancelButton: true,
      confirmButtonColor: "#3085d6",
      cancelButtonColor: "#d33",
      confirmButtonText: "Yes, remove it!",
    }).then((result) => {
      if (result.isConfirmed) {
        // User confirmed, proceed with removal
        $.ajax({
          url: url,
          method: "POST",
          headers: { "X-CSRFToken": getCookie("csrftoken") },
          data: {
            id: product_id,
          },
          dataType: "json",
          beforeSend: function () {
            // Hide the delete button or show a loading indicator
            button.hide(); // Use the stored button reference to hide it
            console.log("Removing product from cart...");
          },
          success: function (response) {
            console.log(response);
            $(".cart-items-count").text(response.totalcartitems);
            console.log("Product removed from cart successfully");
            // Remove the row from the cart table
            $(`.cart-item-${product_id}`).remove();
            // Show the button again in case of success
            button.show();
          },
          error: function (xhr, status, error) {
            // Include the xhr parameter here
            console.log("Error removing product from cart");
            console.log(xhr);
            // Handle the error (e.g., show an error message)
            console.log("Error: " + xhr.responseJSON.message);
            // Show the button again in case of error
            button.show();
          },
        });
      }
    });
  });
});
