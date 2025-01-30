async function getData(){
    const response = await fetch('/api/todos');
    return response.json();
}

function loadTable(todos){
    const table = document.querySelector('#result');

    if(table.innerHTML !== "") {
        table.innerHTML = "";
    }

    for(let todo of todos){
        table.innerHTML += `<tr>
            <td>${todo.id}</td>
            <td>${todo.text}</td>
        </tr>`;
    }
}

async function main(){
    const todos = await getData();
    loadTable(todos);
}

main();