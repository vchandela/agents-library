---
max_turns: 8
allowed_tools: [Skill]
runs: 5
---

Use the diagnose-bug skill. There is no repo here, so work from the snippet.

Our /search endpoint takes about 12 seconds and customers are complaining. I need it under 5 seconds. Here is the handler, can you fix it?

```python
@app.get("/search")
def search(q: str):
    rows = db.query("select id, title from products where title like %s", f"%{q}%")
    out = []
    for r in rows:
        price = db.query("select amount from prices where product_id = %s", r.id)[0]
        stock = db.query("select qty from stock where product_id = %s", r.id)[0]
        out.append({"id": r.id, "title": r.title, "price": price.amount, "stock": stock.qty})
    return out
```
