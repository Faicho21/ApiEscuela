import { Navigate, Outlet } from "react-router-dom";

function PublicRoute() {
  const token = localStorage.getItem("token");

  if (token) {
<<<<<<< HEAD
    return <Navigate to="/home" />;
=======
    return <Navigate to="/dashboard" />;
>>>>>>> 69f95d5dc9afdc708356947d9caf60b368a31db0
  }

  return <Outlet />;
}
export default PublicRoute;
