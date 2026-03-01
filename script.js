document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("employeeForm");
  const fileInput = document.getElementById("idProof");
  const fileNameDisplay = document.getElementById("fileName");
  const uploadBox = document.getElementById("uploadBox");

  // File upload UI
  fileInput.addEventListener("change", () => {
    if (fileInput.files.length > 0) {
      fileNameDisplay.textContent =
        "Selected file: " + fileInput.files[0].name;
      uploadBox.classList.add("hidden");
    }
  });

  // Form submit
  form.addEventListener("submit", (e) => {
    e.preventDefault();

    const employee = {
      name: document.querySelector('input[placeholder="e.g. Johnathan Doe"]').value.trim(),
      empId: document.querySelector('input[placeholder="EMP-2023-001"]').value.trim(),
      department: document.querySelector("select").value,
      date: new Date().toLocaleDateString()
    };

    // Save name for success page
    localStorage.setItem("employeeName", employee.name);

    // Save list for admin dashboard
    const employees = JSON.parse(localStorage.getItem("employees")) || [];
    employees.push(employee);
    localStorage.setItem("employees", JSON.stringify(employees));

    // Redirect
    window.location.href = "submit.html";
  });
});