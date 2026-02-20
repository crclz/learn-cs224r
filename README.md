# cs224r

## Suggestion

LLM can help you understand course videos, homework pdfs, formula, math notations, and especially for cs224r.

Gemini-flash (webpage version) is enough.

When writing code, do not directly ask llm to write code for you. Let it check code for you, or give you some hint.

对于cs224r这门课，和大模型聊天会极大帮助你理解视频、homework pdf、公式、数学符号。

用gemini-flash网页版就足够了。豆包大部分时间都还行，有时有点傻逼：问它概念上的东西，它迫不及待地给你吐python代码出来。

写代码的时候，不要直接让大模型给你代码，而是让它检查代码，或者给你提示。


## Homeworks


This is cs224r homework 1-4.

- I'm not sure if my code of homework3 is correct. Other homework is OK, meets requirements.
- Environment problems:
    - Some homework environments are complex, like mojoco. and use many old libraries, only run on Linux.
    - Some tasks still have problems even on Linux.
    - Some slow tasks run on Mac M3, faster than 32-core Linux. But environment must be simple.
- homework4 hint missing a minus sign. Follow hint directly will cause errors.
- I put some answer or picture in .md files

这是cs224r的homework 1-4

- 对于homework3，我不是特别清楚自己做对没有。其他的homework应该没啥问题，基本符合要求。
- 环境问题：
    - 部分homework环境比较复杂例如mojoco，使用了很多停止维护的库，只能在linux上跑。
    - 部分任务即使在linux上跑也会出现兼容性问题。
    - 一些慢的任务，可以在MacM3上跑，比32core的linux机器要快。但环境需要简单。
- homework4 hint中好像少打了一个负号，完全按照hint会有问题
- 一些答案或者截图，在各个.md文件里面



## git cheatsheet

list staged files, find the largest staged file:

```bash
git diff --cached --name-only | xargs du -h | sort -h
```

list staged files, get total:

```bash
git diff --cached --name-only | xargs du -ch
```

