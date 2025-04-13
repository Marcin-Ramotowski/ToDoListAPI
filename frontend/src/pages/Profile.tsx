import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { getUser, updateUser } from "../api/user";
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
  const [editMode, setEditMode] = useState(false);
  const [formData, setFormData] = useState({ username: "", email: "" });

  useEffect(() => {
    const fetchUser = async () => {
      try {
        const data = await getUser(Number(id));
        setUser(data);
        setFormData({ username: data.username, email: data.email });
      } catch (err) {
        console.error("Błąd podczas pobierania danych użytkownika:", err);
        navigate("/tasks");
      }
    };

    fetchUser();
  }, [id]);

  const handleUpdate = async () => {
    try {
      const updated = await updateUser(Number(id), formData);
      setUser(updated);
      setEditMode(false);
    } catch (err) {
      console.error("Błąd podczas aktualizacji użytkownika:", err);
    }
  };

  if (!user) return <p>Ładowanie...</p>;

  return (
    <div className="p-6 max-w-xl mx-auto">
      <h1 className="text-2xl font-bold mb-6">👤 Twój profil</h1>

      <div className="mb-4">
        <label className="block font-semibold mb-1">Nazwa użytkownika:</label>
        {editMode ? (
          <input
            type="text"
            value={formData.username}
            onChange={(e) => setFormData({ ...formData, username: e.target.value })}
            className="border p-2 rounded w-full"
          />
        ) : (
          <p>{user.username}</p>
        )}
      </div>

      <div className="mb-4">
        <label className="block font-semibold mb-1">Email:</label>
        {editMode ? (
          <input
            type="email"
            value={formData.email}
            onChange={(e) => setFormData({ ...formData, email: e.target.value })}
            className="border p-2 rounded w-full"
          />
        ) : (
          <p>{user.email}</p>
        )}
      </div>

      <div className="mb-6">
        <label className="block font-semibold mb-1">Rola:</label>
        <p>{user.role}</p>
      </div>

      {editMode ? (
        <div className="flex gap-2">
          <button
            onClick={handleUpdate}
            className="bg-green-500 text-white px-4 py-2 rounded hover:bg-green-600"
          >
            💾 Zapisz zmiany
          </button>
          <button
            onClick={() => {
              setEditMode(false);
              setFormData({ username: user.username, email: user.email });
            }}
            className="bg-gray-300 px-4 py-2 rounded hover:bg-gray-400"
          >
            Anuluj
          </button>
        </div>
      ) : (
        <button
          onClick={() => setEditMode(true)}
          className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600"
        >
          ✏️ Edytuj profil
        </button>
      )}
      {!editMode && (
        <div className="mt-6 flex flex-col gap-2">
          <button
            onClick={() => navigate("/profile/change-password")}
            className="bg-yellow-500 text-white px-4 py-2 rounded hover:bg-yellow-600"
          >
            🔒 Zmień hasło
          </button>
          <button
            onClick={() => navigate("/profile/delete")}
            className="bg-red-500 text-white px-4 py-2 rounded hover:bg-red-600"
          >
            ❌ Usuń konto
          </button>
        </div>
      )}
    </div>
  );
};

export default Profile;
