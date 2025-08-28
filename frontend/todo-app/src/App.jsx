import { use, useState } from 'react'
import { useEffect } from 'react'
import {Routes, Route, Router, Link } from 'react-router-dom';
//import reactLogo from './assets/react.svg'
//import viteLogo from '/vite.svg'
import { useParams } from 'react-router-dom';
import TodoDetail from './TodoDetail.jsx';
import './App.css'

function App() {
  const [todos, setTodos] = useState([]);
  const [students, setStudents] = useState([]);

  useEffect(() => {
    fetch('https://stunning-tribble-4xxr55547g72qpx9-5000.app.github.dev/api/todos', {credentials: "include"})
    .then(response => {
      if(!response.ok) {
        throw new Error('Network response was not ok');
      }
      return response.json();
    })
    .then(data => {
      setTodos(data);
    })
    .catch(error => {
      console.error('There was a problem with the fetch operation:', error);
    });
  }, []);


    useEffect(() => {
    fetch('https://stunning-tribble-4xxr55547g72qpx9-5000.app.github.dev/api/students', {credentials: "include"})
    .then(response => {
      if(!response.ok) {
        throw new Error('Network response was not ok');
      }
      return response.json();
    })
    .then(data => {
      setStudents(data);
    })
    .catch(error => {
      console.error('There was a problem with the fetch operation:', error);
    });
  }, []);


  return (
    <div>
      
      <Routes>
          <Route path="/todos/:id" element={<TodoDetail todos={todos} />} />
      </Routes>

      <h1>Todo List</h1>
      <ul>
        {todos.map(todo => (
          <li key={todo.id}><Link to={`todos/${todo.id}`}>{todo.text}</Link></li>
        ))}
      </ul>

      <h1>Student List</h1>
      <ul>
        {students.map(student => (
          <li key={student.id}>{student.username}</li>
        ))}
      </ul>
    </div>
  );
}
export default App;
