# 内容维护

小说正文和原始学习笔记仅导入作者提供的准确内容，不得补写缺失章节、猜测标题、自动翻译或修订原句。作者已另行授权新增本站学习词卡；新词卡必须独立保存在 `content/learning-editorial.json` 并标明“本站补充”，按 [选词标准](EDITORIAL_POLICY.md) 编辑。版权授权与代码许可证分别确认。

每章只有一个 UTF-8 `.txt` 规范源文件，放在 `content/season-01/`。两种模式读取同一文件。不要把学习注释放入原稿；不要把 demo 文件移动到第一季。原稿存入后，在 manifest 中标为 available。未知标题保留 null。

标注保存为 `content/annotations/01.json` 等，格式如下（下面仅是结构说明，不是可直接使用的小说笔记）：

```json
{
  "chapterId": "01",
  "vocabulary": [
    {"paragraph": 1, "anchor": "准确匹配原文的词语", "occurrence": 1, "zh": "作者提供的中文释义", "en": "Optional supplied English gloss", "example": "可选的已提供例句"}
  ],
  "grammar": [{"zh": "作者提供的语法说明", "en": "Optional supplied English note"}]
}
```

段落和 occurrence 均从 1 开始。段落按空行分隔，不计算空段。occurrence 是该段内同一 anchor 从左往右的第几次非重叠出现。重复词必须明确段落和出现次数；不允许标注重叠。原始笔记没有提供例句、英文解释或语法说明就省略；本站新增解释不得冒充原始笔记，例句必须直接引用规范正文。英文界面缺少英文笔记时会明确提示，原稿不会翻译。

导入后运行 `python3 scripts/validate.py` 和 `npm test`，再在浏览器验证普通/学习模式文字一致、词语弹窗及手机布局。`--strict` 用于完整内容交付前检查，当前第一季原稿完整，预期通过。部分词卡缺少释义会在导入记录中另行说明。
