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


    // check the previously checked checkboxes and vice versa
    for (let i = 1; i < 5; i++) {  
        let checkBox = document.querySelector(`#checkTodo${i}`);

        checkBoxCheck(checkBox, i);

    }

    // store in local storage the status of the checkboxes and submit the form to the server before the page reloads
    window.addEventListener('beforeunload', function() {
        for (let i = 1; i < 5; i++) {  
        
            let checkBox = document.querySelector(`#checkTodo${i}`);
            console.log(checkBox);

            saveState(checkBox, i);

    }

        document.querySelector('#formTodo').submit();
    })

});


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

