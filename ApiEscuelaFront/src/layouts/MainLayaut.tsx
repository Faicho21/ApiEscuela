import { Outlet } from "react-router-dom";
import Navbar from "../layouts/Nvar";



function MainLayout() {
 return (
   <div>
     <Navbar />
     <main>
       <Outlet />
     </main>
   </div>
 );
}


export default MainLayout;