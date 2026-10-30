"use strict";

const test = require("node:test");
const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");
const vm = require("node:vm");
const engine = require("../validator.js");

const appSource = fs.readFileSync(path.join(__dirname, "..", "app.js"), "utf8");

class FakeElement {
  constructor(tag = "") {
    this.tag = tag;
    this.textContent = "";
    this.className = "";
    this.value = "";
    this.disabled = false;
    this.children = [];
    this.events = {};
    this.classList = {add() {}, remove() {}};
  }
  addEventListener(event, handler) { this.events[event] = handler; }
  replaceChildren(...nodes) { this.children = nodes; }
  append(...nodes) { this.children.push(...nodes); }
  click() { if (this.events.click) this.events.click({preventDefault() {}}); }
}

function boot() {
  const ids = ["input", "drop", "selection", "mapping", "status", "run", "download",
               "issues", "clean", "broken", "total", "valid", "errors", "warnings", "result-context"];
  const elements = Object.fromEntries(ids.map(id => [id, new FakeElement(id)]));
  const document = {
    getElementById(id) { assert.ok(elements[id], "Expected DOM element " + id); return elements[id]; },
    createElement(tag) { return new FakeElement(tag); },
    body: new FakeElement("body")
  };
  vm.runInNewContext(appSource, {
    window: {SurgCoreValidator: engine},
    document, Blob, URL: {createObjectURL: () => "blob:local", revokeObjectURL() {}},
    setTimeout: () => {},
  }, {filename: "app.js"});
  return elements;
}

async function choose(elements, name, content) {
  elements.input.files = [{
    name, size: Buffer.byteLength(content), text: async () => content
  }];
  elements.input.events.change();
  // The change handler runs acceptFile asynchronously by design.
  await new Promise(resolve => setImmediate(resolve));
}

const example = {
  id: "Q1", stem: "Which choice best demonstrates a valid example question?",
  options: ["one", "two", "three", "four"], answer: "B",
  explanation: "Synthetic educational example.", source: "Synthetic source"
};

test("previously saved report is shown immediately; run disabled", async () => {
  const elements = boot();
  const report = engine.validate(engine.parseInput(JSON.stringify([
    example, {...example, id: "Q2", answer: "E"}
  ]), "json"));
  await choose(elements, "surgcore-validation-report 2.json", JSON.stringify(report));
  assert.equal(elements.total.textContent, "2");
  assert.equal(elements.errors.textContent, "2");
  assert.equal(elements.run.disabled, true);
  assert.equal(elements.download.disabled, true);
  assert.match(elements.status.textContent, /Saved report opened/);
  assert.match(elements["result-context"].textContent, /NOT been rechecked/);
  assert.ok(elements.issues.children.some(li => li.children.some(c => String(c.textContent).includes("duplicate_stem"))));
});

test("question bank file restores local checks after opening a saved report", async () => {
  const elements = boot();
  const original = engine.validate(engine.parseInput(JSON.stringify([example]), "json"));
  await choose(elements, "surgcore-validation-report.json", JSON.stringify(original));
  assert.equal(elements.run.disabled, true);
  await choose(elements, "bank.json", JSON.stringify([example]));
  assert.equal(elements.run.disabled, false);
  elements.run.click();
  assert.equal(elements.total.textContent, "1");
  assert.equal(elements.errors.textContent, "0");
  assert.equal(elements.download.disabled, false);
  assert.match(elements["result-context"].textContent, /New structural validation/);
});

test("synthetic example buttons restore functionality after viewing a saved report", async () => {
  const elements = boot();
  const original = engine.validate(engine.parseInput(JSON.stringify([example]), "json"));
  await choose(elements, "random-name.json", JSON.stringify(original));
  elements.broken.click();
  assert.equal(elements.run.disabled, false);
  elements.run.click();
  assert.equal(elements.total.textContent, "3");
  assert.equal(elements.errors.textContent, "2");
  assert.equal(elements.warnings.textContent, "1");
});

test("malformed report fails safely with readable status", async () => {
  const elements = boot();
  const bad = JSON.stringify({schema_version:"1.0",summary:{record_count:5},issues:[]});
  await choose(elements, "report.json", bad);
  assert.equal(elements.run.disabled, true);
  assert.equal(elements.download.disabled, true);
  assert.match(elements.status.textContent, /saved validation report/);
});

test("report IDs render as text only, never interpreted as HTML", async () => {
  const elements = boot();
  const original = engine.validate(engine.parseInput(JSON.stringify([
    {...example, id:"<img src=x onerror=alert(1)>", answer:"E"}
  ]), "json"));
  await choose(elements, "report.json", JSON.stringify(original));
  assert.ok(elements.issues.children.some(li => li.children.some(
    child => child.textContent.includes("<img src=x onerror=alert(1)>"))));
  assert.doesNotMatch(appSource, /\.innerHTML\s*=/);
});

test("results are capped at 200 entries to keep mobile view responsive", async () => {
  const elements = boot();
  const rows = Array.from({length:205}, (_,i) => ({...example,id:"Q"+i,answer:"E"}));
  const report = engine.validate(engine.parseInput(JSON.stringify(rows), "json"));
  await choose(elements, "report.json", JSON.stringify(report));
  assert.equal(elements.issues.children.length, 201);
  assert.match(elements.issues.children[200].textContent,/first 200 findings/);
});
