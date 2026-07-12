# News / updates feed

To add a news item, create a new file in this folder, e.g. `2026-09-01-something.md`,
containing **only** a date and a one-line message:

```markdown
---
date: 2026-09-01
---
Paper *Some Title* accepted at [Conference X](https://example.com/) 2026.
```

That's it. The homepage automatically shows the most recent items in
reverse-chronological order, and the [/news/](../_pages/news.html) archive lists
them all. You can use Markdown (including links and *emphasis*) in the one-line body.

This README is ignored by the feed (it has no `date:`).
