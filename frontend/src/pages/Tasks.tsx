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
          type="text" placeholder="Termin (DD-MM-YYYY HH:MM)" value={newTask.due_date} 
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
            <li key={task.id} className="border p-2 rounded mb-2 flex justify-between items-center">
              <div>
                <h2 className="font-semibold">{task.title}</h2>
                <p>{task.description}</p>
                <p><strong>Termin:</strong> {task.due_date}</p>
                <p><strong>Status:</strong> {task.done ? "✅ Zrobione" : "⏳ Do zrobienia"} 
                <input type="checkbox" checked={task.done} onChange={() => handleToggleTaskStatus(task.id)}/>
                </p>
              </div>
              <button 
                onClick={() => handleDeleteTask(task.id)} 
                className="bg-red-500 text-white p-2 rounded hover:bg-red-600"
              >
                ❌ Usuń
              </button>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default Tasks;
