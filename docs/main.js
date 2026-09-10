$(document).ready(function(){
    // 1. Define your array of allowed dates (Format must match the picker's format)
    const allowedDates = ["2026-09-09", "2026-04-03", "2026-04-13", "2026-04-28", "2026-04-30", "2026-05-19", "2026-05-27", "2026-05-30", "2026-07-04", "2026-07-09"];

    // 2. Initialize the datepicker
    $('#restricted-date').datepicker({
        format: 'yyyy-mm-dd',
        autoclose: true,
        todayHighlight: true,
        beforeShowDay: function(date) {
            let formattedDate = date.getFullYear() + '-' + 
                                ('0' + (date.getMonth() + 1)).slice(-2) + '-' + 
                                ('0' + date.getDate()).slice(-2);
            
            // If the date exists in our allowed array, keep it enabled
            if (allowedDates.includes(formattedDate)) {
                return { enabled: true, classes: 'highlighted-available-day' };
            }
            
            // Otherwise, disable the date
            return { enabled: false };
        }
    });
});

function ShowLog() {
    date = document.getElementById("restricted-date").value;
    section = document.getElementById(date);

    section.removeAttribute("hidden");
}

function HideLog() {
    date = document.getElementById("restricted-date").value;
    section = document.getElementById(date);

    section.setAttribute("hidden", "");
}