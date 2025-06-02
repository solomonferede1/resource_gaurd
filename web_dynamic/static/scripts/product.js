$(".category-option").on("click", function (e) {
  e.preventDefault();
  const categoryId = $(this).data("id");

  $.ajax({
    url: "/filter_products_by_category",
    method: "GET",
    data: { category_id: categoryId },
    success: function (data) {
      $("#productTableBody").html("");
      data.products.forEach((product) => {
        $("#productTableBody").append(`
                      <tr>
                          <td>${product.id}</td>
                          <td>${product.product_name}</td>
                          <td>${product.product_type}</td>
                          <td>${product.quantity}</td>
                          <td>${product.price}</td>
                          <td>${product.production_date}</td>
                          <td>${product.status || "Present"}</td>
                      </tr>
                  `);
      });
    },
    error: function () {
      alert("Failed to fetch products.");
    },
  });
});
