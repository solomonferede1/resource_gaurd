/* $ global */

$(document).ready(function() {
    $('form').on('submit', function(event) {
        event.preventDefault();

        // Gather form data
        const employeeData = {
            first_name: $('input[placeholder="First Name"]').val(),
            last_name: $('input[placeholder="Last Name"]').val(),
            email: $('input[placeholder="Email"]').val(),
            phone: $('input[placeholder="Phone"]').val(),
            role: $('input[placeholder="Role"]').val(),
            /*password: $('input[placeholder="Password"]').val(),
            confirm_password: $('input[placeholder="Confirm Password"]').val(),
            gender: $('select[required]').val(),*/
            age: $('input[placeholder="Age"]').val()
            //employeeType: $('input[name="employeeType"]:checked').val()
        };

        /* Validate form data
        if (employeeData.password !== employeeData.confirm_password) {
            alert("Passwords do not match!");
            return;
        }*/

        // Make AJAX request
        $.ajax({
            url: 'http://localhost:5000/api/v1/employees',
            type: 'POST',
            contentType: 'application/json',
            dataType: 'json',
            data: JSON.stringify(employeeData),
            success: function(response) {
                alert('Employee created successfully!');
                // Optionally, redirect or clear form fields here
            },
            error: function(xhr, status, error) {
                alert('Error: ' + (xhr.responseJSON.description || 'An error occurred.'));
            }
        });
    });
});
