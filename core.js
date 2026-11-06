export function paragraphs(text) { return text.replace(/\r\n?/g, '\n').split(/\n[\t ]*\n/).filter(p => p.trim()); }
export function annotationRanges(text, entries, paragraph) {
  const ranges = [];
  for (const entry of entries || []) {
    if (entry.paragraph !== paragraph || !entry.anchor || !Number.isInteger(entry.occurrence) || entry.occurrence < 1) continue;
    let start = -1, from = 0;
    for (let n = 0; n < entry.occurrence; n++) { start = text.indexOf(entry.anchor, from); if (start < 0) break; from = start + entry.anchor.length; }
    if (start >= 0) ranges.push({ start, end: start + entry.anchor.length, entry });
  }
  return ranges.sort((a,b) => a.start-b.start).filter((r,i,all) => !all.slice(0,i).some(p => p.end > r.start));
}
export function safeStorage(storage) {
  return { get(key, fallback) { try { const value=JSON.parse(storage.getItem(key)); return value ?? fallback; } catch { return fallback; } }, set(key,value) { try { storage.setItem(key, JSON.stringify(value)); } catch {} } };
}
export function adjacent(chapters,id,delta) { const index=chapters.findIndex(c=>c.id===id); return index < 0 ? null : chapters[index+delta]?.id ?? null; }
export function clampProgress(value) { return Math.max(0,Math.min(1,Number(value)||0)); }

// An explicit editorial chapter selection supersedes imported inline notes.
// Imported notes remain available in the notes panel; demo retains its own cards.
export function learningCards(chapterId, editorial, original = []) {
  return Object.hasOwn(editorial || {}, chapterId) ? editorial[chapterId] : original;
}
