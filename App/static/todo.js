function editTask(todoId) {
    const todoEditButton = document.getElementById(`edit-button-${todoId}`);
    const todoText = document.getElementById('todo-text').value;

    fetch(`/todos/${todoId}`, {
            method: 'PUT',

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


function toggleDone(todoId) {
    const taskCheckbox = document.getElementById(`task-checkbox-${todoId}`);
    const taskDoneField = document.getElementById(`done-${todoId}`);

    fetch(`/todos/${todoId}/check`, {
        method: 'PUT',

        headers: {
            'Content-Type': 'application/json',
        },
        
        }).then(response => response.json())
            .then(data => {
            console.log("Received data:", data);  // check what’s coming from the backend
    
            if (data.success) {
                //console.log("Update successful");

                if(data.done) {
                    taskDoneField.innerHTML = `<span>Yes</span>`;
                    taskCheckbox.innerHTML = `<a style="color: green;" class="material-symbols-outlined" onclick="toggleDone('${todoId}')">check_box</a>`;
                }
                else {
                    taskDoneField.innerHTML = `<span>No</span>`;
                    taskCheckbox.innerHTML = `<a style="color: green;" class="material-symbols-outlined" onclick="toggleDone('${todoId}')">check_box_outline_blank</a>`;
                }

            } else {
                    alert("Couldn't mark task as done.");
            }
        });
}


