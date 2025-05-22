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
    fetch(`/api/employees/${id}`)
        .then(response => response.json())
        .then(data => {
            const modal = new bootstrap.Modal(document.getElementById('viewEmployeeModal'));
            const modalContent = `
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
            document.getElementById('viewEmployeeModal').innerHTML = modalContent;
            modal.show();
        })
        .catch(error => console.error('Error:', error));
}

function editEmployee(id) {
    window.location.href = `/employees/edit/${id}`;
}

function confirmDelete(id) {
    if (confirm('Are you sure you want to delete this employee?')) {
        fetch(`/api/employees/${id}`, {
            method: 'DELETE'
        })
        .then(response => {
            if (response.ok) {
                location.reload();
            }
        })
        .catch(error => console.error('Error:', error));
    }
}