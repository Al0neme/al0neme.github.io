# al0neme 的个人博客 ❄

基于 [Hexo](https://hexo.io) + 自定义二次元主题 `anime` 的纯静态个人博客。

## 特性

- 两栏布局：左侧文章/内容，右侧搜索、作者信息、文章目录（点击目录可跳转对应位置，侧栏跟随滚动固定）
- 文章搜索：构建时由 `scripts/search-json.js` 生成 `search.json`，前端纯 JS 过滤，无需任何插件和后端
- 清冷雾蓝配色 + 圆体字体，背景图半透明遮罩

## 本地开发

```bash
npm install        # 安装依赖（只需一次）
npm run server     # 本地预览，访问 http://localhost:4000
```

## 构建

```bash
npm run build      # 产物输出到 public/ 目录
```

## 部署（纯静态，任意主机均可）

> 详细部署步骤见 [DEPLOY.md](./DEPLOY.md)。

`public/` 目录就是完整的静态网站，把它上传到任何静态主机即可：

- **Nginx / 云服务器**：将 `public/` 内容拷到网站根目录（如 `/var/www/blog`）
- **Vercel / Netlify**：导入本仓库，构建命令 `npm run build`，输出目录 `public`
- **对象存储（OSS / COS / S3）**：直接同步上传 `public/` 并开启静态网站托管

## 迁移

整个站点（含主题）都在本目录内，迁移 = 拷贝整个 `blog/` 目录，然后 `npm install` 即可。

## 个性化配置

- **站点信息**（标题、作者、语言）：`_config.yml`
- **头像 / 背景 / 个人资料 / 标签 / 社交链接 / 菜单**：`themes/anime/_config.yml`
- **图片文件**：`source/images/avatar.jpg`、`source/images/background.jpg`
- **写新文章**：`npx hexo new "文章标题"`，文件生成在 `source/_posts/`
