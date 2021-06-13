async function allData(){
    let request = await fetch('/get_info_for_home_page');
    let data = await request.json();

    displayShows(data)
}



function displayShows(someData){
    let contentWrapper = document.querySelector('.index-wrapper');
    let smallCardDiv =
     `<div class="card">
     <h2>Welcome TV show lovers!</h2>
     <p>This great site is happy to bring you your favourite TV show's <i>details</i>.</p>
     </div>`;
    contentWrapper.innerHTML=smallCardDiv;
    let tableCard =
    `<div class="card">
    <table>
    <thead>
    <tr><th>Shows</th></tr>
    </thead>
    <tbody>
    </tbody>
    </table>
    </div>`;
    contentWrapper.insertAdjacentHTML("beforeend", tableCard);
    let tableBody=document.querySelector('tbody');
    someData.forEach((element) => {
        tableBody.innerHTML+=`<tr>
        <td>
        <a href="/show/${element.id}">${element.title}</a>
        </td>
        </tr>`
        
    });
}

allData()

/*
<div class="card">
    <table>
        <thead>
        <tr>
            <th>Shows</th>
        </tr>
        </thead>
        <tbody>
        {% for show in shows %}
        <tr>
            <td><a href="/show/{{ show.id }}">{{ show["title"] }}</a></td>
        </tr>
        {% endfor %}
        </tbody>
    </table>
</div> */