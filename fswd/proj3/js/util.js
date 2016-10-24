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

/* Checks that the username is valid.
 * @detail The username is valid if it contains between 3 and 35 alphanumeric
 * characters, a dot, or an underscore, and it begins with a letter.
 * @param el The element where the user input is located.
 * @return True if the username is valid, false otherwise.
 */
function checkUsername(el) {
  var val = el.elements.user.value;
  return /^[a-z][a-z\d._]{3,35}$/.test(val);
}

/* Checks that the password is valid.
 * @detail The password is valid if it contains between 6 and 35 non-white space
 * characters, at least one digit, and at least one letter.
 * @param el The element where the password input is located.
 * @return True if the password is valid, false otherwise.
 */
function checkPassword(el) {
  var val = el.elements.password.value;
  return /^\S{6,35}$/.test(val) && /\d/.test(val) && /[a-z]/.test(val);
}

function checkRegister(e) {
  e.preventDefault();
  var msg;

  var warnUser = 'warning-username';
  var inUserClassList = document.getElementById('input-username').classList;
  usercheck = checkUsername(this);
  if (usercheck.good) {
    if (inUserClassList.contains(warnUser))
      inUserClassList.remove(warnUser);
  }
  else {
    if (!inUserClassList.contains(warnUser))
      inUserClassList.add(warnUser);
  }

  var warnPwd = 'warning-password';
  var inPwdClassList = document.getElementById('input-password').classList;
  pwdcheck = checkPassword(this);
  if (pwdcheck.good) {
    if (inPwdClassList.contains(warnPwd))
      inPwdClassList.remove(warnPwd);
  }
  else {
    if (!inPwdClassList.contains(warnPwd))
      inPwdClassList.add(warnPwd);
  }

  if (usercheck.good && pwdcheck.good)
    this.submit();
}

var form = document.getElementById('register-form');
addEvent(form, 'submit', checkRegister);
