// Create a form input element that listens to click events.
function createInputSubmit(action, value) {
  let input = document.createElement('input');
  input.type = 'submit';
  input.formAction = action;
  input.value = value;
  addEvent(input, 'click', function(e) {
    let el = e.currentTarget;
    el.form.action = el.formAction;
  });
  return input;
}

function createCommentForm(commentNode) {
  var form = document.createElement('form');
  form.id = commentNode.id + '-edit';
  form.dataset.id = commentNode.id;
  form.classList.add('row');
  form.method = 'post';
  form.action = commentNode.querySelector('.edit-comment').href;

  var div = document.createElement('div');
  div.classList.add('col-md-8', 'col-centered');

  var textArea = document.createElement('textarea');
  textArea.classList.add('form-control', 'input-lg');
  textArea.name = 'text';
  textArea.value = commentNode.querySelector('p').innerHTML;

  div.appendChild(textArea);
  div.appendChild(createInputSubmit('cancel', 'Cancel'));
  div.appendChild(createInputSubmit('save', 'Save'));
  form.appendChild(div);

  return form;
}

// Hides a comment and displays a form to edit a given comment, bringing focus
// to the form.
function tryEditComment(e) {
  e.preventDefault();
  let comment = document.getElementById(e.currentTarget.dataset.id);
  let form = createCommentForm(comment);
  addEvent(form, 'submit', editComment);
  comment.style.display = 'none';
  comment.insertAdjacentElement('afterend', form);
  form.focus();
}

// Removes the form to edit a comment, the old comment, and adds the modified
// comment.
function refreshComment(data) {
  let form = document.getElementById(data.id + '-edit');
  let oldComment = form.previousElementSibling;
  let comments = oldComment.parentNode;
  comments.removeChild(form);
  if (!oldComment.previousElementSibling) {
    // This comment is first comment
    comments.removeChild(oldComment);
    comments.insertAdjacentHTML('afterbegin', data.comment);
  } else {
    // This is not the first comment
    let sibling = oldComment.previousElementSibling;
    comments.removeChild(oldComment);
    sibling.insertAdjacentHTML('afterend', data.comment);
  }
  let comment = comments.querySelector('#' + data.id);
  addEvent(comment.querySelector('.delete-comment'), 'click', deleteComment);
  addEvent(comment.querySelector('.edit-comment'), 'click', tryEditComment);
}

// Removes the form to edit a comment and re-displays the original comment.
function putCommentBack(form) {
  form.previousElementSibling.style.display = 'block';
  form.parentNode.removeChild(form);
}

function editComment(e) {
  e.preventDefault();
  var form = e.currentTarget;
  if (form.action.includes('cancel')) {
    putCommentBack(form);
    return;
  }
  var xhr = new XMLHttpRequest();
  xhr.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
      var data = JSON.parse(this.responseText);
      refreshComment(data);
    } 
    // TODO: need to revert changes if there is an error
  };
  xhr.open('POST', '/edit-comment', true);
  var msg = JSON.stringify({
    'id': form.dataset.id,
    'text': form.elements.text.value
  });
  xhr.send(msg);
}

function deleteComment(e) {
  e.preventDefault();
  var xhr = new XMLHttpRequest();
  xhr.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
      var data = JSON.parse(this.responseText);
      if (data.id) {
        var el = document.getElementById(data.id);
        el.parentNode.removeChild(el);
      }
    }
  };
  xhr.open('GET', e.currentTarget.href, true);
  xhr.send();
}

function createComment(e) {
  e.preventDefault();
  var xhr = new XMLHttpRequest();
  xhr.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
      var data = JSON.parse(this.responseText);
      var comments = document.querySelector('.blog-comments');
      comments.insertAdjacentHTML('beforeend', data.comment);
      document.querySelector('form').reset();
      comments.lastChild.scrollIntoView();
      let lc = comments.lastChild;
      addEvent(lc.querySelector('.edit-comment'), 'click', tryEditComment);
      addEvent(lc.querySelector('.delete-comment'), 'click', deleteComment);
    }
  };
  var form = document.querySelector('form');
  xhr.open('POST', form.action, true);
  var msg = JSON.stringify({'text': form.elements.text.value});
  xhr.send(msg);
}

function clickLike(e) {
  e.preventDefault();
  var xhr = new XMLHttpRequest();
  xhr.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
      var response = JSON.parse(this.responseText);
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

(function() {
  let delLinks = document.querySelectorAll('.delete-comment');
  for (let i = 0; i < delLinks.length; i++) {
    addEvent(delLinks[i], 'click', deleteComment);
  }

  let editLinks = document.querySelectorAll('.edit-comment');
  for (let i = 0; i < editLinks.length; i++) {
    addEvent(editLinks[i], 'click', tryEditComment);
  }

  let form = document.querySelector('form');
  if (form.action.includes('create-comment')) {
    addEvent(form, 'submit', createComment);
  }

  addEvent(document.getElementById('like-button'), 'click', clickLike);
})();
