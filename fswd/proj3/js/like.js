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

addEvent(document.getElementById('like-button'), 'click', clickLike);
