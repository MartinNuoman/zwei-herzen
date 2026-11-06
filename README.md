# Zwei Herzen, ein Zuhause

A dependency-free bilingual German/Chinese novel reader. Plain and learning modes share one canonical manuscript. Season 1 (12 chapters and epilogue) was imported verbatim from the author-supplied shared conversations; the synthetic demo remains separate.

这是 Leon 与 Max 小说的静态阅读器。纯净阅读不显示学习标注；互动学习显示单独提供的词语和语法笔记。界面语言切换不会翻译、改写原文。无账号、后端、外部字体、分析或追踪。

## 本地运行与检查

需要 Python 3 和 Node.js 18+，无需安装依赖。在项目目录运行：

```sh
python3 -m http.server 8000
```

打开 http://localhost:8000 。请使用 HTTP 服务，不能直接双击 HTML（浏览器会限制 fetch）。

```sh
npm test
python3 scripts/validate.py
python3 scripts/validate.py --strict
```

普通校验允许已声明缺失的内容，以 MISSING 列出；严格模式在任何原文、标题、标注缺失时失败。无效 JSON、非 UTF-8、重复 ID/顺序、标注定位错误、重叠标注、断开的本地资源链接都会使校验失败。

## 原稿导入

目前 **01–12 和 epilogue 共 13 篇原稿均已从作者提供的分享页面导入**，包含 91 处可点击学习标注和原始词表、语法说明。标题已核实。部分折叠词卡未暴露释义，明确保留为缺少释义；没有编造补充。详见 [导入记录](SOURCE_IMPORT_REPORT.md)。后续修订仍只导入已提供的原文。

1. 从原始对话取得准确文本，保存到 `content/season-01/01.txt` 至 `12.txt`、`epilogue.txt`，UTF-8 编码，段落间空一行。保留中德混排、标点、对话、空白和原有文字。
2. 在 `content/manifest.json` 将对应项 `status` 从 `missing` 改为 `available`。核实未知标题后再填写 `title`；可加 `cefr`。保持稳定 ID、顺序和相对文件路径。
3. 按 CONTRIBUTING.md 单独导入原始学习笔记。没有笔记时允许不创建标注文件，界面显示“学习笔记即将补充”。
4. 运行校验和测试，在两种模式中逐段核对原稿。

本实现将 .txt 作为纯文本安全渲染，不解析 HTML 或 Markdown。原始文本中的 Markdown 符号会逐字显示。原稿的斜体、引用及小节标题通过独立的 `content/formatting.json` 恢复；不解析不受信任的 HTML。空行分段，段内换行、标点及文字保持；CRLF 仅为显示统一成 LF。

`demo/` 是明确标注的合成测试，不是第一季的一部分。`core.js` 负责分段、标注定位和存储适配，`app.js` 负责 UI；`styles.css` 为响应式主题。

## GitHub Pages 部署

仓库：https://github.com/MartinNuoman/zwei-herzen

网站：https://martinnuoman.github.io/zwei-herzen/

作者已确认公开仓库和网站；许可证尚未选择，本项目不默认授予开源许可。

1. 将此目录作为仓库上传到你选择的 GitHub 仓库。不要包含私密对话或尚未授权的稿件。
2. 在仓库 Settings → Pages，选择 Deploy from a branch，分支选择 main，目录选择 `/ (root)`，保存。
3. 使用 GitHub 返回的网址访问。项目站点通常为 `https://用户名.github.io/仓库名/`。资源、内容和模块全部使用相对路径，不要改成以 `/` 开头的根路径。
4. 部署前测试项目子路径：在本目录的父目录运行 `python3 -m http.server 8000`，访问 `http://localhost:8000/zwei_herzen_codex_handoff/`。

无需构建步骤或付费服务。`.nojekyll` 禁用不必要的 Jekyll 处理。`index.html` 中的 Open Graph 标题和描述已提供；发布后填写正式 `og:url`、`og:image`，并按需替换 `assets/favicon.svg` 占位图标。

## 阅读状态与可访问性

主题、界面语言、模式、章节及各章近似段落位置保存到本机 localStorage；不可用时仍可阅读，刷新后状态可能丢失。位置按段落保存，不依赖两种模式不同的页面高度。使用按钮键盘导航、可见焦点和原生 dialog（Escape 关闭，关闭后焦点回到词语）。移动端目录位于阅读区下方。没有可用稿件时不显示虚假的阅读进度。

## 完整第一季资料

- [完整阅读 TXT](Zwei_Herzen_Complete.txt)
- [学习笔记 JSON](Learning_Notes.json)
- [导入与连续性记录](SOURCE_IMPORT_REPORT.md)
- 分章规范源：`content/season-01/`；独立交付目录：`Season_01/`（本地资料包）。

本地 `scripts/import_shared_sources.py` 可从已归档的渲染块重现导入；需要本机 `source-archive/` 证据文件，这些文件不随公开发布包分发。普通阅读、校验和测试不需要此目录。
