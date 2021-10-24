const requestUrl = 'http://localhost:8000/api/'


// list_of_orders.html
function deleteOrder(id) {
    fetch(requestUrl + "deleteOrder/" + id, {
        method: 'DELETE',
        credentials: 'same-origin',
        headers: {
            "X-CSRFToken": getCookie("csrftoken")
        }
    })
    .then((response) => {
        console.log(response);
        document.getElementById("order_" + id).remove();
    })
    .catch((err) => console.error(err));
};


document.addEventListener('DOMContentLoaded', () => {

    const ajaxSend = async (formData) => {
        const fetchResp = await fetch(requestUrl + "addOrder/", {
            method: 'POST',
            body: formData
        });
        if (!fetchResp.ok) {
            console.log(formData)
            throw new Error(`Ошибка!`);
        }
        return await fetchResp.text();
    };

    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function (e) {
            e.preventDefault();
            const formData = new FormData(this);
            ajaxSend(formData)
                .then((response) => {
                    const data = JSON.parse(response)
                    var tr_new = document.createElement("tr");
                    tr_new.id = "order_" + data.id;
                    if ('status' in data && data['status'] != 200){
                        alert('Ошибка ввода данных!');
                        form.reset();
                        return 1;
                    }
                    for (const key of Object.keys(data)){
                        console.log(key)
                        var td = document.createElement("td");
                        if (key == 'date') {
                             var newDate = new Date(data[key]);
                             td.textContent = newDate.toLocaleString();
                        }
                        else {
                            td.textContent = data[key];
                        }
                        tr_new.appendChild(td);
                    }
                    var button = document.createElement("button");
                    button.textContent = 'Удалить';
                    button.setAttribute("onclick", "deleteOrder(" + data['id'] + ")");
                    var td_button = document.createElement("td");
                    td_button.appendChild(button);
                    tr_new.appendChild(td_button);

                    var tbody = document.getElementById("main_table").children[1];
                    var tr_add = document.getElementById("order_add");
                    tbody.insertBefore(tr_new, tr_add);

                    form.reset(); // очищаем поля формы
                })
                .catch((err) => console.error(err))
        });
    });

});


// free_list_of_orders.html
async function selectWeek(week) {
    const response = await fetch(requestUrl + "freeOrdersList/" + week.options[week.selectedIndex].value, {
        method: 'GET',
        credentials: 'same-origin',
        headers: {
            "X-Requested-With": "XMLHttpRequest"
        }
    });
    const data = JSON.parse(await response.json());
    console.log(data);
    const days = Object.keys(data);
    for (let day = 0; day < days.length - 2; day++) {
        var tr = document.getElementById("day_" + (day + 1));
        tr.children[0].innerHTML = days[day];
        tr.children[1].innerHTML = data[days[day]]['customers'];
        tr.children[2].innerHTML = data[days[day]]['total_sum'];
    }
    var tr = document.getElementById("results");
    tr.children[0].innerHTML = data[days[8]];
    tr.children[1].innerHTML = data[days[7]];
//    .catch((err) => console.error(err));
};

// Get CSRF token
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}