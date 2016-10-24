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
 * @param el The element where the user input is located.
 * @return True if the username is valid, false otherwise.
 */
function checkUsername(el) {
  var response = {name: el.elements.user.value, good: false};
  response.good = /^[a-z][a-z\d._]{3,35}$/.test(response.name);
  return response;
}

function checkPassword(el) {
  var response = {name: el.elements.password.value, good: false};
  response.good = /^\S{6,35}$/.test(response.name)
    && /\d/.test(response.name)
    && /[a-z]/.test(response.name);
  return response;
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
