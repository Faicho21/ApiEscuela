import { BrowserRouter, Routes, Route } from 'react-router-dom'
import { lazy } from 'react'
import ProtectedRoute from './components/Routes/ProtectedRoute'
import PublicRoute from './components/Routes/PublicRoute'
import Login from './views/Login'
import MainLayout from './layouts/MainLayaut'

function App() {
 const Dashboard = lazy(() => import('./views/Dashboard'))


  return (
       <BrowserRouter>
     <Routes>
       <Route element={<PublicRoute />}>
         <Route path="/" element={<Login />} />
         <Route path="/login" element={<Login />} />
       </Route>

       <Route element={<ProtectedRoute />}>
        <Route element={<MainLayout />}>
          <Route path="/dashboard" element={<Dashboard />} />
        </Route>
       </Route>
     </Routes>
   </BrowserRouter>
  )
}

export default App
