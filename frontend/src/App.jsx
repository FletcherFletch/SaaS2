import { useState } from 'react'
import react from "react"
import {Navigate, BrowserRouter, Route, Routes} from 'react-router-dom'
import Login from "./pages/Login"
import Home from "./pages/Home"

function App() {
  const [count, setCount] = useState(0)

  return (
   
      <BrowserRouter>
        <Routes>
          <Route path="/Login" element={<Login />} />
          <Route path="/" element={<Home />} />


        </Routes>
      
      </BrowserRouter>

   
  )
}

export default App
