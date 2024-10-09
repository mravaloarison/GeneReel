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

function applyTheme(theme = "light") {
	document.querySelector("sp-theme").setAttribute("color", theme);
}

AddOnSdk.ready.then(async () => {
	document.querySelector("sp-theme").style.opacity = "1";

	applyTheme(AddOnSdk.app.ui.theme);
	AddOnSdk.app.on("themechange", (data) => {
		applyTheme(data.theme);
	});

	console.log("AddOnSdk is ready for use.");

	const userPrompt = document.getElementById("user-prompt");
	const generateBtn = document.getElementById("generate-btn");
	let userPromptValue = "";

	userPrompt.addEventListener("input", (event) => {
		userPromptValue = event.target.value;

		if (userPromptValue.length > 5) {
			generateBtn.removeAttribute("disabled");
		}
	});

	generateBtn.addEventListener("click", () => {
		startLoading(generateBtn);
		runTask(userPromptValue);
	});
});

function startLoading(triger) {
	triger.setAttribute("disabled", "true");

	let dots = 0;
	setInterval(() => {
		dots = (dots + 1) % 4;
		triger.textContent = `Generating${" .".repeat(dots)}`;
	}, 500);
}

async function runTask(prompt) {}
