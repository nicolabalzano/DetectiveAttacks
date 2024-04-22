import React, { useState } from 'react'
import './App.css'
import 'bootstrap/dist/css/bootstrap.min.css'
import Header from "./components/header/Header.jsx";
import Home from "./pages/home/Home.jsx";
import "./scss/bootstrap.scss";
import {createBrowserRouter, createRoutesFromElements, Outlet, Route, RouterProvider} from "react-router-dom";
import SearchingChoice from "./pages/searching_choice/SearchingChoice.jsx";
import ManualSearch from "./pages/manual_search/ManualSearch.jsx";


const router = createBrowserRouter(
  createRoutesFromElements(
    <Route path="/" element={<Header />}>
      <Route path="" element={<Home />} />
        <Route path="searching_choice" element={<SearchingChoice />} />
        <Route path="manual_search" element={<ManualSearch />} />
        {/*  <Route path="register" element={<Register />}/> */}
    </Route>
  )
)

function App({routes}) {
  const [count, setCount] = useState(0)

  return (
    <div className="App">
      <div>
            <RouterProvider router={router}/>
      </div>
    </div>
  )
}

export default App
