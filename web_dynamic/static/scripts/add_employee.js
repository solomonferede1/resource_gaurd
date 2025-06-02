/* Global jQuery handler */

$(document).ready(function () {
  // Initialize department and role defaults if needed
  $('select[name="department"]').val("Production");

  $("form").on("submit", function (event) {
    event.preventDefault();

    // Form validation
    let isValid = true;
    let errorMessage = "";

    // Required fields validation (according to model)
    const requiredFields = ["first_name", "last_name", "phone"];
    requiredFields.forEach((field) => {
      const input = $(`[name="${field}"]`);
      if (!input.val().trim()) {
        isValid = false;
        errorMessage += `${field.replace("_", " ")} is required.\n`;
        input.addClass("is-invalid");
      } else {
        input.removeClass("is-invalid");
      }
    });

    // Password validation (if you're using it)
    const password = $('input[placeholder="Password"]').val();
    const confirmPassword = $('input[placeholder="Confirm Password"]').val();

    if (password || confirmPassword) {
      if (password !== confirmPassword) {
        isValid = false;
        errorMessage += "Passwords do not match!\n";
        $('input[placeholder="Confirm Password"]').addClass("is-invalid");
      } else {
        $('input[placeholder="Confirm Password"]').removeClass("is-invalid");
      }
    }

    if (!isValid) {
      alert(errorMessage);
      return false;
    }

    // Gather form data - include all fields from model
    const employeeData = {
      // Required fields
      first_name: $('input[placeholder="First Name"]').val().trim(),
      last_name: $('input[placeholder="Last Name"]').val().trim(),
      phone: $('input[placeholder="Phone"]').val().trim(),

      // Optional fields (with defaults if empty)
      email: $('input[placeholder="Email"]').val().trim() || null,
      department: $('select[name="department"]').val() || "Production",
      gender: $('select[name="gender"]').val() || null,
      salary: parseFloat($('input[placeholder="salary"]').val()) || null,
      status: "active", // Default value
    };

    // Include employee type if present (maps to role)
    const employeeType = $('input[name="employeeType"]:checked').val();
    if (employeeType) {
      employeeData.role = employeeType;
    }

    // Optional: Include password if your API handles it
    if (password) {
      employeeData.password = password;
    }

    // Remove any null or undefined values to let backend use its defaults
    Object.keys(employeeData).forEach((key) => {
      if (employeeData[key] === null || employeeData[key] === undefined) {
        delete employeeData[key];
      }
    });

    // Show loading state
    const submitBtn = $(this).find('button[type="submit"]');
    const originalBtnText = submitBtn.text();
    submitBtn
      .prop("disabled", true)
      .html(
        '<span class="spinner-border spinner-border-sm mr-2"></span> Processing...'
      );

    // Make AJAX request
    $.ajax({
      url: "http://localhost:5000/api/v1/employees",
      type: "POST",
      contentType: "application/json",
      dataType: "json",
      data: JSON.stringify(employeeData),
      success: function (response) {
        // Show success message
        alert("Employee created successfully!");

        // Redirect to employees page
        window.location.href = "http://localhost:5050/employees";
      },
      error: function (xhr, status, error) {
        // Show detailed error message
        let errorMsg = "Error creating employee: ";

        if (xhr.responseJSON && xhr.responseJSON.description) {
          errorMsg += xhr.responseJSON.description;
        } else if (xhr.responseJSON && xhr.responseJSON.message) {
          errorMsg += xhr.responseJSON.message;
        } else {
          errorMsg += "Unknown error occurred. Please try again.";
        }

        alert(errorMsg);

        // Reset button state
        submitBtn.prop("disabled", false).text(originalBtnText);
      },
    });
  });

  // Optional: Real-time validation
  $("input").on("blur", function () {
    const field = $(this).attr("name");
    if (requiredFields.includes(field) && !$(this).val().trim()) {
      $(this).addClass("is-invalid");
    } else {
      $(this).removeClass("is-invalid");
    }
  });
});
