function createComment(e) {
  console.log('intercepted request to create a new comment');
  e.preventDefault();
  var xhr = new XMLHttpRequest();
  xhr.onreadystatechange = function() {
    if (xhr.readyState == 4 && xhr.status == 200) {
      var comments = document.querySelector('.blog-comments');
      comments.insertAdjacentHTML('beforeend', xhr.responseText);
      document.querySelector('form').reset();
      comments.lastChild.scrollIntoView();
    }
  };
  var form = document.querySelector('form');
  xhr.open('POST', form.action, true);
  console.log('text: ' + form.elements.text.value);
  var msg = JSON.stringify({'text': form.elements.text.value});
  xhr.send(msg);
}

function clickLike(e) {
  e.preventDefault();
  var xhr = new XMLHttpRequest();
  xhr.onreadystatechange = function() {
    if (xhr.readyState == 4 && xhr.status == 200) {
      var response = JSON.parse(xhr.responseText);
      if (response.add) {
        // Enable red heart and increase likes count
        var cl = document.getElementById('likes-heart').classList;
        cl.add('red-heart');
        cl.remove('normal');
        var el = document.querySelector('.likes-number');
        el.innerText = parseInt(el.innerText, 10) + 1;
      } else if (response.remove) {
        // Disable red heart and decrease likes count
        var cl = document.getElementById('likes-heart').classList;
        cl.remove('red-heart');
        cl.add('normal');
        var el = document.querySelector('.likes-number');
        var count = parseInt(el.innerText, 10);
        // double check that we are not taking number below zero
        if (count) {
          el.innerText = count - 1;
        }
      }
    }
  };
  var href = document.getElementById('like-button').href;
  xhr.open('GET', href, true);
  xhr.send();
}

var form = document.querySelector('form');
if (form.action.includes('create-comment')) {
  console.log('found action create-comment');
  addEvent(form, 'submit', createComment);
}
addEvent(document.getElementById('like-button'), 'click', clickLike);
