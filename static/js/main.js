document.addEventListener("DOMContentLoaded", function () {
    const toggleBtn = document.createElement("button");
    toggleBtn.innerText = "🌙";
    toggleBtn.title = "Toggle dark mode";

    // ZAMONAVIY STIL
    Object.assign(toggleBtn.style, {
        position: "fixed",
        bottom: "20px",
        right: "20px",
        zIndex: 9999,
        width: "50px",
        height: "50px",
        background: "#222",
        color: "#fff",
        border: "none",
        borderRadius: "50%",
        boxShadow: "0 4px 12px rgba(0, 0, 0, 0.2)",
        fontSize: "24px",
        cursor: "pointer",
        transition: "all 0.3s ease",
    });

    // HOVER effekt
    toggleBtn.addEventListener("mouseover", () => {
        toggleBtn.style.background = "#444";
        toggleBtn.style.transform = "scale(1.1)";
    });

    toggleBtn.addEventListener("mouseout", () => {
        toggleBtn.style.background = "#222";
        toggleBtn.style.transform = "scale(1)";
    });

    toggleBtn.onclick = function () {
        document.body.classList.toggle("dark-mode");
        if (document.body.classList.contains("dark-mode")) {
            localStorage.setItem("theme", "dark");
        } else {
            localStorage.setItem("theme", "light");
        }
    };

    document.body.appendChild(toggleBtn);

    if (localStorage.getItem("theme") === "dark") {
        document.body.classList.add("dark-mode");
    }
});
