import React, { useState } from 'react'
import './App.css'
import 'bootstrap/dist/css/bootstrap.min.css'
import Header from "./components/header/Header.jsx";
import Home from "./pages/home/Home.jsx";
import "./scss/bootstrap.scss";
import {createBrowserRouter, createRoutesFromElements, Outlet, Route, RouterProvider} from "react-router-dom";
import SearchingChoice from "./pages/searching_choice/SearchingChoice.jsx";
import ManualSearch from "./pages/manual_search/ManualSearch.jsx";
import Attack from "./pages/threat_show/attack/Attack.jsx";
import Tool from "./pages/threat_show/tool/Tool.jsx";
import Malware from "./pages/threat_show/malware/Malware.jsx";
import Campaign from "./pages/threat_show/campaign/Campaign.jsx";
import Asset from "./pages/threat_show/asset/Asset.jsx";
import Vulnerability from "./pages/threat_show/vulnerability/Vulnerability.jsx";
import IntrusionSet from "./pages/threat_show/intrusion_set/IntrusionSet.jsx";


const router = createBrowserRouter(
  createRoutesFromElements(
    <Route path="/" element={<Header />}>
      <Route path="" element={<Home />} />
        <Route path="searching_choice" element={<SearchingChoice />} />
        <Route path="manual_search" element={<ManualSearch />} />
        <Route path="attack_pattern" element={<Attack />} />
        <Route path="tool" element={<Tool />} />
        <Route path="malware" element={<Malware />} />
        <Route path="campaign" element={<Campaign />} />
        <Route path="asset" element={<Asset />}/>
        <Route path="intrusion_set" element={<IntrusionSet />}/>
        <Route path="vulnerability" element={<Vulnerability />}/>
        {/*  <Route path="register" element={<Register />}/> */}
    </Route>
  )
)

function App() {

  return (
    <div className="App">
      <div>
            <RouterProvider router={router}/>
      </div>
    </div>
  )
}

export default App
