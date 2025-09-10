# ✨ Personal Blog

This is my **personal blog** built with [Hugo](https://gohugo.io/).  
I write about **technology, programming, performance engineering, story telling and personal learnings**.  

---

## 🚀 Features
- ⚡ Fast & optimized static site (Hugo).
- 📝 Easy content writing with Markdown.
- 🖼️ Image optimization & automatic PNG conversion.
- 🔎 SEO-friendly metadata and tags.
- 📱 Responsive design for all devices.
- 📢 Google AdSense ready (monetization support).

---

## 📂 Project Structure
```
blog/
│── content/
│   └── blog/           # Blog posts in Markdown (.md)
│── static/
│   └── images/         # Blog images
│── config.toml         # Hugo configuration
│── README.md
```

---

## 🛠️ Writing a Blog Post
1. Create a new Markdown file inside `content/blog/`:
   ```bash
   hugo new blog/<blog-name>.md
   ```
2. Add metadata (title, description, date, tags, image).
3. Write your blog content in Markdown.
4. Run server locally:
   ```bash
   hugo server -D
   ```
   Visit 👉 `https://akshatjme.github.io/`

---

## 🌍 Deployment
- Build static files:
  ```bash
  hugo
  ```
  Output will be in the `public/` folder.

- Deploy by pushing `public/` to the [`Blog Repo`](https://github.com/akshatjme/public) repo.

---
