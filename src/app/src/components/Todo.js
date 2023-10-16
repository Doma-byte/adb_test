import React, { useState, useEffect } from 'react';
import "./Todo.css";
import axios from 'axios';

function Todo() {
    const [todos, setTodos] = useState([]);
    const [newTodo, setNewTodo] = useState('');

    useEffect(() => {
        fetchTodos();
    }, []);

    const fetchTodos = () => {
        axios.get('http://localhost:8000/todos/')
            .then((response) => setTodos(response.data))
            .catch((err) => console.error("Error fetching TODOs: ", err));
    }

    const handleTodoChange = (event) => {
        setNewTodo(event.target.value);
    };

    const handleAddTodo = (e) => {
        e.preventDefault();
        axios.post('http://localhost:8000/todos/', { description: newTodo })
            .then((response) => {
                if (response.status === 201) {
                    alert('Successfully Todo created');
                    setNewTodo('');
                    fetchTodos();
                } else {
                    alert('Error occurred');
                }
            })
            .catch((err) => console.error('Error creating TODO: ', err));
    }

    return (
        <div className='Todo'>
            <div>
                <h1>List of TODOs</h1>
                {todos.length > 0 ? (
                    <ul>
                        {todos.map((todo) => (
                            <li key={todo._id}>{todo.description}</li>
                        ))}
                    </ul>
                ) : (
                    <p>No TODOs found.</p>
                )}
            </div>
            <div>
                <h1>Create a ToDo</h1>
                <form onSubmit={handleAddTodo}>
                    <div>
                        <label htmlFor="todo">ToDo: </label>
                        <input
                            type="text"
                            id="todo"
                            value={newTodo}
                            onChange={handleTodoChange}
                        />
                    </div>
                    <div style={{ marginTop: '5px' }}>
                        <button type="submit">Add ToDo!</button>
                    </div>
                </form>
            </div>
        </div>
    );
};

export default Todo;
