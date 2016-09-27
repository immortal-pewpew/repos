/**
 * @author fdypua
 */


$(document).ready(function(){

function setClock() {
  var today = new Date();

  var currentHours = today.getHours();
  var currentMinutes = today.getMinutes();
  var currentSeconds = today.getSeconds();

  // Pad the minutes and seconds with leading zeros, if required
  currentMinutes = ( currentMinutes < 10 ? "0" : "" ) + currentMinutes;
  currentSeconds = ( currentSeconds < 10 ? "0" : "" ) + currentSeconds;
  var timeOfDay = ( currentHours < 12 ) ? "AM" : "PM";   // Use "AM" or "PM" depending on time of day


  // Convert the hours component to 12-hour format
  currentHours = ( currentHours > 12 ) ? currentHours - 12 : currentHours;
  currentHours = ( currentHours == 0 ) ? 12 : currentHours; // Convert millitary hours to "0" to "12"

  // Compose the string for display
  var currentTime = currentHours + ":" + currentMinutes + ":" + currentSeconds + " " + timeOfDay;
    console.log(currentTime + ' ' + document.getElementById("clock").innerHTML);
  document.getElementById("clock").innerHTML = currentTime;
}

});//end
