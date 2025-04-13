import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { getUser, deleteUser } from "../api/user";
import Cookies from "js-cookie";

interface User {
  id: number;
  username: string;
  email: string;
  role: string;
}

const Profile = () => {
  const id = Cookies.get("user_id")
  const navigate = useNavigate();
  if (!id) {
    navigate("/login")
  }
  const [user, setUser] = useState<User | null>(null);

  useEffect(() => {
    const fetchUser = async () => {
      try {
        const userData = await getUser(Number(id));
        setUser(userData);
      } catch (error) {
        console.error("Błąd podczas pobierania danych użytkownika:", error);
      }
    };

    fetchUser();
  }, [id]);

  const handleDeleteAccount = async () => {
    if (!window.confirm("Na pewno chcesz usunąć konto? Tej operacji nie da się cofnąć.")) return;

    try {
      await deleteUser(Number(id));
      Cookies.remove("user_id");
      navigate("/login");
    } catch (error) {
      console.error("Błąd podczas usuwania konta:", error);
    }
  };

  if (!user) return <div className="p-6">Ładowanie danych użytkownika...</div>;

  return (
    <div className="p-6 max-w-md mx-auto">
      <h1 className="text-2xl font-bold mb-4">Twój profil</h1>

      <div className="bg-white shadow rounded p-4 mb-4">
        <p><strong>Nazwa użytkownika:</strong> {user.username}</p>
        <p><strong>Email:</strong> {user.email}</p>
        <p><strong>Rola:</strong> {user.role}</p>
      </div>

      <div className="flex flex-col gap-2">
        <button
          onClick={() => navigate("/profile/change-password")}
          className="bg-blue-500 text-white p-2 rounded hover:bg-blue-600"
        >
          🔐 Zmień hasło
        </button>

        <button
          onClick={handleDeleteAccount}
          className="bg-red-500 text-white p-2 rounded hover:bg-red-600"
        >
          🗑️ Usuń konto
        </button>
      </div>
    </div>
  );
};

export default Profile;
