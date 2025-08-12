const calendarContainer = document.querySelector('.calendar-container');
const calendarHeader = document.querySelector('.calendar-header');
const calendarDates = document.querySelector('.calendar-dates');
const monthDropdown = document.querySelector('.month');
const monthHeader = document.querySelector('#month-header');
const monthNames = [
  "January", "February", "March", "April", "May", "June",
  "July", "August", "September", "October", "November", "December"
];

setCalendarMonthDays(monthDropdown.value, 2025);

monthDropdown.addEventListener("change", (e) => {
     calendarDates.innerHTML = "";

    switch(e.target.value) {
        case e.target.value:
            setCalendarMonthDays(e.target.value, 2025);
            break;
        default:
            setCalendarMonthDays(8, 2025);
            break;
    }
});

function getMonthStartDay(month, year) {
    return new Date(year, month-1, 1).getDay()-1;
}

function getNumDaysInMonth(month, year) {
    if(month==4 || month==6 || month==9 || month==11)
        return 30;
    else if(month==2) {
        if(isLeapYear(year))
            return 29;
        else
            return 28;
    }
    else 
        return 31;
}

function isLeapYear(year) {
    if(year % 4 !== 0)
        return false;
    else {
        if(year % 100 === 0) {
            if(year % 400 === 0) 
                return true;
            else
                return false;
        }
    }
}

async function getTodosByMonth(year, month) {
    const todos = await fetch(`/todos/${year}/${month}`);
    return todos.json();
}

function formatDate(dateString) {
    const date = new Date(dateString);
    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const day = String(date.getDate()+1).padStart(2, '0');
    return `${year}-${month}-${day}`;
}


function sortTodosByDate(todos) {
    let todosByDate = {};
    for(let todo of todos) {
        const dueDate = formatDate(todo.date_due);
        console.log(dueDate)
        if(!todosByDate[dueDate]) {
            todosByDate[dueDate] = [];
        }
        todosByDate[dueDate].push(todo.text);
    }
    return todosByDate;
}

function loadTodos(todos, key) {
    let todoList = document.createElement('ul');
    colors = ['red', 'green', 'blue', 'orange', 'orangered'];

    if(todos[key]) {
        todos[key].forEach(todo => {
            let todoLi = document.createElement('li');
            let span = document.createElement('span');
            span.className = "task-badge";
            span.style.backgroundColor = `${colors[getRandomIntInclusive(0,4)]}`;
            console.log(`${key} ${todo}`);
            span.textContent = `${todo}`;
            todoLi.appendChild(span);
            todoList.appendChild(todoLi);
        });
    }
        
    return todoList;
}

async function setCalendarMonthDays(month, year) {
    const numDays = getNumDaysInMonth(month);
    const prevNumDays = getNumDaysInMonth(month-1);
    const startDay = getMonthStartDay(month, year);

    monthHeader.textContent = `${monthNames[month-1]} ${year}`;
    const fragment = document.createDocumentFragment();

    for(let day=startDay-1; day>=0; day--) {
        const dateCellEmpty = document.createElement('div');
        dateCellEmpty.classList.add('date-cell');
        dateCellEmpty.classList.add('empty');
        dateCellEmpty.textContent = `${prevNumDays-day}`;
        fragment.appendChild(dateCellEmpty);
    }

    for(let day=0; day<numDays; day++) {
        let todos = await getTodosByMonth(year, month);
        let todosByDate = sortTodosByDate(todos);
        const dateKey = formatDate(`${year}-${month}-${day}`);

        const dateCell = document.createElement('div');
        dateCell.id = `todos-${year}-${month}-${day}`;
        dateCell.classList.add('date-cell');

        const todosLink = document.createElement('a');
        todosLink.href = `/todos/${year}_${month}_${day+1}`;
        todosLink.textContent = `${day+1}`;

        dateCell.appendChild(todosLink);

        if(todosByDate[dateKey]) {
            const todoList = loadTodos(todosByDate, dateKey);
            dateCell.appendChild(todoList);
        }

        dateCell.addEventListener("click", () => {
            const days = document.querySelectorAll('.date-cell');
            
            days.forEach(d => {
                d.classList.remove('outline-clicked');
            }); 
            dateCell.classList.add('outline-clicked');
        });

        fragment.appendChild(dateCell);
    }

    calendarDates.appendChild(fragment);
}

function selectDay(day) {
    const days = document.querySelectorAll('.date-cell');
    
    days.forEach(d => {
        d.classList.remove('outline-clicked');
    }); 
    day.classList.add('outline-clicked');
}

function getRandomIntInclusive(min, max) {
    min = Math.ceil(min);
    max = Math.floor(max);
    return Math.floor(Math.random() * (max - min + 1)) + min;
}

