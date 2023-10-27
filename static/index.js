function saveState (checkBox, i) {
    localStorage.removeItem(`checkbox${i}`);
    if (checkBox.checked == true) {
        localStorage.setItem(`checkbox${i}`, 'yes')
    }
    else if (checkBox.checked == false)
        localStorage.setItem(`checkbox${i}`, 'no');

}

function checkBoxCheck (checkBox, i) {
    if (localStorage.getItem(`checkbox${i}`) == 'yes') {
        checkBox.checked = true;
    } else
        checkBox.checked = false;
}

function validateForm () {
    let todoField = document.querySelector('#todoField');
    
    if (!todoField)
        return false;
    else
        return true;
}

// Get the current date
const currentDate = new Date();

// Extract the components of the date
const year = currentDate.getFullYear();
const month = currentDate.getMonth() + 1; // Adding 1 because January is 0
const day = currentDate.getDate();

// Format the date as needed
const formattedDate = year + "-" + month + "-" + day;

document.addEventListener('DOMContentLoaded', function() {

    // turn off the alert if user clicks on search
    document.querySelector('#search').addEventListener('click', function() {
        document.querySelector('.alert').style.display = 'none';
    });

    // show the alert if execute is true and then toggle execute to false so that when the page is refreshed the alert is not shown again (original value display: none)
    if (localStorage.getItem('execute') == 'true') {
        document.querySelector('.alert').style.display = 'block';
        localStorage.setItem('execute', false);
    } 

    // when search results are none toggle the execute to true so that when the page is refreshed the alert is shown via the previous if condition
    if (document.querySelector('#searchButton')) {
        document.querySelector('#searchButton').addEventListener('click', function() {    
            if (!document.querySelector('#tableSearch')) {
                localStorage.setItem('execute', true);
            }
        });
    }

    // check the previously checked checkboxes and vice versa by looking at the localStorage
    let i = 1;
    while (true) {  
        let checkBox = document.querySelector(`#checkTodo${i}`);
       
        i++;

        if (checkBox) {
            
            checkBox.addEventListener('change', function() {
                document.querySelector('#formTodo').submit();
            })

            checkBoxCheck(checkBox, i);
        } else
            break;
    }

    // store in localStorage the status of the checkboxes and submit the form to the server before the page reloads
    window.addEventListener('beforeunload', function() {
        // generally, you don't want to submit the form before unload because if the user have something within the todo field
        // it will automatically be sent as well.
        let k = 1;
        while (true) {
            let checkBox = document.querySelector(`#checkTodo${k}`);
            k++;
            if (checkBox) {
                saveState(checkBox, k);
            } else
                break;
        } 
    })

    // colorize the link or button when the link is clicked or when that page is loaded in todolist section
    if (window.location.pathname === '/todo_completed') {
        document.querySelector('#todo_completed').classList.toggle('linkClicked');
    } else if (window.location.pathname === '/todolist') {
        document.querySelector('#todolist').classList.toggle('linkClicked');
    }
    
    let deadlineButtons = document.querySelectorAll('.addDeadline');

    // after the first button is removed because a deadline is added,
    // the second button becomes the first button or first index of the deadlineButtons array
    // we have to somehow associate the buttons with their respective parents

    // show input to user when add deadline button is clicked
    // associate the button with the parent using the index of the for loop
    for (let i = 0, k = deadlineButtons.length; i < k; i++) {

        let button = deadlineButtons[i];
        
        button.addEventListener('click', function(e) {
            e.preventDefault();

            let id = (button.id).charAt((button.id).length - 1);

            document.querySelector(`#parentDeadline${id}`).removeChild(button);
          
            // add input to the parent td
            let inputDeadline = document.createElement('input');
            inputDeadline.setAttribute('type', 'date');
            inputDeadline.setAttribute('name', `addDeadline${id}`);

            let buttonAdd = document.createElement('button');
            buttonAdd.classList.add('btn', 'btn-primary')
            buttonAdd.setAttribute('type', 'submit')
            buttonAdd.innerHTML = '+';

            document.querySelector(`#parentDeadline${id}`).appendChild(inputDeadline);
            document.querySelector(`#parentDeadline${id}`).appendChild(buttonAdd);

        });
    }

    // let deleteRowButton = document.querySelectorAll('#deleteRow')

    // deleteRowButton.forEach((button) => {
    //     button.addEventListener('clicked', function() {
    //         button.
    //     })
    // });

});



