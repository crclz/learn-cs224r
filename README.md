list staged files, find the largest staged file:

```bash
git diff --cached --name-only | xargs du -h | sort -h
```

list staged files, get total:

```bash
git diff --cached --name-only | xargs du -ch
```

