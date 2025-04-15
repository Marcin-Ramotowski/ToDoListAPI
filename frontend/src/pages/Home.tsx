import { useEffect } from "react";
import { useNavigate } from "react-router-dom";
import Cookies from "js-cookie";

const Home = () => {
  const navigate = useNavigate();
  const userId = Cookies.get("user_id");

  useEffect(() => {
    if (userId) {
      navigate("/tasks"); // redirect logged-in users to tasks
    }
  }, [userId]);

  return (
    <div className="flex flex-col items-center justify-center h-screen bg-gray-50">
      <h1 className="text-4xl font-bold mb-4">Witaj w Taskerze ✅</h1>
      <p className="text-lg mb-6">Zarządzaj swoimi zadaniami w prosty sposób.</p>
      <div className="flex space-x-4">
        <button 
          onClick={() => navigate("/login")} 
          className="bg-blue-500 text-white px-6 py-2 rounded hover:bg-blue-600"
        >
          Zaloguj się
        </button>
        <button 
          onClick={() => navigate("/register")} 
          className="bg-green-500 text-white px-6 py-2 rounded hover:bg-green-600"
        >
          Zarejestruj się
        </button>
      </div>
    </div>
  );
};

export default Home;
