const calendarContainer = document.querySelector('.calendar-container');
const calendarHeader = document.querySelector('.calendar-header');
const calendarDates = document.querySelector('.calendar-dates');
const monthDropdown = document.querySelector('.month');

monthDropdown.value = 8;
setCalendarMonthDays(monthDropdown, 2025);

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

function setCalendarMonthDays(month, year) {
    const numDays = getNumDaysInMonth(month);
    const prevNumDays = getNumDaysInMonth(month-1);
    const startDay = getMonthStartDay(month, 2025);

    for(let day=startDay-1; day>=0; day--) {
         calendarDates.innerHTML += `
        <div class="date-cell empty">${prevNumDays-day}</div>`;
    }

    for(let day=0; day<numDays; day++) {
        calendarDates.innerHTML += `
        <a href="/todos/${year}_${month}_${day+1}"> <div class="date-cell">${day+1}</div></a>`;
    }
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

