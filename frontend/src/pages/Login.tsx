import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { login } from "../api/auth";

const Login = () => {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const navigate = useNavigate();

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");

    try {
      const { userId } = await login(username, password);
      console.log("User logged in successfully! user_id:", userId);
      navigate("/tasks");
    } catch (err) {
      console.error(err);
      setError("Incorrect login data");
    }
  };

  return (
    <div className="flex justify-center items-center h-screen bg-gray-100">
      <div className="bg-white p-8 rounded-lg shadow-md w-96">
        <h2 className="text-2xl font-bold mb-4 text-center">Logowanie</h2>
        {error && <p className="text-red-500 text-center">{error}</p>}
        
        <form onSubmit={handleLogin} className="flex flex-col gap-4">
          <input 
            type="text" 
            placeholder="Nazwa użytkownika" 
            value={username} 
            onChange={(e) => setUsername(e.target.value)} 
            className="border p-2 rounded"
            required
          />
          <input 
            type="password" 
            placeholder="Hasło" 
            value={password} 
            onChange={(e) => setPassword(e.target.value)} 
            className="border p-2 rounded"
            required
          />
          <button type="submit" className="bg-blue-500 text-white p-2 rounded hover:bg-blue-600">
            Zaloguj się
          </button>
        </form>
        <p className="mt-4">
          Nie masz jeszcze konta?{" "}
          <a href="/register" className="text-blue-600 hover:underline">
            Zarejestruj się
          </a>
        </p>        
      </div>
    </div>
  );
};

export default Login;
