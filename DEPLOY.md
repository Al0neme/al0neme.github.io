# 部署说明（DEPLOY）

本项目是基于 Hexo 8 + 自定义主题 `anime` 的**纯静态博客**，构建产物是普通 HTML/CSS/JS，
可部署到任意静态主机，无需数据库和后端服务。

## 1. 环境要求

| 依赖 | 版本要求 | 说明 |
|------|---------|------|
| Node.js | ≥ 18（推荐 20 LTS） | Hexo 8 运行环境 |
| npm | 随 Node.js 附带 | 包管理 |

## 2. 从备份恢复 / 首次搭建

```bash
cd blog-backup        # 项目目录
npm install           # 按 package-lock.json 还原依赖
npm run server        # 本地预览，默认 http://localhost:4000
```

> 服务器配置在 `_config.yml` 的 `server:` 段（端口 4000、监听 0.0.0.0）。
> 若 4000 被占用：`npx hexo server -p 4001`，或先 `pkill -x hexo` 清理残留进程。

## 3. 构建

```bash
npm run build         # 等价于 npx hexo generate，产物输出到 public/
```

构建产物说明：
- `public/` 内是完整静态站点，**部署时只上传这个目录的内容**
- `public/search.json` 是搜索索引，由 `scripts/search-json.js` 自动生成，前端搜索依赖它
- 主题样式 `style.styl` 会编译为 `css/style.css`

常用命令速查：

| 命令 | 作用 |
|------|------|
| `npm run build` | 生成静态文件到 `public/` |
| `npm run clean` | 清除缓存（db.json）和 public/ |
| `npm run server` | 本地预览 |
| `npx hexo new "标题"` | 新建文章（生成在 `source/_posts/`） |
| `npx hexo new page "页面名"` | 新建独立页面 |

## 4. 部署方式（任选其一）

### 4.1 GitHub Pages（当前使用，al0neme.github.io）

仓库：`al0neme/al0neme.github.io`，采用 **GitHub Actions 自动构建**，推送源码即自动发布。

**一次性设置**（仓库 Settings → Pages → Build and deployment → Source 选 **GitHub Actions**）

**日常发布**：把改动的文件上传/推送到仓库 main 分支即可，Actions 会自动执行：
`npm ci → hexo generate → 发布 public/ 到 Pages`，约 1~2 分钟后生效。

相关文件：
- `.github/workflows/deploy.yml`：构建发布流水线（push 到 main 或手动触发）
- `_config.yml` 中 `url: https://al0neme.github.io`
- `scripts/empty-home-fallback.js`：无文章时保证首页/归档页仍能生成（否则 Pages 会 404）

排查：发布失败时到仓库 **Actions** 页看日志；确认 Pages Source 是 GitHub Actions 而不是分支。

### 4.2 Nginx / 云服务器

```bash
npm run build
scp -r public/* user@your-server:/var/www/blog/
```

Nginx 参考配置：

```nginx
server {
    listen 80;
    server_name your-domain.com;
    root /var/www/blog;
    index index.html;

    location / {
        try_files $uri $uri/ $uri/index.html =404;
    }

    # 静态资源缓存
    location ~* \.(css|js|jpg|png|webp|svg|woff2)$ {
        expires 7d;
    }
}
```

### 4.3 Vercel

1. 将项目推送到 GitHub 仓库
2. Vercel 导入该仓库
3. Build Command: `npm run build`；Output Directory: `public`
4. 部署完成，后续 push 自动重新部署

### 4.4 Netlify

与 Vercel 相同：Build command `npm run build`，Publish directory `public`。

### 4.5 对象存储（OSS / COS / S3）

```bash
npm run build
# 以 aws s3 为例（OSS/COS 有对应 CLI，用法类似）
aws s3 sync public/ s3://your-bucket --delete
```

记得在存储控制台开启「静态网站托管」，首页文档设为 `index.html`。

## 5. 迁移

整个站点（含主题、脚本、文章、图片）都在项目目录内，无任何外部依赖：

```bash
# 旧机器打包（排除生成物）
tar czf blog.tar.gz --exclude=node_modules --exclude=public --exclude=db.json blog/

# 新机器恢复
tar xzf blog.tar.gz && cd blog && npm install && npm run build
```

## 6. 个性化修改入口

| 想改什么 | 改哪里 |
|---------|--------|
| 站点标题 / 作者 / 语言 | `_config.yml` |
| 头像、背景图文件 | `source/images/avatar.jpg`、`background.jpg` |
| 昵称 / 签名 / 个人标签 / 社交链接 / 导航菜单 | `themes/anime/_config.yml` |
| 配色 / 布局 / 移动端样式 | `themes/anime/source/css/style.styl` |
| 搜索逻辑 | `themes/anime/source/js/search.js`、`scripts/search-json.js` |

改完执行 `npm run build` 重新生成即可（本地预览 `npm run server` 会自动热更新）。

## 7. 常见问题

- **构建后页面没变化**：先 `npm run clean` 清缓存再 `npm run build`
- **搜索不出结果**：确认 `public/search.json` 存在；新文章需重新构建才会进索引
- **目录悬浮按钮不见了**：该按钮仅在移动端（≤960px）的文章页/独立页显示，且文章需有 Markdown 标题
- **端口冲突**：`pkill -x hexo` 清理残留进程，或换端口启动
- **字体加载慢**：圆体来自 Google Fonts CDN，国内访问慢时会自动回退系统字体，不影响布局
