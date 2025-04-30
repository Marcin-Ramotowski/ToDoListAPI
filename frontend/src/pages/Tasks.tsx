import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { getUserTasks, createTask, deleteTask } from "../api/tasks";
import { logout } from "../api/auth";
import api from "../api/api";
import Cookies from "js-cookie";
import { User } from "lucide-react";

// Define Task type
interface Task {
  id: number;
  title: string;
  description: string;
  due_date: string;
  done: boolean;
}

const Tasks = () => {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [newTask, setNewTask] = useState({ title: "", description: "", due_date: "", done: false });
  const [editingTaskId, setEditingTaskId] = useState<number | null>(null);
  const [editedTask, setEditedTask] = useState<Partial<Task>>({});  
  const navigate = useNavigate();
  const userId = Number(Cookies.get("user_id"))

  useEffect(() => {
    if (!userId) {
      navigate("/login");
      return;
    }

    const fetchTasks = async () => {
      try {
        const tasksData = await getUserTasks(userId);
        setTasks(tasksData);
      } catch (error) {
        console.error("Error during tasks fetching:", error);
      }
    };

    fetchTasks();
  }, [userId]);

  const handleLogout = async () => {
    await logout();
    navigate("/login");
  };

  const handleCreateTask = async () => {
    try {
      const task = await createTask(newTask);
      setTasks([...tasks, task]); // List update
      setNewTask({ title: "", description: "", due_date: "", done: false }); // Form reset
    } catch (error) {
      console.error("Error during task creation:", error);
    }
  };

  const handleDeleteTask = async (taskId: number) => {
    try {
      await deleteTask(taskId);
      setTasks(tasks.filter((task) => task.id !== taskId));
    } catch (error) {
      console.error("Error during task deletion:", error);
    }
  };

  // Change task status
  const handleToggleTaskStatus = async (taskId: number) => {
    try {
      const updatedTasks = tasks.map(task => {
        if (task.id === taskId) {
          const newStatus = !task.done;
          // Send PATCH request to backend
          api.patch(`/tasks/${task.id}`, { done: newStatus });
          // Change local state
          return { ...task, done: newStatus };
        }
        return task;
      });
      setTasks(updatedTasks); // refresh UI
    } catch (err) {
      console.error("Error during task update:", err);
    }
  };

  const handleEditTask = (task: Task) => {
    setEditingTaskId(task.id);
    setEditedTask({
      title: task.title,
      description: task.description,
      due_date: task.due_date
    });
  };
  
  const handleCancelEdit = () => {
    setEditingTaskId(null);
    setEditedTask({});
  };
  
  const handleSaveEdit = async (taskId: number) => {
    try {
      const response = await api.patch(`/tasks/${taskId}`, editedTask);
      setTasks(tasks.map((t) => (t.id === taskId ? response.data : t)));
      setEditingTaskId(null);
      setEditedTask({});
    } catch (error) {
      console.error("Błąd podczas edycji zadania:", error);
    }
  };

  return (
    <div className="p-6 relative min-h-screen">
      <button 
        onClick={() => navigate(`/profile`)} 
        className="text-gray-600 hover:text-black mb-4 flex items-center">
        <User className="w-5 h-5 mr-1" />
        Profil
      </button>
      <h1 className="text-2xl font-bold mb-4">Twoje zadania</h1>
      <button 
        onClick={handleLogout} 
        className="bg-red-500 text-white p-2 rounded hover:bg-red-600 mb-4"
      >
        Wyloguj
      </button>

      {/* Form to add a task */}
      <div className="mb-6">
        <input 
          type="text" placeholder="Tytuł" value={newTask.title} 
          onChange={(e) => setNewTask({ ...newTask, title: e.target.value })} 
          className="border p-2 mr-2"
        />
        <input 
          type="text" placeholder="Opis" value={newTask.description} 
          onChange={(e) => setNewTask({ ...newTask, description: e.target.value })} 
          className="border p-2 mr-2"
        />
        <input 
          type="datetime-local" placeholder="Termin" value={newTask.due_date} 
          onChange={(e) => setNewTask({ ...newTask, due_date: e.target.value })} 
          className="border p-2 mr-2"
        />
        <button 
          onClick={handleCreateTask} 
          className="bg-blue-500 text-white p-2 rounded hover:bg-blue-600"
        >
          Dodaj zadanie
        </button>
      </div>

      {/* 🔹 Task list */}
      {tasks.length === 0 ? (
        <p>Brak zadań.</p>
      ) : (
        <ul>
          {tasks.map((task) => (
            <li key={task.id} className="border p-2 rounded mb-2 flex justify-between items-start gap-2">
              <div className="flex-1">
                {editingTaskId === task.id ? (
                  <>
                    <input
                      type="text"
                      value={editedTask.title || ""}
                      onChange={(e) => setEditedTask({ ...editedTask, title: e.target.value })}
                      className="border p-1 mb-1 w-full"
                    />
                    <textarea
                      value={editedTask.description || ""}
                      onChange={(e) => setEditedTask({ ...editedTask, description: e.target.value })}
                      className="border p-1 mb-1 w-full"
                    />
                    <input
                      type="datetime-local"
                      value={editedTask.due_date || ""}
                      onChange={(e) => setEditedTask({ ...editedTask, due_date: e.target.value })}
                      className="border p-1 mb-1 w-full"
                    />
                    <div className="flex gap-2 mt-1">
                      <button
                        onClick={() => handleSaveEdit(task.id)}
                        className="bg-green-500 text-white px-2 py-1 rounded hover:bg-green-600"
                      >
                        💾 Zapisz
                      </button>
                      <button
                        onClick={handleCancelEdit}
                        className="bg-gray-400 text-white px-2 py-1 rounded hover:bg-gray-500"
                      >
                        ❌ Anuluj
                      </button>
                    </div>
                  </>
                ) : (
                  <>
                    <h2 className="font-semibold">{task.title}</h2>
                    <p>{task.description}</p>
                    <p><strong>Termin:</strong> {task.due_date}</p>
                    <p>
                      <strong>Status:</strong> {task.done ? "✅ Zrobione" : "⏳ Do zrobienia"}
                      <input
                        type="checkbox"
                        checked={task.done}
                        onChange={() => handleToggleTaskStatus(task.id)}
                        className="ml-2"
                      />
                    </p>
                  </>
                )}
              </div>

              <div className="flex flex-col gap-2">
                {editingTaskId !== task.id && (
                  <button
                    onClick={() => handleEditTask(task)}
                    className="bg-yellow-400 text-white px-2 py-1 rounded hover:bg-yellow-500"
                  >
                    ✏️ Edytuj
                  </button>
                )}
                <button
                  onClick={() => handleDeleteTask(task.id)}
                  className="bg-red-500 text-white px-2 py-1 rounded hover:bg-red-600"
                >
                  ❌ Usuń
                </button>
              </div>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default Tasks;
