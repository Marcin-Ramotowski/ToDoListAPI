import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Register from "./pages/Register";
import Login from "./pages/Login";
import Tasks from "./pages/Tasks";
import Profile from "./pages/Profile";
import ChangePassword from "./pages/ChangePassword";
import DeleteAccount from "./pages/DeleteAccount";

const App = () => {
  return (
    <Router>
      <Routes>
        <Route path="/register" element={<Register />} />        
        <Route path="/login" element={<Login />} />
        <Route path="/tasks" element={<Tasks />} />
        <Route path="/profile" element={<Profile />} />
        <Route path="/profile/change-password" element={<ChangePassword />} />
        <Route path="/profile/delete" element={<DeleteAccount />} />
      </Routes>
    </Router>
  );
};

export default App;
