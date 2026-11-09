// Automatically hide notification messages after 4 seconds
document.addEventListener("DOMContentLoaded", function () {
    const memberSearch = document.getElementById("memberSearch");

if (memberSearch) {
    memberSearch.addEventListener("input", function () {
        const searchValue = this.value.toLowerCase();

        document.querySelectorAll("#membersTable tbody tr")
            .forEach(function (row) {
                row.style.display =
                    row.textContent.toLowerCase().includes(searchValue)
                    ? ""
                    : "none";
            });
    });
}
    const bookSearch = document.getElementById("bookSearch");

if (bookSearch) {
    bookSearch.addEventListener("input", function () {
        const searchValue = this.value.toLowerCase();

        document.querySelectorAll("#booksTable tbody tr")
            .forEach(function (row) {
                row.style.display =
                    row.textContent.toLowerCase().includes(searchValue)
                    ? ""
                    : "none";
            });
    });
}
    const profileBtn = document.getElementById("profileBtn");
const profileDropdown = document.getElementById("profileDropdown");

if (profileBtn && profileDropdown) {

    profileBtn.addEventListener("click", function (event) {
        event.stopPropagation();
        profileDropdown.classList.toggle("show");
    });

    document.addEventListener("click", function (event) {
        if (!profileDropdown.contains(event.target)) {
            profileDropdown.classList.remove("show");
        }
    });
}
    const alerts = document.querySelectorAll(".alert");

    alerts.forEach(function (alert) {
        setTimeout(function () {
            alert.style.transition = "opacity 0.5s";
            alert.style.opacity = "0";

            setTimeout(function () {
                alert.remove();
            }, 500);
        }, 4000);
    });
});