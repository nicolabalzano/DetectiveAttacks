import { useState, useEffect } from "react";
import { useThemeContext } from "../../hooks/useThemeContext";
import "./theme-switch.css";

export default function ThemeSwitch() {
  const { darkMode, setDarkMode } = useThemeContext();

  const switchTheme = () => setDarkMode((prev) => !prev);

  useEffect(() => {
    darkMode
      ? document.documentElement.setAttribute("darkMode", "")
      : document.documentElement.removeAttribute("darkMode", "");
  }, [darkMode]);

  return (
    <div id="theme-switch" className="mt-3 fixed-top">
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