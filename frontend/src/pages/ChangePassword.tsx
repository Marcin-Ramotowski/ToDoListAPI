import { useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../api/api";
import Cookies from "js-cookie"

const ChangePassword = () => {
  const id = Cookies.get("user_id")
  const navigate = useNavigate();
  if (!id) {
    navigate("/login")
  }
  const [newPassword, setNewPassword] = useState("");
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    setSuccess("");

    try {
      await api.patch(`/users/${id}`, {
        password: newPassword,
      });

      setSuccess("Hasło zostało zmienione.");
      setNewPassword("");

      setTimeout(() => navigate("/profile"), 2000); // krótka pauza, żeby pokazać sukces
    } catch (err: any) {
      console.error(err);
      setError(err.response?.data?.message || "Błąd zmiany hasła.");
    }
  };

  return (
    <div className="p-6 max-w-md mx-auto">
      <h1 className="text-2xl font-bold mb-4">Zmień hasło</h1>

      <form onSubmit={handleSubmit} className="bg-white shadow p-4 rounded flex flex-col gap-4">
        <input
          type="password"
          placeholder="Nowe hasło"
          value={newPassword}
          onChange={(e) => setNewPassword(e.target.value)}
          required
          className="border p-2 rounded"
        />

        <button
          type="submit"
          className="bg-blue-500 text-white p-2 rounded hover:bg-blue-600"
        >
          💾 Zapisz hasło
        </button>

        {error && <p className="text-red-500">{error}</p>}
        {success && <p className="text-green-600">{success}</p>}
      </form>
    </div>
  );
};

export default ChangePassword;
