const checkboxes = document.querySelectorAll(".form-checkbox input[type='checkbox']");

checkboxes.forEach((checkbox) => {
    checkbox.addEventListener("change", () => {
        checkbox.form.submit();
    });
});