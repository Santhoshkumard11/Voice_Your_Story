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
const diagnosticMessageId = document.getElementById("diagnosticMessageId");
var TranscribeCounter = 0;

var ErrorNoCharInStory =
  "Type or narrate at least CharCount more characters to your story before submitting";

var MinStoryCharCount = 200;

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
      showToast("Error while getting the transcript.", "warning");
    }
  };

  recognition.onnomatch = function (event) {
    showToast("Can't recognize the audio - speak again!", "warning");
  };

  recognition.onerror = function (event) {
    showToast("Error occurred in recognition: " + event.error, "warning");
  };
};

function updateTextArea(text) {
  speechRecognitionTextAreaId.value += text + " ";
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
  var splittedText = speechRecognitionTextAreaId.value.split(" ");
  var splittedTextLength = splittedText.length;

  if (splittedTextLength == 1 && splittedText[0] == "") {
    storyWordCountId.innerText = 0;
  } else {
    storyWordCountId.innerText =
      speechRecognitionTextAreaId.value.split(" ").length;
  }
}

function showToast(text, color) {
  var toastBody = document.getElementById("toastBody");
  toastBody.innerHTML = text;
  toastDiv.className = `bg-${color}`;

  $(".toast").toast("show");
}

function publishTheStory() {
  var currentDomain = window.location.origin;
  var urlToHit = `${currentDomain}/api/generate_story?code=gLEk2e_h0lUQ1taT_vS8nVrbfknftPxr2mqW4HGJwoePAzFux-Yvxg==`;

  if (speechRecognitionTextAreaId.value.length < MinStoryCharCount) {
    var errorText = ErrorNoCharInStory.replace(
      "CharCount",
      MinStoryCharCount - speechRecognitionTextAreaId.value.length
    );
    diagnosticMessageId.innerText = errorText;
    showToast(errorText, "warning");
    return;
  } else {
    diagnosticMessageId.innerText = "Generating content....";
  }

  var data = { storyText: speechRecognitionTextAreaId.value };
  showToast("Sent the text for story generation!", "success");
  try {
    fetch(urlToHit, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
    })
      .then(function (response) {
        return response.json();
      })
      .then(function (data) {
        showToast("Submitted story!", "success");
        console.log("Success:", data);
        updateStoryUrl(data["story_link"]);
      })
      .catch(function (err) {
        console.error("Error:", err);
        showToast("Error while trying to parse the output!", "warning");
      });
  } catch (error) {
    console.log(`Error while trying to generate story - ${error}`);
    diagnosticMessageId.innerText = "Unable to generate story!";
    showToast("Unable to generate story!!!", "danger");
  }
}

function updateStoryUrl(storyLink) {
  diagnosticMessageId.innerHTML = `<b> <a href="${storyLink}" target="_blank">Story Link</a> </b>`;
}
