const SpeechRecognition =
  window.SpeechRecognition || window.webkitSpeechRecognition;
const SpeechGrammarList =
  window.SpeechGrammarList || window.webkitSpeechGrammarList;
const SpeechRecognitionEvent =
  window.SpeechRecognitionEvent || window.webkitSpeechRecognitionEvent;
const diagnostic = document.querySelector(".diagnostics");
var recognition = null;
const startRecognitionId = document.getElementById("startRecognition");
const stopRecognitionId = document.getElementById("stopRecognition");
const speechRecognitionTextAreaId = document.getElementById(
  "speechRecognitionTextAreaId"
);
var TranscribeCounter = 0;

window.onload = function () {
  var copyrightId = document.getElementById("copyright");
  var today = new Date();
  var customCopyrightText = `© ${today.getFullYear()} Copyright `;

  copyrightId.innerText = customCopyrightText;

  var colors = ["aqua", "azure", "beige", "bisque", "black", "blue", "brown"];

  recognition = new SpeechRecognition();

  if (SpeechGrammarList) {
    // SpeechGrammarList is not currently available in Safari, and does not have any effect in any other browser.
    // This code is provided as a demonstration of possible capability. You may choose not to use it.
    var speechRecognitionList = new SpeechGrammarList();
    var grammar =
      "#JSGF V1.0; grammar colors; public <color> = " +
      colors.join(" | ") +
      " ;";
    speechRecognitionList.addFromString(grammar, 1);
    recognition.grammars = speechRecognitionList;
  }
  recognition.continuous = true;
  recognition.lang = "en-US";
  recognition.interimResults = false;
  recognition.maxAlternatives = 1;

  recognition.onresult = function (event) {
    try {
      var transcript = event.results[TranscribeCounter][0].transcript;
      console.log(
        "Confidence: " + event.results[TranscribeCounter][0].confidence
      );
      if (typeof transcript !== null) {
        updateTextArea(transcript);
        updateStoryWordCount();
        TranscribeCounter += 1;
      }
    } catch {
      console.error("Error while getting the transcript.");
    }
  };

  recognition.onnomatch = function (event) {
    diagnostic.textContent = "I didn't recognise that color.";
  };

  recognition.onerror = function (event) {
    diagnostic.textContent = "Error occurred in recognition: " + event.error;
  };
};

function updateTextArea(text) {
  speechRecognitionTextAreaId.value += text;
}

function startRecognition() {
  recognition.start();
  console.log("Ready to recognize story text.");
  stopRecognitionId.className = "btn btn-danger";
  startRecognitionId.className = "btn btn-success disabled";
}

function stopRecognition() {
  recognition.stop();
  speechRecognitionTextAreaId.value += ".";
  console.log("Stopped to recognize story text.");
  stopRecognitionId.className = "btn btn-outline-danger disabled";
  startRecognitionId.className = "btn btn-outline-success";
  TranscribeCounter = 0;
}

function clearStoryText() {
  // show a pop up or a warning message before clearing the story or give an option to download the story before deleting
  speechRecognitionTextAreaId.value = "";
  storyWordCountId.innerText = 0;
}

function updateStoryWordCount() {
  storyWordCountId.innerText =
    speechRecognitionTextAreaId.value.split(" ").length;
}

function publishTheStory() {
  var currentDomain = "window.location.origin";
  var urlToHit = `${currentDomain}/api/generate_story`;
  var data = { storyText: speechRecognitionTextAreaId.value };

  try {
    const response = fetch(urlToHit, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
    });

    const result = response.json();
    console.log("Success:", result);
  } catch (error) {
    console.error("Error:", error);
  }
}
