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
        let this_value = $(this)
        let index = this_value.attr("data-index");
        
        let quantity = $(".product-quantity-"+index).val();
        let product_id = $(".product-id-"+index).val();
        let product_title = $(".product-title-"+index).val();
        let product_price = $(".current-price-"+index).text();
        let product_pid = $(".product-pid-"+index).val();
        let product_image = $(".product-image-"+index).val();

        let url = $(this).attr('data-url');

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
                "id": product_id,
                "title": product_title,
                "pid": product_pid,
                "image": product_image,

                "qty": quantity,
                "price": product_price,
            },
            dataType: "json",
            beforesend: function () {
                console.log("adding to cart.....");
            },
            success: function (response) {
                console.log("added to cart successfully");
                swal(response.message, "", response.status);
                console.log(response);
                $(".cart-items-count").text(response.totalcartitems);
                this_value.text("✓ Added");
                this_value.attr("disabled", true);
            },
            error: function (response) {
                console.log("error adding to cart");
                console.log(response);
            }
        })
        })
})