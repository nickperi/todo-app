function makeTaskEditable(todoId) {
    const todoTextInput = document.getElementById(`task-${todoId}-input`);
    const todoEditButton = document.getElementById(`edit-button-${todoId}`);
    todoEditButton.innerHTML = `<a style="color: darkcyan;" class="material-symbols-outlined" onclick="editTask('${todoId}')">save</a>`;
    todoTextInput.readOnly = false;
    todoTextInput.select();
}

function editTask(todoId) {
    const todoTextInput = document.getElementById(`task-${todoId}-input`);
    const todoText = todoTextInput.value;
    const todoEditButton = document.getElementById(`edit-button-${todoId}`);

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
                    todoEditButton.innerHTML = `<a style="color: orangered;" class="material-symbols-outlined" onclick="makeTaskEditable('${todoId}')">edit</a>`;
                    todoTextInput.readOnly = true;
            
                  } else {
                      alert("Update failed.");
                  }
                });
}


function toggleDone(todoId) {
    const taskCheckbox = document.getElementById(`task-checkbox-${todoId}`);
    const taskDoneField = document.getElementById(`done-${todoId}`);
    const taskCompletedField = document.getElementById(`task-completed-${todoId}`);

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
                    taskCheckbox.innerHTML = `<a style="color:limegreen;" class="material-symbols-outlined" onclick="toggleDone('${todoId}')">check_box</a>`;
                    taskCompletedField.innerHTML = `${data.date_completed}`;
                }
                else {
                    taskDoneField.innerHTML = `<span>No</span>`;
                    taskCheckbox.innerHTML = `<a style="color:cadetblue;" class="material-symbols-outlined" onclick="toggleDone('${todoId}')">check_box_outline_blank</a>`;
                    taskCompletedField.innerHTML = "_";
                }

            } else {
                    alert("Couldn't mark task as done.");
            }
        });
}


