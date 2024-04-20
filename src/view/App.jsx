import React, { useState } from 'react'
import './App.css'
import 'bootstrap/dist/css/bootstrap.min.css'
import Header from "./components/header/Header.jsx";
import Home from "./components/home/Home.jsx";
import ThemeSwitch from "./components/theme_switch/themeSwitch.jsx";
import { ThemeProvider } from "./hooks/useThemeContext";
import "./scss/bootstrap.scss";

function App() {
  const [count, setCount] = useState(0)

  return (
    <div className="App p-3">
      <div className="d-flex flex-column align-items-center">
          <ThemeProvider>

              <ThemeSwitch/>
              <Header/>
              <Home/>

          </ThemeProvider>
      </div>
    </div>
  )
}

export default App
