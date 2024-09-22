$(document).ready(function() {
    // Submit form via AJAX
    $('#addRawMaterialForm').on('submit', function(e) {
        e.preventDefault(); // Prevent the form from submitting normally

        // Collect the form data
        let materialData = {
            material_name: $('#material_name').val(),
            quantity: $('#quantity').val(),
            unit_price: $('#unit_price').val(),
            supplier_id: $('#supplier_id').val()
        };

        // Make the AJAX request
        $.ajax({
            type: 'POST',
            url: 'http://localhost:5000/api/v1/raw_materials',  // Adjust the endpoint URL as needed
            contentType: 'application/json',
            data: JSON.stringify(materialData),
            success: function(response) {
                // Handle success response
                alert('Raw material added successfully!');
                // Optionally, reset the form
                $('#addRawMaterialForm')[0].reset();
            },
            error: function(xhr, status, error) {
                // Handle error response
                console.error('Error adding raw material:', error);
                alert('There was an error adding the raw material.');
            }
        });
    });
});
