// Helper function to add an event listener
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

/* May enable or disable behavior or style on an element by adding a class to
 * an element.
 * @param flag A boolean flag that determines whether a class name should be
 * added to an element.
 * @param id The id of the input element where the class name may be added.
 * @param className The name of the class.
 */
function enableClass(flag, id, className) {
  var cl = document.getElementById(id).classList;
  if (flag && cl.contains(className)
    cl.remove(className);
  else if (!flag && !cl.contains(className)
    cl.add(className);
}

/* Checks that the username is valid.
 * @detail The username is valid if it contains between 3 and 35 alphanumeric
 * characters, a dot, or an underscore, and it begins with a letter.
 * @param formEl The form element where the user input is located.
 * @param id The id of the form element.
 * @param className The name of the class that enables a warning on the
 * username.
 * @return True if the username is valid, false otherwise.
 */
function checkUsername(formEl, id, className) {
  var val = el.elements.user.value;
  var valid = /^[a-z][a-z\d._]{3,35}$/.test(val);
  enableClass(valid, id, className);
  return valid;
}

/* Checks that the password is valid.
 * @detail The password is valid if it contains between 6 and 35 non-white space
 * characters, at least one digit, and at least one letter.
 * @param formEl The element where the password input is located.
 * @param id The id of the input element that may need a warning.
 * @param className The name of the class that may be added as an attribute.
 * @return True if the password is valid, false otherwise.
 */
function checkPassword(formEl, id, className) {
  var val = el.elements.password.value;
  var valid = /^\S{6,35}$/.test(val) && /\d/.test(val) && /[a-z]/.test(val);
  enableClass(valid, id, className);
  return valid;
}

/* Checks the username and passwords are valid.
 * @detail Enables warnings if the username or password are not valid, or
 * submits the form if they are.
 * @param e The event whose default behavior we want to stop.
 */
function checkRegister(e) {
  e.preventDefault();
  validUser = checkUsername(this, 'input-username', 'warning-username');
  validPwd = checkPassword(this, 'input-password', 'warning-password');
  if (usercheck.good && pwdcheck.good)
    this.submit();
}

var form = document.getElementById('register-form');
addEvent(form, 'submit', checkRegister);
