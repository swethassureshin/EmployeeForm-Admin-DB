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
  form.addEventListener("submit", async (e) => {
    e.preventDefault();

    const formData = new FormData();

    formData.append("full_name", document.getElementById("fullName").value);
    formData.append("email", document.getElementById("email").value);
    formData.append("phone", document.getElementById("phone").value);
    formData.append("address", document.getElementById("address").value);
    formData.append("employee_id", document.getElementById("employeeId").value);
    formData.append("department", document.getElementById("department").value);
    formData.append("date_of_joining", document.getElementById("joinDate").value);
    formData.append("gender", document.getElementById("gender").value);
    formData.append("dob", document.getElementById("dob").value);

    if (fileInput.files.length > 0) {
      formData.append("idProof", fileInput.files[0]);
    }

    const response = await fetch("http://127.0.0.1:5000/add-employee", {
      method: "POST",
      body: formData
    });

    if (response.ok) {
      window.location.href = "submit.html";
    } else {
      alert("Submission failed. Try again.");
    }
  });
});
