import { useState, useEffect } from 'react';
import axios from 'axios';

function App() {
    const [notes, setNotes] = useState([]);
    const [newNote, setNewNote] = useState('');

    // Pobieranie notatek z API
    useEffect(() => {
        axios.get('http://localhost:5000/tasks')
            .then((response) => setNotes(response.data))
            .catch((error) => console.error('Błąd podczas pobierania notatek:', error));
    }, []);

    // Dodawanie nowej notatki
    const addNote = () => {
        if (newNote.trim() !== '') {
            axios.post('http://localhost:5000/tasks', { content: newNote })
                .then((response) => {
                    setNotes([...notes, response.data]);
                    setNewNote('');
                })
                .catch((error) => console.error('Błąd podczas dodawania notatki:', error));
        }
    };

    // Usuwanie notatki
    const deleteNote = (id) => {
        axios.delete(`http://localhost:5000/tasks/${id}`)
            .then(() => setNotes(notes.filter((note) => note.id !== id)))
            .catch((error) => console.error('Błąd podczas usuwania notatki:', error));
    };

    return (
        <div className="min-h-screen bg-gray-100 p-6">
            <div className="max-w-3xl mx-auto bg-white p-6 rounded-2xl shadow-lg">
                <h1 className="text-2xl font-bold mb-4">📝 Moja lista notatek</h1>
                <div className="mb-4">
                    <input
                        type="text"
                        placeholder="Dodaj nową notatkę..."
                        className="p-2 border rounded w-full"
                        value={newNote}
                        onChange={(e) => setNewNote(e.target.value)}
                    />
                    <button
                        className="mt-2 bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600"
                        onClick={addNote}
                    >
                        Dodaj notatkę
                    </button>
                </div>
                <ul>
                    {notes.map((note) => (
                        <li key={note.id} className="flex justify-between items-center p-2 bg-gray-50 rounded mb-2">
                            <span>{note.content}</span>
                            <button
                                className="bg-red-500 text-white px-2 py-1 rounded hover:bg-red-600"
                                onClick={() => deleteNote(note.id)}
                            >
                                Usuń
                            </button>
                        </li>
                    ))}
                </ul>
            </div>
        </div>
    );
}

export default App;