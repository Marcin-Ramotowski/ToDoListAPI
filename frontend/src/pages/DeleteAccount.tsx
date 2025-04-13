import { useNavigate, useParams } from "react-router-dom";
import { useState } from "react";
import api from "../api/api";
import { logout } from "../api/auth";

const DeleteAccount = () => {
  const navigate = useNavigate();
  const { id } = useParams();
  const [confirmation, setConfirmation] = useState("");
  const [error, setError] = useState("");

  const handleDelete = async () => {
    try {
      await api.delete(`/users/${id}`);
      await logout();
      navigate("/login");
    } catch (err: any) {
      console.error(err);
      setError("Wystąpił błąd podczas usuwania konta.");
    }
  };

  return (
    <div className="p-6 max-w-md mx-auto">
      <h1 className="text-2xl font-bold mb-4 text-red-600">⚠️ Usuń konto</h1>
      <p className="mb-4">
        Tej operacji nie można cofnąć. Aby potwierdzić, wpisz <strong>USUŃ</strong> poniżej:
      </p>

      <input
        type="text"
        placeholder="Wpisz: USUŃ"
        value={confirmation}
        onChange={(e) => setConfirmation(e.target.value)}
        className="border p-2 rounded w-full mb-4"
      />

      <button
        onClick={handleDelete}
        disabled={confirmation !== "USUŃ"}
        className={`p-2 rounded w-full ${
          confirmation === "USUŃ"
            ? "bg-red-600 text-white hover:bg-red-700"
            : "bg-gray-300 text-gray-600 cursor-not-allowed"
        }`}
      >
        🗑️ Potwierdź usunięcie konta
      </button>

      {error && <p className="text-red-500 mt-2">{error}</p>}
    </div>
  );
};

export default DeleteAccount;
