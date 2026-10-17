// One query interface over two databases, so the exporter is the same code in the Worker
// (D1) and in the round-trip gate (node:sqlite). Nothing here emits a transaction, because
// remote D1 rejects BEGIN TRANSACTION where local SQLite accepts it.

export function nodeDb(database) {
  return {
    async all(sql, params = []) { return database.prepare(sql).all(...params); },
    async run(sql, params = []) { return database.prepare(sql).run(...params); },
  };
}

export function d1Db(DB) {
  return {
    async all(sql, params = []) {
      const r = await DB.prepare(sql).bind(...params).all();
      return r.results || [];
    },
    async run(sql, params = []) { return DB.prepare(sql).bind(...params).run(); },
  };
}
