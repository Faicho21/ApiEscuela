import { NavLink } from "react-router-dom";

function Logout() {
  localStorage.removeItem("token");
  localStorage.removeItem("user");
  window.location.href = "/login";
}

function Nvar() {
  return (
    <nav className="navbar navbar-expand-lg navbar-dark" style={{ backgroundColor: "#3ab397" }}>
      <div className="container">
        <NavLink className="navbar-brand" to="/dashboard">Mi Escuela</NavLink>
        <button className="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
          <span className="navbar-toggler-icon"></span>
        </button>
        <div className="collapse navbar-collapse" id="navbarNav">
          <ul className="navbar-nav me-auto">
            <li className="nav-item">
              <NavLink className="nav-link" to="/dashboard">Home</NavLink>
            </li>
            <li className="nav-item">
              <NavLink className="nav-link" to="/contactos">Contactos</NavLink>
            </li>
            <li className="nav-item">
              <NavLink className="nav-link" to="/profile">Perfil</NavLink>
            </li>
            <li className="nav-item">
              <NavLink className="nav-link" to="/notificaciones">Notificaciones</NavLink>
            </li>
          </ul>
          <button className="btn btn-outline-light" onClick={Logout}>Cerrar Sesión</button>
        </div>
      </div>
    </nav>
  );
}

export default Nvar;