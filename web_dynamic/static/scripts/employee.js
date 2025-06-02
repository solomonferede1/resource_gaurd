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
    url.searchParams.set("page", "1"); // Ensure page is set as string
    url.searchParams.set("search", search);
    url.searchParams.set("department", department);

    window.location.href = url.toString();
  }

  if (searchInput) {
    searchInput.addEventListener("input", () => debounce(applyFilters, 500));
  }
  if (departmentFilter) {
    departmentFilter.addEventListener("change", applyFilters);
  }

  // Initialize delete confirmation handler
  const confirmDeleteBtn = document.getElementById("confirmDeleteBtn");
  if (confirmDeleteBtn) {
    confirmDeleteBtn.addEventListener("click", function () {
      handleEmployeeDelete();
    });
  }
});

// View Employee Modal
function viewEmployee(id) {
  fetch(`${API_BASE_URL}/api/v1/employees/${id}`)
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
                                         data.status
                                       }">
                                        ${
                                          data.status.charAt(0).toUpperCase() +
                                          data.status.slice(1)
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

      const viewEmployeeContentElement = document.getElementById(
        "viewEmployeeContent"
      );
      if (viewEmployeeContentElement) {
        viewEmployeeContentElement.innerHTML = modalContent;
      }

      const modalElement = document.getElementById("viewEmployeeModal");
      if (modalElement) {
        const modal = new bootstrap.Modal(modalElement);
        modal.show();
      }
    })
    .catch((error) => {
      console.error("Error:", error);
      showNotification("Failed to load employee details", "error");
    });
}

// Delete Employee Functionality
let currentEmployeeToDelete = null;
let isDeleting = false; // Flag to prevent multiple delete clicks

function confirmDelete(id) {
  currentEmployeeToDelete = id;
  const modalElement = document.getElementById("confirmDeleteModal");
  if (modalElement) {
    const modal = new bootstrap.Modal(modalElement);
    modal.show();
  }
}

async function handleEmployeeDelete() {
  if (!currentEmployeeToDelete || isDeleting) return;

  isDeleting = true;
  const confirmDeleteBtn = document.getElementById("confirmDeleteBtn");
  const originalText = confirmDeleteBtn
    ? confirmDeleteBtn.textContent
    : "Delete";

  try {
    // Update button state to show loading
    if (confirmDeleteBtn) {
      confirmDeleteBtn.disabled = true;
      confirmDeleteBtn.innerHTML =
        '<span class="spinner-border spinner-border-sm me-2" role="status"></span>Deleting...';
    }

    // Show loading state on the employee row
    const employeeRow = document.querySelector(
      `tr[data-employee-id="${currentEmployeeToDelete}"]`
    );
    if (employeeRow) {
      employeeRow.style.opacity = "0.5";
      employeeRow.style.pointerEvents = "none"; // Disable interactions
    }

    const response = await fetch(
      `${API_BASE_URL}/api/v1/employees/${currentEmployeeToDelete}`,
      {
        method: "DELETE",
        headers: {
          "Content-Type": "application/json",
        },
      }
    );

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(
        errorData.message || `HTTP error! status: ${response.status}`
      );
    }

    const result = await response.json();
    if (result.success === false) {
      throw new Error(result.message || "Delete operation failed on server.");
    }

    showNotification("Employee deleted successfully", "success");

    await removeEmployeeRowWithConfirmation(currentEmployeeToDelete);

    const modalElement = document.getElementById("confirmDeleteModal");
    if (modalElement) {
      const modalInstance = bootstrap.Modal.getInstance(modalElement);
      if (modalInstance) {
        modalInstance.hide();
      }
    }

    await refreshEmployeeListIfNeeded();
  } catch (error) {
    console.error("Error deleting employee:", error);

    const employeeRow = document.querySelector(
      `tr[data-employee-id="${currentEmployeeToDelete}"]`
    );
    if (employeeRow) {
      employeeRow.style.opacity = "1";
      employeeRow.style.pointerEvents = "auto";
    }

    showNotification(
      error.message || "Failed to delete employee. Please try again.",
      "error"
    );
  } finally {
    if (confirmDeleteBtn) {
      confirmDeleteBtn.disabled = false;
      confirmDeleteBtn.textContent = originalText;
    }

    isDeleting = false;
    currentEmployeeToDelete = null;
  }
}

async function removeEmployeeRowWithConfirmation(employeeId) {
  return new Promise((resolve) => {
    const row = document.querySelector(`tr[data-employee-id="${employeeId}"]`);
    if (row) {
      row.classList.add("fade-out");
      setTimeout(() => {
        if (row.parentNode) {
          row.remove();
        }
        resolve();
      }, 300);
    } else {
      resolve();
    }
  });
}

async function refreshEmployeeListIfNeeded() {
  const employeeRows = document.querySelectorAll("tbody tr[data-employee-id]");

  if (employeeRows.length === 0) {
    const url = new URL(window.location.href);
    const currentPage = parseInt(url.searchParams.get("page") || "1");

    if (currentPage > 1) {
      url.searchParams.set("page", (currentPage - 1).toString());
      window.location.href = url.toString();
    } else {
      window.location.reload();
    }
  }
  window.location.reload();
}

// Edit Employee Functionality
async function editEmployee(id) {
  try {
    const response = await fetch(`${API_BASE_URL}/api/v1/employees/${id}`);
    if (!response.ok) throw new Error("Failed to fetch employee");
    const employee = await response.json();

    const formResponse = await fetch("/get_edit_form");
    if (!formResponse.ok) throw new Error("Failed to load form");
    const formHtml = await formResponse.text();

    const container = document.getElementById("editEmployeeFormContainer");
    if (!container) throw new Error("Edit form container not found");

    container.innerHTML = formHtml;
    populateForm(employee);

    const modalElement = document.getElementById("editEmployeeModal");
    if (modalElement) {
      const modal = new bootstrap.Modal(modalElement);
      modal.show();
    }

    const editForm = document.getElementById("editEmployeeForm");
    if (editForm) {
      const newForm = editForm.cloneNode(true);
      editForm.parentNode.replaceChild(newForm, editForm);

      newForm.addEventListener("submit", async (e) => {
        e.preventDefault();
        await updateEmployee(id);
      });
    }
  } catch (error) {
    console.error("Error:", error);
    showNotification("Failed to load employee data", "error");
  }
}

function populateForm(employee) {
  const form = document.getElementById("editEmployeeForm");
  if (!form) return;

  // Populate standard text/number/select inputs
  for (const [key, value] of Object.entries(employee)) {
    // Skip radio buttons and checkboxes here, they are handled separately
    const input = form.querySelector(`[name="${key}"]`);
    if (input && input.type !== "radio" && input.type !== "checkbox") {
      input.value = value !== null && value !== undefined ? String(value) : "";
    }
  }

  // Special handling for gender radio buttons
  if (employee.gender) {
    const genderRadios = form.querySelectorAll('input[name="gender"]');
    genderRadios.forEach((radio) => {
      if (
        radio instanceof HTMLInputElement &&
        radio.value === employee.gender
      ) {
        radio.checked = true;
      }
    });
  }

  // *** MODIFIED: Special handling for 'status' radio buttons ***
  if (employee.status) {
    const statusRadios = form.querySelectorAll('input[name="status"]');
    statusRadios.forEach((radio) => {
      if (
        radio instanceof HTMLInputElement &&
        radio.value === employee.status
      ) {
        radio.checked = true;
      }
    });
  }

  // Special handling for date fields
  if (employee.date_hired) {
    const dateInput = form.querySelector("#date_hired");
    if (dateInput instanceof HTMLInputElement && dateInput.type === "date") {
      const date = new Date(employee.date_hired);
      dateInput.value = date.toISOString().split("T")[0];
    }
  }
}

async function updateEmployee(id) {
  const saveChangesBtn = document.querySelector(
    "#editEmployeeForm .btn-orange"
  );
  const originalBtnText = saveChangesBtn
    ? saveChangesBtn.textContent
    : "Save Changes";

  try {
    const form = document.getElementById("editEmployeeForm");
    if (!form) throw new Error("Edit form not found");

    if (saveChangesBtn) {
      saveChangesBtn.disabled = true;
      saveChangesBtn.innerHTML =
        '<span class="spinner-border spinner-border-sm me-2" role="status"></span>Saving...';
    }

    const formData = new FormData(form);
    const data = Object.fromEntries(formData.entries());

    // *** MODIFIED: 'status' is now directly from the radio buttons, no conversion needed ***
    // The 'status' field will be present in 'data' if a radio button is selected.
    // If no status is selected (e.g., form validation issue), you might want a default.
    // For now, assuming 'status' will always be 'active' or 'inactive' from the form.

    // Convert salary to number
    if (data.salary) {
      data.salary = parseFloat(data.salary);
    }

    const response = await fetch(`${API_BASE_URL}/api/v1/employees/${id}`, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(
        errorData.message || `HTTP error! status: ${response.status}`
      );
    }

    const updatedEmployee = await response.json();

    showNotification("Employee updated successfully", "success");

    // Update the table row with the fresh data from the server
    updateEmployeeRow(id, updatedEmployee);

    const modalElement = document.getElementById("editEmployeeModal");
    if (modalElement) {
      const modalInstance = bootstrap.Modal.getInstance(modalElement);
      if (modalInstance) {
        modalInstance.hide();
      }
    }
  } catch (error) {
    console.error("Error:", error);
    showNotification(error.message || "Failed to update employee", "error");
  } finally {
    if (saveChangesBtn) {
      saveChangesBtn.disabled = false;
      saveChangesBtn.textContent = originalBtnText;
    }
  }
}

function updateEmployeeRow(id, employee) {
  const row = document.querySelector(`tr[data-employee-id="${id}"]`);
  if (!row) return;

  row.classList.add("updated-row");
  setTimeout(() => row.classList.remove("updated-row"), 1500);

  const cells = row.cells;
  if (cells.length >= 8) {
    cells[1].textContent = `${employee.first_name} ${employee.last_name}`;
    cells[2].innerHTML =
      employee.gender === "Male"
        ? '<i class="fas fa-mars" style="color: #3498db;"></i> Male'
        : '<i class="fas fa-venus" style="color: #e83e8c;"></i> Female';
    cells[3].textContent = employee.role;
    cells[4].textContent = employee.department;
    cells[5].textContent = `ETB ${(employee.salary || 0).toLocaleString(
      "en-US",
      { minimumFractionDigits: 2, maximumFractionDigits: 2 }
    )}`;
    cells[6].textContent = employee.date_hired
      ? new Date(employee.date_hired).toLocaleDateString("en-US", {
          day: "numeric",
          month: "short",
          year: "numeric",
        })
      : "N/A";
    // Use employee.status directly for display
    cells[7].innerHTML = `<span class="status-badge status-${employee.status}">
          ${employee.status.charAt(0).toUpperCase() + employee.status.slice(1)}
      </span>`;
  }
}

// Notification function
function showNotification(message, type = "success") {
  const notification = document.getElementById("notification");
  if (!notification) return;

  const alertClass = type === "success" ? "alert-success" : "alert-danger";
  const iconClass =
    type === "success" ? "fas fa-check-circle" : "fas fa-exclamation-triangle";

  notification.innerHTML = `
        <div class="alert ${alertClass} alert-dismissible fade show" role="alert">
            <i class="${iconClass} me-2"></i>
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
        </div>
    `;

  setTimeout(() => {
    const alert = notification.querySelector(".alert");
    if (alert) {
      alert.classList.remove("show");
      setTimeout(() => {
        if (notification.innerHTML.includes(message)) {
          notification.innerHTML = "";
        }
      }, 150);
    }
  }, 5000);
}

window.addEventListener("unhandledrejection", (event) => {
  console.error("Unhandled promise rejection:", event.reason);
  if (
    event.reason instanceof TypeError &&
    event.reason.message === "Failed to fetch"
  ) {
    showNotification(
      "Network error occurred. Please check your connection.",
      "error"
    );
  } else if (event.reason && event.reason.message) {
    showNotification(
      `An unexpected error occurred: ${event.reason.message}`,
      "error"
    );
  } else {
    showNotification("An unexpected error occurred.", "error");
  }
});
