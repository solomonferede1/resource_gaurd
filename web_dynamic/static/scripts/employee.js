document.addEventListener("DOMContentLoaded", function () {
  // Search functionality
  const searchInput = document.getElementById("employeeSearch");
  const departmentFilter = document.getElementById("departmentFilter");

  // Debounce function to prevent rapid firing of search
  let debounceTimer;
  function debounce(callback, delay) {
    clearTimeout(debounceTimer);
    debounceTimer = setTimeout(callback, delay);
  }

  function applyFilters() {
    const search = searchInput.value;
    const department = departmentFilter.value;
    const url = new URL(window.location.href);

    // Reset to first page when filters change
    url.searchParams.set("page", 1);
    url.searchParams.set("search", search);
    url.searchParams.set("department", department);

    window.location.href = url.toString();
  }

  searchInput.addEventListener("input", () => debounce(applyFilters, 500));
  departmentFilter.addEventListener("change", applyFilters);
});

// View Employee Modal
function viewEmployee(id) {
  fetch(`/api/v1/employees/${id}`)
    .then((response) => {
      if (!response.ok) throw new Error("Failed to fetch employee");
      return response.json();
    })
    .then((data) => {
      const modalContent = `
                <div class="modal-header">
                    <h5 class="modal-title">Employee Details</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body">
                    <div class="row">
                        <div class="col-md-4 text-center">
                            <div class="employee-avatar-lg mb-3">
                                ${
                                  data.photo
                                    ? `<img src="/static/uploads/${data.photo}" alt="${data.first_name}" class="img-thumbnail">`
                                    : `<div class="avatar-placeholder">${data.first_name[0]}${data.last_name[0]}</div>`
                                }
                            </div>
                            <h4>${data.first_name} ${data.last_name}</h4>
                            <p class="text-muted">${data.role}</p>
                        </div>
                        <div class="col-md-8">
                            <div class="row mb-3">
                                <div class="col-md-6">
                                    <p><strong>Employee ID:</strong> ${
                                      data.id
                                    }</p>
                                    <p><strong>Department:</strong> ${
                                      data.department
                                    }</p>
                                    <p><strong>Hire Date:</strong> ${
                                      data.date_hired
                                        ? new Date(
                                            data.date_hired
                                          ).toLocaleDateString()
                                        : "N/A"
                                    }</p>
                                </div>
                                <div class="col-md-6">
                                    <p><strong>Email:</strong> ${
                                      data.email || "N/A"
                                    }</p>
                                    <p><strong>Phone:</strong> ${
                                      data.phone || "N/A"
                                    }</p>
                                    <p><strong>Salary:</strong> ETB ${
                                      data.salary
                                        ? data.salary.toLocaleString("en-US", {
                                            minimumFractionDigits: 2,
                                            maximumFractionDigits: 2,
                                          })
                                        : "0.00"
                                    }</p>
                                </div>
                            </div>
                            <hr>
                            <div class="row">
                                <div class="col-12">
                                    <h5>Additional Information</h5>
                                    <p><strong>Status:</strong> 
                                        <span class="status-badge status-${
                                          data.is_active ? "active" : "inactive"
                                        }">
                                            ${
                                              data.is_active
                                                ? "Active"
                                                : "Inactive"
                                            }
                                        </span>
                                    </p>
                                    <p><strong>Gender:</strong> ${
                                      data.gender || "N/A"
                                    }</p>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                </div>
            `;

      document.getElementById("viewEmployeeContent").innerHTML = modalContent;
      const modal = new bootstrap.Modal(
        document.getElementById("viewEmployeeModal")
      );
      modal.show();
    })
    .catch((error) => {
      console.error("Error:", error);
      showNotification("Failed to load employee details", "error");
    });
}

// Delete Employee Functionality
let currentEmployeeToDelete = null;

function confirmDelete(id) {
  currentEmployeeToDelete = id;
  const modal = new bootstrap.Modal(
    document.getElementById("confirmDeleteModal")
  );
  modal.show();
}

document
  .getElementById("confirmDeleteBtn")
  .addEventListener("click", function () {
    if (!currentEmployeeToDelete) return;

    fetch(`/api/v1/employees/${currentEmployeeToDelete}`, {
      method: "DELETE",
    })
      .then((response) => {
        if (!response.ok) throw new Error("Failed to delete employee");
        return response.json();
      })
      .then(() => {
        showNotification("Employee deleted successfully", "success");
        removeEmployeeRow(currentEmployeeToDelete);
        bootstrap.Modal.getInstance(
          document.getElementById("confirmDeleteModal")
        ).hide();
      })
      .catch((error) => {
        console.error("Error:", error);
        showNotification("Failed to delete employee", "error");
      })
      .finally(() => {
        currentEmployeeToDelete = null;
      });
  });

function removeEmployeeRow(employeeId) {
  const row = document.querySelector(`tr[data-employee-id="${employeeId}"]`);
  if (row) {
    row.classList.add("fade-out");
    setTimeout(() => row.remove(), 300);
  }
}

// Edit Employee Functionality
async function editEmployee(id) {
  try {
    // Fetch employee data
    const response = await fetch(`/api/v1/employees/${id}`);
    if (!response.ok) throw new Error("Failed to fetch employee");
    const employee = await response.json();

    // Load edit form template
    const formResponse = await fetch("/get_edit_form");
    if (!formResponse.ok) throw new Error("Failed to load form");
    const formHtml = await formResponse.text();

    // Populate form with employee data
    const container = document.getElementById("editEmployeeFormContainer");
    container.innerHTML = formHtml;
    populateForm(employee);

    // Initialize modal
    const modal = new bootstrap.Modal(
      document.getElementById("editEmployeeModal")
    );
    modal.show();

    // Setup form submission
    document
      .getElementById("editEmployeeForm")
      .addEventListener("submit", async (e) => {
        e.preventDefault();
        await updateEmployee(id);
      });
  } catch (error) {
    console.error("Error:", error);
    showNotification("Failed to load employee data", "error");
  }
}

function populateForm(employee) {
  const form = document.getElementById("editEmployeeForm");
  for (const [key, value] of Object.entries(employee)) {
    const input = form.querySelector(`[name="${key}"]`);
    if (input) {
      if (input.type === "checkbox") {
        input.checked = value;
      } else if (input.type === "radio") {
        if (input.value === value) {
          input.checked = true;
        }
      } else {
        input.value = value !== null ? value : "";
      }
    }
  }

  // Special handling for date fields
  if (employee.date_hired) {
    const dateInput = form.querySelector("#date_hired");
    if (dateInput) {
      const date = new Date(employee.date_hired);
      dateInput.value = date.toISOString().split("T")[0];
    }
  }
}

async function updateEmployee(id) {
  try {
    const form = document.getElementById("editEmployeeForm");
    const formData = new FormData(form);
    const data = Object.fromEntries(formData.entries());

    // Convert is_active to boolean
    data.is_active = data.is_active === "on";

    const response = await fetch(`/api/v1/employees/${id}`, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
    });

    if (!response.ok) throw new Error("Failed to update employee");

    const updatedEmployee = await response.json();

    // Show success notification
    showNotification("Employee updated successfully", "success");

    // Update the table row
    updateEmployeeRow(id, updatedEmployee);

    // Close modal
    bootstrap.Modal.getInstance(
      document.getElementById("editEmployeeModal")
    ).hide();
  } catch (error) {
    console.error("Error:", error);
    showNotification("Failed to update employee", "error");
  }
}

function updateEmployeeRow(id, employee) {
  const row = document.querySelector(`tr[data-employee-id="${id}"]`);
  if (!row) return;

  // Highlight the updated row
  row.classList.add("updated-row");
  setTimeout(() => row.classList.remove("updated-row"), 1500);

  // Update each cell with new data
  row.cells[1].textContent = `${employee.first_name} ${employee.last_name}`;
  row.cells[2].innerHTML =
    employee.gender === "Male"
      ? '<i class="fas fa-mars" style="color: #3498db;"></i> Male'
      : '<i class="fas fa-venus" style="color: #e83e8c;"></i> Female';
  row.cells[3].textContent = employee.role;
  row.cells[4].textContent = employee.department;
  row.cells[5].textContent = `ETB ${(employee.salary || 0).toLocaleString(
    "en-US",
    { minimumFractionDigits: 2, maximumFractionDigits: 2 }
  )}`;
  row.cells[6].textContent = employee.date_hired
    ? new Date(employee.date_hired).toLocaleDateString("en-US", {
        day: "numeric",
        month: "short",
        year: "numeric",
      })
    : "N/A";
  row.cells[7].innerHTML = `<span class="status-badge status-${
    employee.is_active ? "active" : "inactive"
  }">
        ${employee.is_active ? "Active" : "Inactive"}
    </span>`;
}

// Notification function
function showNotification(message, type = "success") {
  const notification = document.getElementById("notification");
  const alertClass = type === "success" ? "alert-success" : "alert-danger";

  notification.innerHTML = `
        <div class="alert ${alertClass} alert-dismissible fade show" role="alert">
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
        </div>
    `;

  // Auto-remove after 5 seconds
  setTimeout(() => {
    const alert = notification.querySelector(".alert");
    if (alert) {
      alert.classList.remove("show");
      setTimeout(() => (notification.innerHTML = ""), 150);
    }
  }, 5000);
}
