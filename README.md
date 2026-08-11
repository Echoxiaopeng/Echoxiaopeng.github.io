# VLA 求职展示站（GitHub Pages 骨架）

静态个人站，面向 **Vision-Language-Action / 具身智能** 求职。适合把链接放在简历上。

## 本地预览

用浏览器直接打开 `index.html`，或在本目录启动静态服务：

```bash
npx --yes serve .
```

## 发布到 GitHub Pages

### 方案 A：用户主站（简历链接最短）

1. 把仓库命名为 `你的用户名.github.io`
2. 推送到 GitHub，默认分支 `main`
3. 仓库 Settings → Pages → Source 选 `Deploy from a branch`，分支 `main` / `/ (root)`
4. 几分钟后访问：`https://你的用户名.github.io`

### 方案 B：项目站（当前文件夹名 `portfolio`）

1. 仓库名可用 `portfolio`
2. 同样开启 Pages（`main` / root）
3. 访问：`https://你的用户名.github.io/portfolio/`

## 你需要替换的内容

| 位置 | 说明 |
|------|------|
| `Your Name` | 姓名 / 英文名 |
| 求职方向文案 | 更贴合你的目标 JD |
| 三个项目占位 | 真实项目描述、技术栈、链接 |
| 联系方式 | Email / GitHub / Scholar |
| `resume.pdf` | 放入本目录后，「简历 PDF」按钮即可下载 |

## 文件结构

```
portfolio/
├── index.html
├── styles.css
├── script.js
├── resume.pdf   （自行添加）
└── README.md
```
