$(document).ready(function() {
    // Hide product details initially
    $('#productDetails').hide();

    // Show product details when category is selected
    $('#category').on('change', function() {
        let categoryId = $(this).val();
        
        if (categoryId) {
            // If a category is selected, show the product details form
            $('#productDetails').fadeIn();
        }
    });

    // Handle form submission using AJAX
    $('#productForm').on('submit', function(e) {
        e.preventDefault();
        
        let productData = {
            category_id: $('#category').val(),
            product_name: $('#productName').val(),
            quantity: $('#quantity').val(),
            price: $('#unitPrice').val(),
            production_date: $('#productionDate').val(),
            product_type: $('#productType').val()
        };

        $.ajax({
            type: 'POST',
            url: 'http://localhost:5000/api/v1/products', // Adjust the URL to your API endpoint
            contentType: 'application/json',
            data: JSON.stringify(productData),
            success: function(response) {
                alert('Product added successfully!');
                // Optionally, you can reset the form or redirect the user
                $('#productForm')[0].reset();
                $('#productDetails').hide();
            },
            error: function(xhr, status, error) {
                console.error('Error adding product:', error);
                alert('There was an error adding the product. Please try again.');
            }
        });
    });
});
