import { useState, useEffect } from "react";
import { useThemeContext } from "../../hooks/useThemeContext";
import "./theme-switch.css";

export default function ThemeSwitch() {
  const { darkMode, setDarkMode } = useThemeContext();

  const switchTheme = () => setDarkMode((prev) => !prev);

  useEffect(() => {
    // Set the theme mode on the document element
    if (darkMode) {
      document.documentElement.setAttribute("darkMode", "");
    } else {
      document.documentElement.removeAttribute("darkMode", "");
    }

    // Initialize scroll position
    let prevScrollpos = window.pageYOffset;

    // Handle scroll function to hide or show the theme switch based on scroll direction
    const handleScroll = () => {
      let currentScrollPos = window.pageYOffset;
      if (prevScrollpos > currentScrollPos) {
        document.getElementById("theme-switch").style.bottom = "20px";
      } else {
        document.getElementById("theme-switch").style.bottom = "-50px"; // Adjust this value based on your actual needs
      }
      prevScrollpos = currentScrollPos;
    };

    // Attach scroll event listener
    window.addEventListener("scroll", handleScroll);

    // Clean up the event listener when the component unmounts
    return () => {
      window.removeEventListener("scroll", handleScroll);
    };
  }, [darkMode]);

  return (
    <div id="theme-switch" className="position-fixed mt-4">
      <div className="switch-track">
        <div className="switch-check">
          <span className="switch-icon">
              <i className="bi bi-moon-fill text-primary"></i>
          </span>
        </div>
          <div className="switch-x">
          <span className="switch-icon">
              <i className="bi bi-brightness-high-fill text-white"></i>
          </span>
        </div>
          <div className="switch-thumb"></div>
      </div>

      <input
        type="checkbox"
        checked={darkMode}
        onChange={switchTheme}
        aria-label="Switch between dark and light mode"
      />
    </div>
  );
}