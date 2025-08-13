const calendarContainer = document.querySelector('.calendar-container');
const calendarHeader = document.querySelector('.calendar-header');
const calendarDates = document.querySelector('.calendar-dates');
const monthDropdown = document.querySelector('.months-dropdown');
const monthHeader = document.querySelector('#month-header');
const currentYear = parseInt(document.getElementById('current-year').textContent);
console.log("current year: " + currentYear);

const monthNames = [
  "January", "February", "March", "April", "May", "June",
  "July", "August", "September", "October", "November", "December"
];

setCalendarMonthDays(monthDropdown.value, currentYear);

calendarDates.addEventListener("click", (e) => {
    const days = document.querySelectorAll('.date-cell');

    if(e.target.classList.contains('date-cell')) {
        days.forEach(d => {
            d.classList.remove('outline-clicked');
        }); 
        e.target.classList.add('outline-clicked');
    }
});

monthDropdown.addEventListener("change", (e) => {
     calendarDates.innerHTML = "";

    switch(e.target.value) {
        case e.target.value:
            setCalendarMonthDays(e.target.value, currentYear);
            break;
        default:
            setCalendarMonthDays(8, currentYear);
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


function sortTodosByDate(todos) {
    let map = {};
    for(let todo of todos) {
        const dueDate = todo.date_due;
        //console.log(dueDate);
        (map[dueDate] ||= []).push(todo.text);
    }
    return map;
}

function loadTodos(todos, key) {
    let todoList = [];
    const colors = ['green', 'orangered', 'blue', 'orange', 'red'];
    let i=0;

    if(todos[key]) {
        todos[key].forEach(todo => {
            todoList += `<li><span class="task-badge" style="background-color:${colors[i]}">${todo}</span></li>`;
            i++;
            if(i == colors.length)
                i=0;
            //console.log(`${key} ${todo}`);
        });
    }
        
    return todoList;
}

async function setCalendarMonthDays(month, year) {
    const numDays = getNumDaysInMonth(month);
    const prevNumDays = getNumDaysInMonth(month-1);
    const startDay = getMonthStartDay(month, year);

    monthHeader.textContent = `${monthNames[month-1]} ${year}`;
    let calendarDays = "";
    const todos = await getTodosByMonth(year, month);
    const todosByDate = sortTodosByDate(todos);

    for(let day=startDay-1; day>=0; day--) {
        calendarDays += `<div class="date-cell empty">${prevNumDays-day}</div>`;
    }

    for(let day=0; day<numDays; day++) {
        const dateKey = `${year}-${String(month).padStart(2, '0')}-${String(day+1).padStart(2, '0')}`;

        if(todosByDate[dateKey]) {
            const todoList = loadTodos(todosByDate, dateKey);
            calendarDays += `<div class="date-cell id="todos-${year}-${month}-${day}">
            <a href = "/todos/${year}_${month}_${day+1}">${day+1}</a>
        <ul>${todoList}</ul> </div>`;
        }

        else {
            calendarDays += `<div class="date-cell id="todos-${year}-${month}-${day}">
            <a href = "/todos/${year}_${month}_${day+1}">${day+1}</a>
        </div>`;
        }
    }

    calendarDates.innerHTML = calendarDays;
}

function getRandomIntInclusive(min, max) {
    min = Math.ceil(min);
    max = Math.floor(max);
    return Math.floor(Math.random() * (max - min + 1)) + min;
}

