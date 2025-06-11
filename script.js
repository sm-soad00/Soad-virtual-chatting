let ws;
let currentChatUser = null;

function connect() {
    ws = new WebSocket(`ws://${location.host}/ws/${username}`);

    ws.onmessage = (event) => {
        const data = JSON.parse(event.data);
        if(data.from === currentChatUser) {
            addMessage(data.from, data.message);
        }
    };

    ws.onclose = () => {
        console.log("WebSocket disconnected");
    };
}

connect();

function filterUsers() {
    const searchTerm = document.getElementById('search').value.toLowerCase();
    const list = document.getElementById('usersList');
    Array.from(list.children).forEach(li => {
        li.style.display = li.textContent.toLowerCase().includes(searchTerm) ? '' : 'none';
    });
}

function startChat(user) {
    currentChatUser = user;
    document.getElementById('chatWith').textContent = user;
    document.getElementById('chatWindow').style.display = 'block';
    document.getElementById('messages').innerHTML = '';
}

function closeChat() {
    currentChatUser = null;
    document.getElementById('chatWindow').style.display = 'none';
}

function addMessage(from, message) {
    const div = document.createElement('div');
    div.textContent = from + ": " + message;
    document.getElementById('messages').appendChild(div);
}

function sendMessage() {
    const input = document.getElementById('messageInput');
    const msg = input.value.trim();
    if(!msg || !currentChatUser) return;
    ws.send(JSON.stringify({to: currentChatUser, message: msg}));
    addMessage("You", msg);
    input.value = '';
}
