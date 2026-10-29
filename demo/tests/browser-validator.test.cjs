"use strict";

const test = require("node:test");
const assert = require("node:assert/strict");
const v = require("../validator.js");

const q = (id, stem, options = ["alpha", "beta", "gamma", "delta"], answer = "B") => ({
  id, stem, options, answer, explanation: "This is a synthetic example.", source: "Synthetic fixture"
});

function check(data, mapping) {
  return v.validate(v.parseInput(JSON.stringify(data), "json", mapping));
}

test("valid JSON array and wrapper parse", () => {
  const item = q("Q1", "Which label identifies the selected answer?");
  for (const value of [[item], { questions: [item] }]) {
    const result = check(value);
    assert.equal(result.summary.record_count, 1);
    assert.equal(result.summary.error_count, 0);
    assert.equal(result.summary.warning_count, 0);
  }
});

test("valid CSV with quotes and escaped quotes", () => {
  const csv = 'id,stem,option_a,option_b,option_c,option_d,answer,explanation,source\nQ1,"What does ""CSV"" represent?",a,b,c,d,B,Long enough explanation,Source\n';
  assert.equal(v.parseCsv(csv)[0].stem, 'What does "CSV" represent?');
  const result = v.validate(v.parseInput(csv, "csv"));
  assert.equal(result.summary.error_count, 0);
});

test("CSV quoted multiline cell works", () => {
  const csv = 'id,stem,option_a,option_b,option_c,option_d,answer\nQ1,"First line\nsecond line?",a,b,c,d,B\n';
  assert.match(v.parseCsv(csv)[0].stem, /\n/);
  assert.equal(v.parseInput(csv, "csv").length, 1);
});

test("CSV with duplicate headers is rejected", () => {
  assert.throws(() => v.parseCsv("id,ID\nQ1,Q2"), /unique/);
});

test("CSV with extra fields is rejected", () => {
  assert.throws(() => v.parseCsv("id,stem\n1,question,x"), /columns/);
});

test("CSV with unclosed quotes is rejected", () => {
  assert.throws(() => v.parseCsv('id,stem\n1,"question'), /Unclosed/);
});

test("malformed JSON is rejected", () => {
  assert.throws(() => v.parseInput("{broken", "json"), /not valid JSON/);
});

test("wrong type and empty data rejected", () => {
  assert.throws(() => v.parseInput("{}", "json"), /question array/);
  assert.throws(() => v.parseInput("[]", "json"), /no question/);
});

test("mapping works with customized field names", () => {
  const mapping = v.parseMapping('{"id":"qid","stem":"prompt","option_a":"one","option_b":"two","option_c":"three","option_d":"four","answer":"key"}');
  const item = { qid:"Q1", prompt:"Which key identifies the correct choice?", one:"a", two:"b", three:"c", four:"d", key:"C" };
  const parsed = v.parseInput(JSON.stringify([item]), "json", mapping);
  assert.equal(parsed[0].question_id,"Q1");
  assert.equal(parsed[0].answer,"C");
  assert.equal(v.validate(parsed).summary.error_count,0);
});

test("invalid and duplicate mapping sources rejected", () => {
  assert.throws(() => v.parseMapping('{"stem":"x","answer":"x"}'), /unique/);
  assert.throws(() => v.parseMapping('{"mystery":"x"}'), /Unknown/);
  assert.throws(() => v.parseMapping("[]"), /JSON object/);
});

test("five-option lists or objects rejected, not truncated", () => {
  assert.throws(() => check([q("Q1","What is the required field?",["a","b","c","d","e"])]), /exactly/);
  assert.throws(() => check([{ ...q("Q1","What is the required field?"), options:{A:"a",B:"b",C:"c",D:"d",E:"e"} }]), /exactly/);
});

test("invalid answer and duplicated question stem flagged", () => {
  const result = check([q("Q1","Which field stores the answer?"),q("Q2","Which field stores the answer?",undefined,"E")]);
  assert.deepEqual(result.issues.filter(x => x.severity === "error").map(x => x.code), ["duplicate_stem","invalid_answer"]);
  assert.equal(result.summary.schema_valid_record_count,1);
});

test("missing explanations and references flagged", () => {
  const item=q("Q1","Which field stores the answer?");
  item.explanation=""; item.source="";
  assert.deepEqual(check([item]).issues.map(x=>x.code),["missing_explanation","missing_source"]);
});

test("critical comparison operators and decimals remain distinct", () => {
  const a=q("Q1","For pH < 7.30, choose an answer.");
  const b=q("Q2","For pH > 7.30, choose an answer.");
  const c=q("Q3","For pH < 7.03, choose an answer.");
  assert.equal(check([a,b,c]).issues.filter(x=>x.code==="duplicate_stem").length,0);
});

test("option comparator symbols remain distinct", () => {
  const item=q("Q1","For the synthetic scenario, select a comparison.",["pH < 7.30","pH > 7.30","pH = 7.30","pH >= 7.30"]);
  assert.equal(check([item]).summary.error_count,0);
});

test("superficial duplicate option punctuation is detected", () => {
  const item=q("Q1","Select the choice used twice.",["same value!","Same VALUE","different","other"]);
  assert.ok(check([item]).issues.some(x=>x.code==="duplicate_option"));
});

test("Arabic Unicode parsing works", () => {
  const item=q("Q1","ماذا تعني علامة < مقارنة ب > ؟");
  assert.equal(check([item]).summary.error_count,0);
});

test("question ID is kept in JSON output, never rendered as HTML", () => {
  const item=q("<script>alert(1)</script>", "Which one is correct?");
  const report=check([item]);
  assert.equal(report.issues.length,0);
  assert.equal(report.summary.record_count,1);
});

test("file size and record count limits apply", () => {
  const long="A".repeat(v.LIMIT_BYTES+1);
  assert.throws(()=>v.parseInput(long, "json"), /5 MiB/);
  const thousands=Array.from({length:v.LIMIT_RECORDS+1}, (_,i)=>q(String(i),"Example question?"));
  assert.throws(()=>v.parseInput(JSON.stringify(thousands), "json"), /5,000/);
});

test("browser validator does not claim near-duplicate semantic detection", () => {
  const r=check([q("Q1","This is the correct original question text?"),q("Q2","This is the correct original question version?")]);
  assert.ok(r.disclaimer.includes("does not run"));
  assert.equal(r.issues.some(x=>x.code==="near_duplicate_stem"),false);
});
