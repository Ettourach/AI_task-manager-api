/**
 * TaskList Component
 * 
 * Displays a list of tasks with filtering and CRUD operations.
 * 
 * Usage:
 * import TaskList from './components/TaskList';
 * <TaskList />
 */

import { useState, useEffect } from 'react';
import apiClient from '../api/apiClient';

const TaskList = () => {
  const [tasks, setTasks] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [newTaskTitle, setNewTaskTitle] = useState('');

  useEffect(() => {
    fetchTasks();
  }, []);

  const fetchTasks = async () => {
    try {
      setLoading(true);
      const response = await apiClient.get('/tasks/');
      setTasks(response.data);
      setError(null);
    } catch (err) {
      setError('Failed to fetch tasks');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const createTask = async (e) => {
    e.preventDefault();
    if (!newTaskTitle.trim()) return;

    try {
      const response = await apiClient.post('/tasks/', { title: newTaskTitle });
      setTasks([...tasks, response.data]);
      setNewTaskTitle('');
    } catch (err) {
      setError('Failed to create task');
      console.error(err);
    }
  };

  const toggleComplete = async (task) => {
    try {
      const response = await apiClient.patch(`/tasks/${task.id}/`, {
        completed: !task.completed,
      });
      setTasks(tasks.map((t) => (t.id === task.id ? response.data : t)));
    } catch (err) {
      setError('Failed to update task');
      console.error(err);
    }
  };

  const deleteTask = async (taskId) => {
    try {
      await apiClient.delete(`/tasks/${taskId}/`);
      setTasks(tasks.filter((t) => t.id !== taskId));
    } catch (err) {
      setError('Failed to delete task');
      console.error(err);
    }
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center p-8">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500"></div>
      </div>
    );
  }

  return (
    <div className="max-w-2xl mx-auto p-4">
      <h1 className="text-2xl font-bold mb-6">My Tasks</h1>
      
      {error && (
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
          {error}
        </div>
      )}

      <form onSubmit={createTask} className="mb-6">
        <div className="flex gap-2">
          <input
            type="text"
            value={newTaskTitle}
            onChange={(e) => setNewTaskTitle(e.target.value)}
            placeholder="Add a new task..."
            className="flex-1 px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
          <button
            type="submit"
            className="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition-colors"
          >
            Add
          </button>
        </div>
      </form>

      <ul className="space-y-2">
        {tasks.map((task) => (
          <li
            key={task.id}
            className="flex items-center gap-3 p-4 bg-white rounded-lg shadow hover:shadow-md transition-shadow"
          >
            <input
              type="checkbox"
              checked={task.completed}
              onChange={() => toggleComplete(task)}
              className="h-5 w-5 rounded border-gray-300 text-blue-500 focus:ring-blue-500"
            />
            <span
              className={`flex-1 ${
                task.completed ? 'line-through text-gray-400' : ''
              }`}
            >
              {task.title}
            </span>
            {task.is_overdue && (
              <span className="px-2 py-1 text-xs bg-red-100 text-red-600 rounded">
                Overdue
              </span>
            )}
            {task.tags?.map((tag) => (
              <span
                key={tag.id}
                className="px-2 py-1 text-xs bg-gray-100 rounded"
              >
                {tag.name}
              </span>
            ))}
            <button
              onClick={() => deleteTask(task.id)}
              className="text-red-500 hover:text-red-700"
            >
              Delete
            </button>
          </li>
        ))}
      </ul>

      {tasks.length === 0 && (
        <p className="text-center text-gray-500 py-8">
          No tasks yet. Create one above!
        </p>
      )}
    </div>
  );
};

export default TaskList;
