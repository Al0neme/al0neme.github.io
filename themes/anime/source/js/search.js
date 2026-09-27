/* 前端文章搜索：拉取 search.json，按关键词过滤标题与正文 */
(function () {
  var input = document.getElementById('search-input');
  var resultsEl = document.getElementById('search-results');
  var emptyEl = document.getElementById('search-empty');
  if (!input || !resultsEl) return;

  var posts = null;
  var root = (document.querySelector('meta[name="root"]') || {}).content || '/';

  function loadIndex(cb) {
    if (posts) return cb();
    fetch(root + 'search.json')
      .then(function (r) { return r.json(); })
      .then(function (d) { posts = d; cb(); })
      .catch(function () { posts = []; cb(); });
  }

  function escapeHtml(s) {
    return String(s).replace(/[&<>"']/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c];
    });
  }

  function snippet(text, kw) {
    var i = text.toLowerCase().indexOf(kw);
    if (i === -1) return escapeHtml(text.slice(0, 60)) + '…';
    var start = Math.max(0, i - 20);
    var end = Math.min(text.length, i + kw.length + 50);
    return (start > 0 ? '…' : '') +
      escapeHtml(text.slice(start, i)) +
      '<mark>' + escapeHtml(text.slice(i, i + kw.length)) + '</mark>' +
      escapeHtml(text.slice(i + kw.length, end)) +
      (end < text.length ? '…' : '');
  }

  function search() {
    var kw = input.value.trim().toLowerCase();
    if (!kw) {
      resultsEl.hidden = true;
      resultsEl.innerHTML = '';
      emptyEl.hidden = true;
      return;
    }
    loadIndex(function () {
      var hits = posts.filter(function (p) {
        return (p.title && p.title.toLowerCase().indexOf(kw) !== -1) ||
               (p.text && p.text.toLowerCase().indexOf(kw) !== -1);
      }).slice(0, 8);

      if (!hits.length) {
        resultsEl.hidden = true;
        resultsEl.innerHTML = '';
        emptyEl.hidden = false;
        return;
      }
      emptyEl.hidden = true;
      resultsEl.innerHTML = hits.map(function (p) {
        return '<li><a href="' + escapeHtml(p.path) + '">' +
          '<span class="sr-title">' + escapeHtml(p.title) + '</span>' +
          '<span class="sr-snippet">' + snippet(p.text || '', kw) + '</span>' +
          '</a></li>';
      }).join('');
      resultsEl.hidden = false;
    });
  }

  var timer = null;
  input.addEventListener('input', function () {
    clearTimeout(timer);
    timer = setTimeout(search, 200);
  });
  input.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') {
      input.value = '';
      search();
      input.blur();
    }
  });
})();
