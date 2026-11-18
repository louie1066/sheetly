/* Contact form: validates the fields, then opens the visitor's email app with the message filled in.
 * The site has no server, so nothing is sent from the page itself. */
(function () {
  var EMAIL = "hello@sheetly.example";
  var form = document.getElementById("contactForm");
  var status = document.getElementById("formStatus");
  if (!form) return;

  form.addEventListener("submit", function (e) {
    e.preventDefault();
    var name = form.elements.name.value.trim();
    var from = form.elements.email.value.trim();
    var topic = form.elements.topic.value;
    var message = form.elements.message.value.trim();

    if (!form.checkValidity()) {
      form.reportValidity();
      status.textContent = "Please fill in every field with a valid email address.";
      return;
    }

    var subject = "[Sheetly] " + topic;
    var body = "Name: " + name + "\nEmail: " + from + "\n\n" + message;
    var link = "mailto:" + EMAIL +
      "?subject=" + encodeURIComponent(subject) +
      "&body=" + encodeURIComponent(body);

    status.innerHTML = "";
    status.append("Your email app should open. If it doesn’t, write to ");
    var a = document.createElement("a");
    a.href = "mailto:" + EMAIL;
    a.textContent = EMAIL;
    status.append(a, ".");

    window.location.href = link;
  });
})();
