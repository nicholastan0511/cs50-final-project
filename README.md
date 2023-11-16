# cs50-final-project
#### Video Demo:  <https://youtu.be/Bl4OKj7l5Nc>
#### Description: 
This web application tracks your daily protein and calorie intake based on the foods you consume. The numbers are determined through your bmi, which is
calculated based on the physical information you hand in to the server right after you register.
    'app.py' handles the server-side of the web application. It imports helper functions from helpers.py, which contains functions that calculate your bmi, determine
your physical status, determine the ranges of daily protein and calorie intake you should consider, and look up nutritional facts based on the csv file from 
'nutrionvalue.org'. 
    'index.js' handles the interactivity part of the website. It utilizes user's local storage to determine which todos are checked and which aren't. It also implements different color schemes to the webpage when user changes the theme.
    'search.html' prints out a table of nutritional facts of foods that you search for.
    'todolist.html' lets you create your simple daily todolist.
    Finally, 'index.html' shows you a couple of statistics of your own physical information and tracks your daily protein and calorie intake based on the foods
    that you add by yourself or alternatively the foods that you add from the server.