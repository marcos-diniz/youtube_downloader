var sendUrlButton = document.getElementById('send-url-button')
var urlInput = document.getElementById('url-input')
sendUrlButton.addEventListener('click', () => {
	if (isYoutubeUrl(urlInput.value)){
		hideSearchPage()
		sendUrl(urlInput.value)
		createYoutubeIframe(urlInput.value)
	}else{
		openModal('Youtube URL invalid!')
          
	};
});

function sendUrl(url) {
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
			createDownloadPage(json);
			document.getElementById('search-page').classList.add('hide')
			document.getElementById('title').classList.add('hide')
		}else{
			openModal(json['status_message'])
		};
	    }).catch(err => openModal(err))
        .finally(() => console.log('Finally!'))
};


function hideSearchPage(){
	document.getElementById('search-page').classList.add('hide')
    document.getElementById('title').classList.add('hide')
};

function htmlToElement(html) {
    videoContainerE = document.getElementById('video-container');
    videoContainerE.textContent = '';
    var template = document.createElement('template');
    html = html.trim();
    template.innerHTML = html;
    var iframe_element = template.content.firstChild;
    iframe_element.width = 400
    iframe_element.height = 260
    videoContainerE.appendChild(iframe_element);
};
function isYoutubeUrl(url){
	var youtube_urls = ['youtube.com', 'youtu.be', 'www.youtube.com'];
	//var host = url.match(/^https?\:\/\/([^\/:?#]+)(?:[\/:?#]|$)/i);
	try {
	var host = new URL(url).hostname;
	}catch(err){
		//error 
		return false};
	if(youtube_urls.indexOf(host) >= 0 ){
		return true;
	}else{
		return false;
	}
};


function createYoutubeIframe(url) {
	fetch(`https://www.youtube.com/oembed?url=${url}&format=json`, {
		method: 'GET'
	}).then(response => {
		if(!response.ok) {
			throw new Error('http response was not ok');
		}
		return response;
}).then(async response => {
	const json = await response.json();
	htmlToElement(json['html']);
}).catch(err => console.log('Error!', err))
.finally(() => console.log('finally'))
};


function createFormatSelectOptions(options){
	formatSelectElement = document.getElementById('format-select');
	for (var key in options){
		if (options.hasOwnProperty(key)){
			var option = options[key];
			var optionElement = document.createElement('option');
			optionElement.value = option['download_url'];
			var fileSize = bytesToSize(parseFloat(option['filesize']));
			optionElement.innerHTML = `${option['mime_type']} ${option['quality']} (${fileSize})`;
			formatSelectElement.appendChild(optionElement);
		}else{};
}};

function createDownloadPage(json){
        document.getElementById('download-page').classList.remove("hide");
        formatSelect = document.getElementById('formatSelect');
        options = json['download_options'];
        createFormatSelectOptions(options)
        document.getElementById('download-link').innerHTML = 'Download'


};

function downloadFile() {
        document.getElementById("download-link").href = document.getElementById("format-select").value;
};

function bytesToSize(bytes) {
    var i = Math.floor( Math.log(bytes) / Math.log(1024) );
    return ( bytes / Math.pow(1024, i) ).toFixed(2) * 1 + ' ' + ['B', 'kB', 'MB', 'GB', 'TB'][i];
};


var modal = document.getElementById("myModal");
var span = document.getElementsByClassName("close")[0];

function openModal(message){
	modal.style.display = "block"
	document.getElementById('modal-message').innerHTML = message
};

span.onclick = function() {
  modal.style.display = "none";
};
window.onclick = function(event) {
  if (event.target == modal) {
    modal.style.display = "none";
  }
};