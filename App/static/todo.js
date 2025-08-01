function editTask(todoId) {
    const todoEditButton = document.getElementById(`edit-button-${todoId}`);
    const todoText = document.getElementById('todo-text').value;

            fetch(`/todos/${todoId}`, {
            method: 'UPDATE',

            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ id: todoId, text:todoText }),
            }).then(response => response.json())
                .then(data => {
                console.log("Received data:", data);  // check what’s coming from the backend
      
                if (data.success) {
                    //console.log("Update successful");
                    window.location.href = '/todos';
                  } else {
                      alert("Update failed.");
                  }
                });
}

