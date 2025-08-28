import { use, useState } from 'react'
import { useEffect } from 'react'
//import reactLogo from './assets/react.svg'
//import viteLogo from '/vite.svg'
import { useParams } from 'react-router-dom';
import './App.css'

function TodoDetail({todos}) {

  const { id } = useParams();
  const todo = todos.find(todo => todo.id === parseInt(id));

  return (
    <div>
      <h2>{todo.text}</h2>
      <h3>User: {todo.user_id}</h3>
      <h3>Category: {todo.category}</h3>
      <h3>Done: {todo.done?"Yes":"No"}</h3>
      <h3>Date Due: {todo.date_due}</h3>
    </div>
  );
}
export default TodoDetail;