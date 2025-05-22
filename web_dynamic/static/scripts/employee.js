document.addEventListener('DOMContentLoaded', function() {
    // Search functionality
    const searchInput = document.getElementById('employeeSearch');
    const departmentFilter = document.getElementById('departmentFilter');
    
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
        url.searchParams.set('page', 1);
        url.searchParams.set('search', search);
        url.searchParams.set('department', department);
        
        window.location.href = url.toString();
    }
    
    searchInput.addEventListener('input', () => debounce(applyFilters, 500));
    departmentFilter.addEventListener('change', applyFilters);
});


// View Employee Modal
function viewEmployee(id) {
    fetch(`${API_BASE_URL}/api/v1/employees/${id}`)
        .then(response => response.json())
        .then(data => {
            const modal = new bootstrap.Modal(document.getElementById('viewEmployeeModal'));

            const modalInnerContent = `
                <div class="modal-dialog modal-lg">
                    <div class="modal-content">
                        <div class="modal-header">
                            <h5 class="modal-title">Employee Details</h5>
                            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                        </div>
                        <div class="modal-body">
                            <div class="row">
                                <div class="col-md-4 text-center">
                                    <div class="employee-avatar-lg mb-3">
                                        ${data.photo ? 
                                            `<img src="/static/uploads/${data.photo}" alt="${data.first_name}">` : 
                                            `${data.first_name[0]}${data.last_name[0]}`}
                                    </div>
                                    <h4>${data.first_name} ${data.last_name}</h4>
                                    <p class="text-muted">${data.role}</p>
                                </div>
                                <div class="col-md-8">
                                    <div class="row mb-3">
                                        <div class="col-md-6">
                                            <p><strong>Employee ID:</strong> ${data.id}</p>
                                            <p><strong>Department:</strong> ${data.department}</p>
                                            <p><strong>Hire Date:</strong> ${new Date(data.date_hired).toLocaleDateString()}</p>
                                        </div>
                                        <div class="col-md-6">
                                            <p><strong>Email:</strong> ${data.email}</p>
                                            <p><strong>Phone:</strong> ${data.phone}</p>
                                            <p><strong>Salary:</strong> ETB ${data.salary ? data.salary.toLocaleString() : '0.00'}</p>
                                        </div>
                                    </div>
                                    <hr>
                                    <div class="row">
                                        <div class="col-12">
                                            <h5>Additional Information</h5>
                                            <p><strong>Status:</strong> 
                                                <span class="status-badge status-${data.is_active ? 'active' : 'inactive'}">
                                                    ${data.is_active ? 'Active' : 'Inactive'}
                                                </span>
                                            </p>
                                            <p><strong>Gender:</strong> ${data.gender}</p>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <div class="modal-footer">
                            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                        </div>
                    </div>
                </div>
            `;

            document.getElementById('viewEmployeeContent').innerHTML = modalInnerContent;
            modal.show();
        })
        .catch(error => console.error('Error:', error));
}

// Delete Employee Functionality
let currentEmployeeToDelete = null;

// Initialize modal
const deleteModal = new bootstrap.Modal('#deleteConfirmModal', {
    keyboard: false,
    focus: true
});

function confirmDelete(id) {
    currentEmployeeToDelete = id;
    
    // Remove aria-hidden before showing
    document.getElementById('deleteConfirmModal').removeAttribute('aria-hidden');
    deleteModal.show();
    
    // Set focus to delete button after showing
    setTimeout(() => {
        document.getElementById('confirmDeleteBtn').focus();
    }, 100);
}

// Handle delete confirmation
document.getElementById('confirmDeleteBtn').addEventListener('click', function() {
    if (!currentEmployeeToDelete) return;

    fetch(`${API_BASE_URL}/api/v1/employees/${currentEmployeeToDelete}`, {
        method: 'DELETE'
    })
    .then(response => {
        if (response.ok) {
            showDeleteSuccess();
            removeEmployeeRow(currentEmployeeToDelete);
        } else {
            throw new Error('Failed to delete employee');
        }
    })
    .catch(handleDeleteError)
    .finally(resetDeleteState);
});

function showDeleteSuccess() {
    const toast = new bootstrap.Toast('#deleteSuccessToast');
    toast.show();
}

function removeEmployeeRow(employeeId) {
    const row = document.querySelector(`tr[data-employee-id="${employeeId}"]`);
    if (row) {
        row.classList.add('fade-out');
        setTimeout(() => row.remove(), 300);
    }
}

function handleDeleteError(error) {
    console.error('Error:', error);
    alert('Failed to delete employee. Please try again.');
}

function resetDeleteState() {
    currentEmployeeToDelete = null;
    // Ensure modal is properly hidden
    document.getElementById('deleteConfirmModal').setAttribute('aria-hidden', 'true');
}

// Ensure proper cleanup when modal hides
document.getElementById('deleteConfirmModal').addEventListener('hidden.bs.modal', function() {
    resetDeleteState();
});

async function editEmployee(id) {
    try {
        // Fetch employee data
        const response = await fetch(`${API_BASE_URL}/api/v1/employees/${id}`);
        if (!response.ok) throw new Error('Failed to fetch employee');
        const employee = await response.json();

        // Load edit form template
        const formResponse = await fetch('/get_edit_form');
        const formHtml = await formResponse.text();
        
        // Populate form with employee data
        const container = document.getElementById('editEmployeeFormContainer');
        container.innerHTML = formHtml;
        populateForm(employee);

        // Initialize modal
        const modal = new bootstrap.Modal(document.getElementById('editEmployeeModal'));
        modal.show();

        // Setup form submission
        document.getElementById('editEmployeeForm').addEventListener('submit', async (e) => {
            e.preventDefault();
            await updateEmployee(id);
        });

    } catch (error) {
        console.error('Error:', error);
        alert('Failed to load employee data');
    }
}

function populateForm(employee) {
    const form = document.getElementById('editEmployeeForm');
    for (const [key, value] of Object.entries(employee)) {
        const input = form.querySelector(`[name="${key}"]`);
        if (input) {
            if (input.type === 'checkbox') {
                input.checked = value;
            } else {
                input.value = value;
            }
        }
    }
}

async function updateEmployee(id) {
    try {
        const form = document.getElementById('editEmployeeForm');
        const formData = new FormData(form);
        const data = Object.fromEntries(formData.entries());

        const response = await fetch(`${API_BASE_URL}/api/v1/employees/${id}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
        });

        if (!response.ok) throw new Error('Failed to update employee');

        const updatedEmployee = await response.json();
        
        // Show success toast
        const toast = new bootstrap.Toast(document.getElementById('editSuccessToast'));
        toast.show();

        // Update the table row
        updateEmployeeRow(id, updatedEmployee);

        // Close modal
        bootstrap.Modal.getInstance(document.getElementById('editEmployeeModal')).hide();

    } catch (error) {
        console.error('Error:', error);
        alert('Failed to update employee');
    }
}

function updateEmployeeRow(id, employee) {

    const row = document.querySelector(`tr[data-employee-id="${id}"]`);
    if (!row) return;

    // Highlight the updated row
    row.classList.add('updated-row');
    setTimeout(() => row.classList.remove('updated-row'), 1500);

    // Update each cell with new data
    row.cells[1].textContent = `${employee.first_name} ${employee.last_name}`;
    row.cells[2].innerHTML = employee.gender === 'Male' ? 
        '<i class="fas fa-mars" style="color: #3498db;"></i> Male' : 
        '<i class="fas fa-venus" style="color: #e83e8c;"></i> Female';
    row.cells[3].textContent = employee.role;
    row.cells[4].textContent = employee.department;
    row.cells[5].textContent = `ETB ${(employee.salary || 0).toLocaleString()}`;
    row.cells[6].textContent = employee.date_hired ? 
        new Date(employee.date_hired).toLocaleDateString('en-US', { day: 'numeric', month: 'short', year: 'numeric' }) : 
        'N/A';
    row.cells[7].innerHTML = `<span class="status-badge status-${employee.is_active ? 'active' : 'inactive'}">
        ${employee.is_active ? 'Active' : 'Inactive'}
    </span>`;
}