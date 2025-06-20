import { BrowserRouter, Routes, Route } from 'react-router-dom'
import { lazy } from 'react'
import ProtectedRoute from './components/Routes/ProtectedRoute'
import PublicRoute from './components/Routes/PublicRoute'
import Login from './views/Login'
import MainLayout from './layouts/MainLayaut'

function App() {
<<<<<<< HEAD
 const Home = lazy(() => import('./views/Home'))
=======
 const Dashboard = lazy(() => import('./views/Dashboard'))
>>>>>>> 69f95d5dc9afdc708356947d9caf60b368a31db0


  return (
       <BrowserRouter>
     <Routes>
       <Route element={<PublicRoute />}>
         <Route path="/" element={<Login />} />
         <Route path="/login" element={<Login />} />
       </Route>

       <Route element={<ProtectedRoute />}>
        <Route element={<MainLayout />}>
<<<<<<< HEAD
          <Route path="/Home" element={<Home />} />
=======
          <Route path="/dashboard" element={<Dashboard />} />
>>>>>>> 69f95d5dc9afdc708356947d9caf60b368a31db0
        </Route>
       </Route>
     </Routes>
   </BrowserRouter>
  )
}

<<<<<<< HEAD
export default App;
=======
export default App
>>>>>>> 69f95d5dc9afdc708356947d9caf60b368a31db0
