"use strict";

function applyDate(el) {
    let date = new Date();
    date.setYear(1998);

    var day = date.getDate();
    var month = date.getMonth();
    var year = date.getFullYear();
    var hours = date.getHours();
    var minutes = date.getMinutes();

    var dayString = day.toString();
    var monthString = month.toString();
    var hoursString = hours.toString();
    var minutesString = minutes.toString();

    // Add the ordinal suffix to the day string (e.g. "1" becomes "1st")
    if (day === 1 || day === 21 || day === 31) {
      dayString += "st";
    } else if (day === 2 || day === 22) {
      dayString += "nd";
    } else if (day === 3 || day === 23) {
      dayString += "rd";
    } else {
      dayString += "th";
    }

    // Add the month name to the month string (e.g. "0" becomes "January")
    var monthNames = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];
    monthString = monthNames[month];

    // Add a leading zero to the hours and minutes strings if necessary
    if (hours < 10) {
      hoursString = "0" + hoursString;
    }
    if (minutes < 10) {
      minutesString = "0" + minutesString;
    }

    // Format the date and time as a string
    var dateString = dayString + " of " + monthString + ", " + year + ", " + hoursString + ":" + minutesString + " PM";
    el.innerHTML = dateString;
}