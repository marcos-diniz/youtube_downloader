var sendUrlButton = document.getElementById('send-url-button')
var urlInput = document.getElementById('url-input')
sendUrlButton.addEventListener('click', () => {
	send_url(urlInput.value)
});

function send_url(url) {
	fetch(`/sendurl?url=${url}`, {
		method: 'GET'
	}).then(response => {
		if(!response.ok) {
			throw new Error('http response was not ok');
		}
		return response;
}).then(async response => {
		const json = await response.json();
		if(json['status'] == 'OK'){
			url_element = document.getElementById('url').innerHTML = json['url']
			status_element = document.getElementById('status').innerHTML = json['status']
			status_message_element = document.getElementById('status-message').innerHTML = json['status_message']

		}else{
			status_element = document.getElementById('status').innerHTML = json['status']
			status_message_element = document.getElementById('status-message').innerHTML = json['status_message']
		};
		console.log(json);
	    }).catch(err => console.log('Error!', err))
        .finally(() => console.log('Finally!'))
};