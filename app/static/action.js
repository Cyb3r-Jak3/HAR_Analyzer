function click_function(clicked_id) {
    const xhr = new XMLHttpRequest();
    xhr.open("POST", "/api/entry_choice", true);
    xhr.setRequestHeader("Content-Type", "application/json");

    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4 && xhr.status === 200) {
            parse_entry(JSON.parse(xhr.responseText))
        }
        if (xhr.readyState === 4 && xhr.status === 404) {
            window.location.reload(false)
        }
    }
    const data = JSON.stringify({"entry_id": clicked_id});
    xhr.withCredentials = true;
    xhr.send(data);
}



function parse_entry(response) {
    document.getElementById("secureState").innerText = response["_securityState"];
    document.getElementById("port").innerText = response.connection;
    document.getElementById("IP").innerText = response.serverIPAddress;
    document.getElementById("startDate").innerText = response.startedDateTime;
    document.getElementById("time").innerText = response.time;
    document.getElementById("request_body").innerText = response.request.bodySize;
    document.getElementById("headerSize").innerText = response.request.headersSize;
    document.getElementById("method").innerText = response.request.method;
    document.getElementById("HTTPversion").innerText = response.request.httpVersion;
    document.getElementById("URL").innerText = response.request.url;
    document.getElementById("response_body").innerText = response.response.bodySize;
    document.getElementById("mimeType").innerText = response.response.content.mimeType;
    document.getElementById("response_content").innerText = response.response.content.text;
}

function changeTab(evt, tabName) {
    let i, tabcontent, tablinks;

    tabcontent = document.getElementsByClassName("tabcontent");
    for (i = 0; i < tabcontent.length; i++) {
        tabcontent[i].style.display = "none";
    }

    tablinks = document.getElementsByClassName("tablinks");
    for (i = 0; i < tablinks.length; i++) {
        tablinks[i].className = tablinks[i].className.replace(" active", "");
    }

    document.getElementById(tabName).style.display = "block";
    evt.currentTarget.className += " active";
}