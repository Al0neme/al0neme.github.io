/* 空站点兜底：没有任何文章时，Hexo 默认不生成首页和归档页，
 * 此脚本在无文章时生成空列表的 index.html 和 archives/index.html，
 * 保证站点始终可访问。有文章时不产生任何影响。 */
'use strict';

hexo.extend.generator.register('empty-home-fallback', function (locals) {
  if (locals.posts.length > 0) return;

  const emptyPosts = locals.posts.filter(() => false);

  return [
    {
      path: 'index.html',
      layout: ['index'],
      data: {
        posts: emptyPosts,
        total: 0,
        current: 1,
        prev: 0,
        next: 0,
        base: '',
        path: 'index.html'
      }
    },
    {
      path: 'archives/index.html',
      layout: ['archive'],
      data: {
        archive: true,
        posts: emptyPosts,
        total: 0,
        current: 1,
        prev: 0,
        next: 0,
        base: 'archives/',
        path: 'archives/index.html'
      }
    }
  ];
});
