import "@spectrum-web-components/styles/typography.css";

import "@spectrum-web-components/theme/src/themes.js";
import "@spectrum-web-components/theme/theme-dark.js";
import "@spectrum-web-components/theme/theme-light.js";
import "@spectrum-web-components/theme/express/theme-light.js";
import "@spectrum-web-components/theme/express/theme-dark.js";
import "@spectrum-web-components/theme/express/scale-medium.js";
import "@spectrum-web-components/theme/sp-theme.js";

import "@spectrum-web-components/button/sp-button.js";

import "@spectrum-web-components/field-label/sp-field-label.js";
import "@spectrum-web-components/textfield/sp-textfield.js";

import "@spectrum-web-components/tabs/sp-tabs.js";
import "@spectrum-web-components/tabs/sp-tab.js";
import "@spectrum-web-components/tabs/sp-tab-panel.js";

import AddOnSdk from "https://new.express.adobe.com/static/add-on-sdk/sdk.js";
import addOnUISdk from "https://new.express.adobe.com/static/add-on-sdk/sdk.js";

import { GIPHY_API_KEY } from "./config.js";

addOnUISdk.ready.then(async () => {
	console.log("addOnUISdk is ready for use.");
});

function applyTheme(theme = "light") {
	document.querySelector("sp-theme").setAttribute("color", theme);
}

AddOnSdk.ready.then(async () => {
	document.querySelector("sp-theme").style.opacity = "1";

	applyTheme(AddOnSdk.app.ui.theme);
	AddOnSdk.app.on("themechange", (data) => {
		applyTheme(data.theme);
	});

	const userPrompt = document.getElementById("user-prompt");
	const generateBtn = document.getElementById("generate-btn");
	let userPromptValue = "";

	userPrompt.addEventListener("input", (event) => {
		userPromptValue = event.target.value;

		if (userPromptValue.length > 5) {
			generateBtn.removeAttribute("disabled");
		}
	});

	generateBtn.addEventListener("click", async () => {
		startLoading(generateBtn);

		const data = await getTranscript(userPromptValue, stopLoading);
		generateVoiceOver(data[1]);
		addTranscriptToUI(data[2]);
		generateGifs(data[0]);
		generateImages(data[0]);
	});

	AddOnSdk.app.on("dragstart", startDrag);
	AddOnSdk.app.on("dragend", endDrag);
});

/* */
async function getTranscript(userPrompt, callback) {
	const response = await fetch("http://127.0.0.1:5000/generate_transcript", {
		method: "POST",
		body: JSON.stringify({ prompt: userPrompt }),
		headers: {
			"Content-type": "application/json; charset=UTF-8",
		},
	});

	const data = await response.json();
	callback(document.getElementById("generate-btn"));

	return await data.response;
}
/* */

/* */
function addTranscriptToUI(arrayOfTranscript) {
	arrayOfTranscript.forEach((sentence) => {
		const transcriptContainer = document.getElementById(
			"transcript-container"
		);

		const divider = document.createElement("sp-divider");
		transcriptContainer.appendChild(divider);

		const div = document.createElement("div");

		div.style = "--spectrum-card-body-header-height: auto;";
		div.textContent = sentence;

		transcriptContainer.appendChild(div);
	});
}
/* */

/* */
function generateGifs(keywords) {
	const grid = document.getElementById("gifs-grid");
	const card = document.createElement("sp-card");
	loadingCard(card);

	grid.appendChild(card);

	keywords.forEach(async (keyword) => {
		let formattedSearchQuery = keyword.replace(" ", "+");
		let url =
			`https://api.giphy.com/v1/gifs/search?api_key=${GIPHY_API_KEY}&q=` +
			formattedSearchQuery;
		let gifUrl = "";

		try {
			const response = await fetch(url);
			const data = await response.json();
			gifUrl = data.data[0].images.original.url;

			// display the gif
			displayImg(gifUrl, keyword, "gifs-grid");
		} catch (error) {
			console.error("Error fetching Giphy data:", error);
		} finally {
			grid.removeChild(card);
		}
	});
}
/* */

/* */
function generateImages(keywords) {
	const grid = document.getElementById("images-grid");
	grid.innerHTML = "";

	const card = document.createElement("sp-card");
	grid.appendChild(card);

	loadingCard(card);

	keywords.forEach(async (keyword) => {
		let url = `http://127.0.0.1:5000/generate_image?q=${keyword}`;

		try {
			const response = await fetch(url);
			const data = await response.json();

			// console.log(data);
			if (data.error) return;

			const imageUrl = "http://127.0.0.1:5000/serve/" + data.id + ".png";

			// display the image
			displayImg(imageUrl, keyword, "images-grid");
		} catch (error) {
			console.error("Error fetching Unsplash data:", error);
		} finally {
			grid.removeChild(card);
		}
	});
}
/* */

/* */
function generateVoiceOver(transcript) {
	const url = "http://127.0.0.1:5000/create_voiceover";

	fetch(url, {
		method: "POST",
		body: JSON.stringify({ transcript: transcript }),
		headers: {
			"Content-type": "application/json; charset=UTF-8",
		},
	})
		.then((response) => response.json())
		.then((data) => {
			if (data.error) return;
			displayAudioFile();
		})
		.catch((error) => {
			console.error("Error fetching data:", error);
		});
}
/* */

/* */
function displayImg(url, keyword, elementID) {
	const grid = document.getElementById(elementID);
	const card = document.createElement("sp-card");
	const img = document.createElement("img");
	img.width = 135;
	img.src = url;
	img.alt = keyword;
	img.addEventListener("click", addImageToDocument);

	AddOnSdk.app.enableDragToDocument(img, {
		previewCallback: (element) => {
			return new URL(element.src);
		},
		completionCallback: async (element) => {
			return [{ blob: await getBlob(element.src) }];
		},
	});

	card.appendChild(img);

	grid.appendChild(card);
}

function displayAudioFile() {
	const grid = document.getElementById("voiceover-grid");
	const card = document.createElement("sp-card");
	const audio = document.createElement("audio");
	audio.style.margin = "5px 5px 10px 5px";
	audio.controls = true;
	audio.src = "http://127.0.0.1:5000/serve/voiceover.mp3";

	card.appendChild(audio);
	grid.appendChild(card);
}
/* */

/* --- Loading animation start --- */
let intervalId;

function startLoading(triger) {
	triger.setAttribute("disabled", "true");

	let dots = 0;
	intervalId = setInterval(() => {
		dots = (dots + 1) % 4;
		triger.textContent = `Generating${" .".repeat(dots)}`;
	}, 500);
}

function stopLoading(triger) {
	triger.textContent = "Generate";
	triger.removeAttribute("disabled");

	clearInterval(intervalId);
}

function loadingCard(motherElement) {
	const progressBar = document.createElement("div");
	progressBar.classList.add("loader");
	motherElement.appendChild(progressBar);
}
/* --- Loading animation end --- */

/* */
async function getBlob(url) {
	return await fetch(url).then((response) => response.blob());
}

async function addImageToDocument(event) {
	const url = event.currentTarget.src;
	const blob = await getBlob(url);
	AddOnSdk.app.document.addImage(blob);
}

function startDrag(eventData) {
	console.log("The drag event has started for", eventData.element.id);
}

function endDrag(eventData) {
	if (!eventData.dropCancelled) {
		console.log("The drag event has ended for", eventData.element.id);
	} else {
		console.log("The drag event was cancelled for", eventData.element.id);
	}
}
/* */
