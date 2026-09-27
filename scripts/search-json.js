/* 生成 search.json 供前端搜索使用（无需第三方插件） */
'use strict';

function stripHtml(html) {
  return String(html || '')
    .replace(/<[^>]+>/g, '')
    .replace(/&nbsp;/g, ' ')
    .replace(/\s+/g, ' ')
    .trim();
}

hexo.extend.generator.register('search-json', function (locals) {
  const data = [];

  locals.posts.sort('date', -1).each(function (post) {
    data.push({
      title: post.title,
      path: hexo.config.root.replace(/\/$/, '') + '/' + post.path,
      text: stripHtml(post.content).slice(0, 500)
    });
  });

  locals.pages.each(function (p) {
    if (!p.title) return;
    data.push({
      title: p.title,
      path: hexo.config.root.replace(/\/$/, '') + '/' + p.path,
      text: stripHtml(p.content).slice(0, 500)
    });
  });

  return {
    path: 'search.json',
    data: JSON.stringify(data)
  };
});
