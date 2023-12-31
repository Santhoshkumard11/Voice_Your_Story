$(document).ready(function () {
  var copyrightId = document.getElementById("copyright");
  var today = new Date();
  var customCopyrightText = `© ${today.getFullYear()} Copyright `;

  copyrightId.innerText = customCopyrightText;
});
