/* Helper function to add an event listener.
 * @param el The element we want to add an event listener to.
 * @param event The event we want to listen to.
 * @param callback The callback function to call when the event is transmitted.
 */
function addEvent(el, event, callback) {
  if ('addEventListener' in el) {
    el.addEventListener(event, callback, false);
  } else {
    el['e' + event + callback] = callback;
    el[event + callback] = function() {
      el['e' + event + callback](window.event);
    };
    el.attachEvent('on' + event, el[event + callback]);
  }
}

(function clearWarning() {
  var nameBox = document.getElementById('inputUsername');
  addEvent(nameBox, 'input', function() {
    var cl = document.getElementById('warning-msg').classList;
    if (!cl.contains('hidden-warning')) {
      cl.add('hidden-warning');
    }
  });
})();

// TODO: should only use this on registration form. Need something else for
// login form.
(function doRegister() {
  var form = document.getElementById('account-form');
  addEvent(form, 'submit', function(e) {
    e.preventDefault();
    var xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function() {
      if (xhr.readyState == 4 && xhr.status == 200) {
        var response = JSON.parse(xhr.responseText);
        if (response.success) {
          window.location.assign('/');
        } else {
          document.getElementById('username-taken').innerText = response.user;
          var cl = document.getElementById('warning-msg').classList;
          cl.remove('hidden-warning');
          var nameBox = document.getElementById('inputUsername');
          nameBox.value = '';
          nameBox.focus();
        }
      }
    };
    var user = form.elements.user.value;
    var pwd = form.elements.password.value;
    var msg = JSON.stringify({'user': user, 'password': pwd});
    xhr.open('POST', '/do-register', true);
    xhr.send(msg);
  });
})();
