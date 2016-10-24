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

  usercheck = checkUsername(this);
  if (usercheck.good)
    msg = 'Welcome ' + usercheck.name + '. Your username is valid. ';
  else
    msg = usercheck.name + ' is not a valid username. ';

  pwdcheck = checkPassword(this);
    msg += 'Your password ' + pwdcheck.name;
  if (pwdcheck.good)
    msg += ' is valid.';
  else
    msg += ' is not valid';

  document.getElementById('response').textContent = msg;
  if (usercheck.good && pwdcheck.good)
    this.submit()
}

var form = document.getElementById('login');
addEvent(form, 'submit', checkRegister);
