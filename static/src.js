var index = 0;
var guess = document.getElementsByName('guess')[0];

document.addEventListener('keydown', logKey);

function logKey(event)
{
    if (event.keyCode == 13)
    {
        document.getElementById('guess_form').submit();
    }
    if (event.keyCode == 8 && index > 0)
    {
        index--;
        document.getElementById('button' + index).innerText = '?';
        guess.value = guess.innerText.substring(0, guess.length - 1);
    }
    if (index <= 4 && event.keyCode >= 65 && event.keyCode <= 90)
    {
        document.getElementById('button' + index).innerText = event.key.toUpperCase();
        guess.value += event.key.toLowerCase();
        index++;
    }
}

function load()
{
    document.getElementById('suggestion_display').innerHTML =
    `<svg class="h-6 w-6 text-indigo-500 fill-current animate-spin inline" viewBox="0 0 20 20" version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
        <path d="M10,3.5 C6.41015,3.5 3.5,6.41015 3.5,10 C3.5,10.4142 3.16421,10.75 2.75,10.75 C2.33579,10.75 2,10.4142 2,10 C2,5.58172 5.58172,2 10,2 C14.4183,2 18,5.58172 18,10 C18,14.4183 14.4183,18 10,18 C9.58579,18 9.25,17.6642 9.25,17.25 C9.25,16.8358 9.58579,16.5 10,16.5 C13.5899,16.5 16.5,13.5899 16.5,10 C16.5,6.41015 13.5899,3.5 10,3.5 Z"></path>
    </svg>`;
    document.getElementById('match_display').innerHTML =
    `<div class="px-20 py-2 flex justify-center cursor-pointer hover:bg-gray-100" onclick="fillWord(this)">
        <svg class="h-6 w-6 text-indigo-500 fill-current animate-spin inline" viewBox="0 0 20 20" version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
            <path d="M10,3.5 C6.41015,3.5 3.5,6.41015 3.5,10 C3.5,10.4142 3.16421,10.75 2.75,10.75 C2.33579,10.75 2,10.4142 2,10 C2,5.58172 5.58172,2 10,2 C14.4183,2 18,5.58172 18,10 C18,14.4183 14.4183,18 10,18 C9.58579,18 9.25,17.6642 9.25,17.25 C9.25,16.8358 9.58579,16.5 10,16.5 C13.5899,16.5 16.5,13.5899 16.5,10 C16.5,6.41015 13.5899,3.5 10,3.5 Z"></path>
        </svg>
    </div>
    `;
}

function redirect(url)
{
    load();
    document.location.href = url;
}

function fillWord(element)
{
    if (element.children.length != 5)
    {
        return;
    }
    for (var child of element.children)
    {
        if (!(child.innerText >= 'A' && child.innerText <= 'Z'))
        {
            return;
        }
    }
    index = 0;
    guess.value = "";
    for (var child of element.children)
    {
        document.getElementById('button' + index).innerText = child.innerText;
        guess.value += child.innerText.toLowerCase();
        index++;
    }
}

function nextChar(element)
{
    if (!(element.innerText >= 'A' && element.innerText <= 'Z'))
    {
        return;
    }
    if (index <= 4)
    {
        document.getElementById('button' + index).innerText = element.innerText;
        guess.value += element.innerText.toLowerCase();
        index++;
    }
}

function delChar()
{
    if (index > 0)
    {
        index--;
        document.getElementById('button' + index).innerText = '?';
        guess.value = guess.innerText.substring(0, guess.length - 1);
    }
}

function changeState(id)
{
    var elem = document.getElementById('button' + id);
    var resp = document.getElementsByName('resp' + id)[0];
    if (resp.value < 2) 
    {
        resp.value++;
    }
    else
    {
        resp.value = 0;
    }
    if (resp.value == 0) 
    {
        elem.classList.remove('bg-green-500');
        elem.classList.add('bg-gray-600');
        elem.classList.remove('hover:bg-green-600');
        elem.classList.add('hover:bg-gray-700');
    }
    if (resp.value == 1) 
    {
        elem.classList.remove('bg-gray-600');
        elem.classList.add('bg-yellow-500');
        elem.classList.remove('hover:bg-gray-700');
        elem.classList.add('hover:bg-yellow-600');
    }
    if (resp.value == 2) 
    {
        elem.classList.remove('bg-yellow-500');
        elem.classList.add('bg-green-500');
        elem.classList.remove('hover:bg-yellow-600');
        elem.classList.add('hover:bg-green-600');
    }
}