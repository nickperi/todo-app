const calendarContainer = document.querySelector('.calendar-container');
const calendarHeader = document.querySelector('.calendar-header');
const calendarDates = document.querySelector('.calendar-dates');
const monthDropdown = document.querySelector('.months-dropdown');
const monthHeader = document.querySelector('#month-header');

const monthNames = [
  "January", "February", "March", "April", "May", "June",
  "July", "August", "September", "October", "November", "December"
];

const currentYear = parseInt(document.getElementById('current-year').textContent);
const currentDay = new Date().getDate();
const currentMonthName = document.getElementById('current-month').textContent;

setCalendarMonthDays(parseInt(monthDropdown.value), currentYear);

calendarDates.addEventListener("click", (e) => {
    const days = document.querySelectorAll('.date-cell');

    if(e.target.classList.contains('date-cell')) {
        days.forEach(d => {
            d.classList.remove('outline-clicked');
        }); 
        e.target.classList.add('outline-clicked');
    }
});

calendarDates.addEventListener("dblclick", (e) => {
    const days = document.querySelectorAll('.date-cell');

    if(e.target.classList.contains('date-cell')) {
        days.forEach(d => {
            d.classList.remove('outline-clicked');
        }); 
        e.target.classList.add('outline-clicked');
        window.location.href = document.getElementById(e.target.id).querySelector('a').href;
    }
});

monthDropdown.addEventListener("change", (e) => {
     calendarDates.innerHTML = "";

    switch(e.target.value) {
        case e.target.value:
            setCalendarMonthDays(parseInt(e.target.value), currentYear);
            break;
        default:
            setCalendarMonthDays(8, currentYear);
            break;
    }
});


function getMonthValue(months, monthName) {
    for(let i=0; i<months.length; i++) {
        if(monthNames[i] === monthName) 
            return i+1;
    }
    return 0;
}

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


function sortTodosByDate(todos) {
    let map = {};
    for(let todo of todos) {
        const dueDate = todo.date_due;
        //console.log(dueDate);
        console.log(todo.date_due + " " + todo.category);
        (map[dueDate] ||= []).push(todo);
    }
    return map;
}

function loadTodos(todos, key) {
    let todoList = document.createElement('ul');
    todoList.className = 'todo-list';
    const categoryColors = {
        work:'#0D6EFD', 
        personal:'#198754', 
        urgent:'#DC3545', 
        reminder:'#ff6600ef', 
        school: "#a3118bff",
        shopping: "#E91E63", 
        'job application': "#4837B5",
        other: "#9E9E9E"
    };

    if(todos[key]) {
        todos[key].forEach(todo => {
            let todoLi = document.createElement('li');
            let span = document.createElement('span');
            span.className = "task-badge";
            span.style.backgroundColor = `${categoryColors[todo.category]}`;
            span.textContent = `${todo.category}`;
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

    const currentMonth = getMonthValue(monthNames, currentMonthName);

    monthHeader.innerHTML = `<span id ="current-month">${monthNames[month-1]}</span> 
            <span id="current-year">${year}</span>`;

    const fragment = document.createDocumentFragment();
    const todos = await getTodosByMonth(year, month);
    const todosByDate = sortTodosByDate(todos);

    for(let day=startDay-1; day>=0; day--) {
        const dateCellEmpty = document.createElement('div');
        dateCellEmpty.classList.add('date-cell');
        dateCellEmpty.classList.add('empty');
        dateCellEmpty.textContent = `${prevNumDays-day}`;
        fragment.appendChild(dateCellEmpty);
    }

    for(let day=0; day<numDays; day++) {
        const dateKey = `${year}-${String(month).padStart(2, '0')}-${String(day+1).padStart(2, '0')}`;

        const dateCell = document.createElement('div');
        const dayText = document.createElement('span');
        dayText.className = 'day-text';
        dayText.textContent = `${day+1} `;
        dateCell.id = `todos-${year}-${month}-${day}`;
        dateCell.classList.add('date-cell');

        const todosLink = document.createElement('a');
        todosLink.href = `/todos/${year}_${month}_${day+1}`;

        if(day===currentDay-1 && month===currentMonth && year===currentYear) {
            dayText.style.backgroundColor = "springgreen";
            dayText.style.color = "navy";
        }
        dateCell.appendChild(dayText);

        if(todosByDate[dateKey]) {
            const todoList = loadTodos(todosByDate, dateKey);
            todoList.className = "todo-list";
            dateCell.appendChild(todoList);
        }

        dateCell.appendChild(todosLink);
        fragment.appendChild(dateCell);
    }

    calendarDates.appendChild(fragment);
}


function getRandomIntInclusive(min, max) {
    min = Math.ceil(min);
    max = Math.floor(max);
    return Math.floor(Math.random() * (max - min + 1)) + min;
}

