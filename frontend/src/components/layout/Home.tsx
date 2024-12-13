import logo from '../../assets/logo.png'
import './Home.css'
import { useNavigate } from 'react-router-dom';
import { useState, useEffect } from 'react';
import { showMessage } from '../../utils/messages';
import type { MessageType } from '../../types';

function Home() {
    const [formData, setFormData] = useState({
        name: '',
    });

    const [message, setMessage] = useState({
        text: '',
        type: null as MessageType
    });

    const [tasks, setTasks] = useState<{ id: number; name: string }[]>([]);
    const [completeTasks, setCompleteTasks] = useState<{ id: number; name: string }[]>([]);
    const navigate = useNavigate();

    const [editingTaskId, setEditingTaskId] = useState<number | null>(null);
    const [editingTaskName, setEditingTaskName] = useState<string>('');

    const handleLogout = () => {
        localStorage.removeItem('token');
        navigate('/');
    };

    const handleAdd = async (event: React.FormEvent) => {
        event.preventDefault();
        if (!formData.name) {
            showMessage('Please fill in the field', 'error', setMessage);
            return;
        }
        try {
            const token = localStorage.getItem('token');
            const response = await fetch('http://localhost:8000/tasks/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`,
                },
                body: JSON.stringify({
                    name: formData.name,
                }),
            });

            const data = await response.json();

            if (response.ok) {
                setTasks((prevTasks) => [...prevTasks, data]);
                setFormData({ name: ''});
            } else {
                showMessage(data.detail || 'Failed to add task', 'error', setMessage);
            }
        } catch (error) {
            console.error('Error adding task:', error);
            alert('Error adding task');
        }
    };

    const handleDelete = async (id: number) => {
        try {
            const token = localStorage.getItem('token');
            const response = await fetch(`http://localhost:8000/tasks/${id}`, {
                method: 'DELETE',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`,
                },
            });

            if (response.ok) {
                setTasks((prevTasks) => prevTasks.filter(task => task.id !== id));
                setCompleteTasks((prevCompleteTasks) => prevCompleteTasks.filter(task => task.id !== id));
            }
        } catch (error) {
            console.error('Error deleting task:', error);
        }
    }

    const handleEdit = (task: { id: number; name: string }) => {
        setEditingTaskId(task.id);
        setEditingTaskName(task.name);
    };

    const handleUpdate = async (id: number) => {
        try {
            const token = localStorage.getItem('token');
            const response = await fetch(`http://localhost:8000/tasks/${id}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`,
                },
                body: JSON.stringify({ name: editingTaskName }),
            });

            if (response.ok) {
                setTasks((prevTasks) => prevTasks.map(task => task.id === id ? { ...task, name: editingTaskName } : task));
                setEditingTaskId(null);
                setEditingTaskName('');
            }
        } catch (error) {
            console.error('Error updating task:', error);
        }

    };

    const handleTick = async (id: number) => {
        const completedTask = tasks.find(task => task.id === id);
        
        if (completedTask) {
            try {
                const token = localStorage.getItem('token');
                const response = await fetch(`http://localhost:8000/tasks/${id}`, {
                    method: 'PUT',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${token}`,
                    },
                    body: JSON.stringify({ name: completedTask.name, completed: true }),
                });

                if (response.ok) {
                    await new Promise(resolve => setTimeout(resolve, 200)); 
                    setTasks(prevTasks => prevTasks.filter(task => task.id !== id));
                    
                    setCompleteTasks(prevCompleteTasks => [...prevCompleteTasks, { ...completedTask, completed: true }]);
                } else {
                    const data = await response.json();
                    showMessage(data.detail || 'Failed to update task', 'error', setMessage);
                }
            } catch (error) {
                console.error('Error updating task:', error);
                alert('Error updating task');
            }
        }
    };

    useEffect(() => {
        const fetchTasks = async () => {
            try {
                const token = localStorage.getItem('token');
                const response = await fetch('http://localhost:8000/tasks/',{
                    method: 'GET',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${token}`,
                    },
                });
                const data = await response.json();
                if (response.ok) {
                    const incompleteTasks = data.filter((item: { completed: boolean }) => !item.completed);
                    setTasks(incompleteTasks);

                    const completeTasks = data.filter((item: { completed: boolean }) => item.completed);
                    setCompleteTasks(completeTasks);

                } else {
                    showMessage('Failed to fetch tasks', 'error', setMessage);
                }
            } catch (error) {
                console.error('Error fetching tasks:', error);
            }
        };

        fetchTasks();
    }, []);

    return (
        <div className="home-container">
            <div className="navbar">
                <img src={logo} alt="logo" className="logo" />
                <a href="/home"><h3>Home</h3></a>
                <a href="/account"><h3>Account</h3></a>
                <a onClick={handleLogout} style={{ background: 'none', border: 'none', cursor: 'pointer' }}>
                    <h3>Logout</h3>
                </a>
            </div>
            <div className="content">
                <div className="todolist">
                    <h1>To Do List</h1>
                    <div className="task-list">
                        {tasks.length > 0 ? (
                            tasks.map((task) => (
                                <li key={task.id} className="task">
                                    {editingTaskId === task.id ? (
                                        <>
                                            
                                            <input
                                                type="text"
                                                value={editingTaskName}
                                                onChange={(e) => setEditingTaskName(e.target.value)}
                                                className='input'
                                            />
                                            <button onClick={() => handleUpdate(task.id)}>OK</button>
                                        </>
                                    ) : (
                                        <>
                                            <input
                                                type="checkbox"
                                                onChange={() => handleTick(task.id)}
                                            />
                                            <span className="task-text">{task.name}</span>
                                            <button className="edit-button" onClick={() => handleEdit(task)}>Edit</button>
                                            <button className="delete-button" onClick={() => handleDelete(task.id)}>Delete</button>
                                        </>
                                    )}
                                </li>
                            ))
                        ) : (
                            <p style = {{ textAlign: 'center'}}>No tasks available.</p>
                        )}
                        <form onSubmit={handleAdd}>
                            <div className="task-input">
                                <input
                                    type="text"
                                    placeholder="Add a new task"
                                    className="input"
                                    value={formData.name}
                                    onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                                    required
                                />
                                <button type='submit'>Add</button>
                            </div>
                        </form>
                    </div>
                </div>
                <div className="completed">
                    <h1>Completed Tasks</h1>
                    <div className="completed-list">
                        {completeTasks.length > 0 ? (
                            completeTasks.map((task) => (
                                <li key={task.id} className="completed-task">
                                    <span className="task-text">{task.name}</span>
                                    <button className="delete-button" onClick={() => handleDelete(task.id)}>Delete</button>
                                </li>
                            ))
                        ) : (
                            <p style = {{ textAlign: 'center'}}>No completed tasks available.</p>
                        )}
                    </div>
                </div>
            </div>
        </div>
    );
}

export default Home