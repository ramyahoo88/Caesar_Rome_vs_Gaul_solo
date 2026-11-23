'use strict';
// Exact shipped v1.3 script with DOM/storage doubles. Not a real-browser test.
// node helper_reaudit.cjs REPO OUTPUT_DIR
const fs=require('fs'),path=require('path'),vm=require('vm'),assert=require('assert/strict');
const repo=path.resolve(process.argv[2]),out=path.resolve(process.argv[3]);
const html=fs.readFileSync(repo+'/print/Caesar_Solo_Deck.html','utf8');
let js=html.match(/<script>([\s\S]*?)<\/script>/)[1],end=js.lastIndexOf('\n}');
js=js.slice(0,end)+'\nglobalThis.audit={state:()=>JSON.parse(JSON.stringify(S)),D,valid,KEY,injectHistory:x=>S.prev.push(x)};'+js.slice(end);
function boot(saved,failWrite=false){
 const nodes={};for(const m of html.matchAll(/\bid="([^"]+)"/g))nodes[m[1]]={value:'',innerHTML:'',textContent:'',hidden:false,disabled:false,setAttribute(){}};
 const store=new Map();if(saved!==undefined)store.set('caesarSoloDeck2',saved);
 let seed=12345;const math=Object.create(Math);math.random=()=>{seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed/4294967296};
 const ctx=vm.createContext({document:{body:{},getElementById:id=>nodes[id]},localStorage:{getItem:k=>store.get(k)||null,setItem:(k,v)=>{if(failWrite)throw Error('QuotaExceededError');store.set(k,v)}},Math:math,JSON});
 let error=null;try{vm.runInContext(js,ctx)}catch(e){error=e.message}
 return {nodes,store,error,state:()=>ctx.audit.state(),data:()=>JSON.parse(JSON.stringify(ctx.audit.D)),valid:t=>ctx.audit.valid(t),injectHistory:x=>ctx.audit.injectHistory(x)};
}
const checks=[];let a=boot();assert(!a.error);checks.push('clean launch');
const printed=JSON.parse(fs.readFileSync(repo+'/print/cards.json','utf8'));
for(const side of ['R','G']){
 a=boot();a.nodes['b'+side].onclick();
 assert.deepEqual(a.data()[side],printed.filter(c=>c.side===side).map(c=>[c.id,c.name,c.missions.join(' '),c.compass]));
 for(let cycle=0;cycle<12;cycle++){
  const seen=[];
  for(let j=0;j<9;j++){
   a.nodes.draw.onclick();seen.push(a.state().cur.i);
   const b=boot(a.store.get('caesarSoloDeck2'));assert(!b.error);assert.deepEqual(b.state(),a.state());a=b;
  }
  assert.equal(new Set(seen).size,9);
  if(cycle%3===2&&cycle<11)a.nodes.next.onclick();
 }
 checks.push(side+': 108 draws with reload, unique deck cycles and turn advancement');
}
a=boot();for(let j=0;j<9;j++)a.nodes.draw.onclick();const deckEnd=a.state();
assert.match(a.nodes.left.textContent,/0 left/);a.nodes.draw.onclick();a.nodes.undo.onclick();assert.deepEqual(a.state(),deckEnd);checks.push('empty-deck label and reshuffle Undo');
const before=a.state();a.nodes.next.onclick();a.nodes.undo.onclick();assert.deepEqual(a.state(),before);checks.push('Undo across Next turn');
for(let j=1;j<6;j++)a.nodes.next.onclick();assert.equal(a.state().turn,6);assert(a.nodes.next.disabled);const six=a.state();a.nodes.next.onclick();assert.deepEqual(a.state(),six);checks.push('Turn 6 advance blocked');
for(const side of ['R','G'])for(let lvl=1;lvl<=5;lvl++){
 a=boot();a.nodes['b'+side].onclick();a.nodes.lvl.onchange({target:{value:String(lvl)}});
 for(let n=1;n<=8;n++){
  a.nodes.draw.onclick();const want=side==='R'?(lvl>=3||(lvl===2&&n<=4)):(lvl===5&&n<=4);
  assert.equal(a.nodes.bonus.innerHTML.includes('class="ap"'),want);
 }
}
checks.push('80 level/bonus boundaries');
a=boot();for(let j=0;j<4;j++)a.nodes.draw.onclick();a.nodes.bG.onclick();a.nodes.lvl.onchange({target:{value:'5'}});a.nodes.draw.onclick();assert.equal(a.state().play.G,1);assert(a.nodes.bonus.innerHTML.includes('class="ap"'));checks.push('independent side counters');
const valid=boot().state(),badSide={...valid,side:'invalid'},badDeck=structuredClone(valid);badDeck.deck.R=Array(9).fill(0);
for(const saved of [JSON.stringify(badSide),JSON.stringify(badDeck),'not JSON']){
 a=boot(saved);assert(!a.error);assert.match(a.nodes.notice.textContent,/could not be restored/);assert.equal(a.state().side,'R');assert.equal(a.store.get('caesarSoloDeck2-damaged'),saved);
}
checks.push('old C05 invalid side, duplicate deck and malformed JSON recover');
a=boot(undefined,true);assert.match(a.nodes.notice.textContent,/not saving/);checks.push('storage failure notice');

// Verify both original R04 cases, mixed valid/invalid history and the use-time guard.
const malformed=structuredClone(valid);malformed.prev=['not JSON'];a=boot(JSON.stringify(malformed));assert(!a.error);assert.equal(a.state().prev.length,0);assert.match(a.nodes.notice.textContent,/history.*damaged/);
const corrupt=structuredClone(valid);corrupt.prev=[JSON.stringify({...valid,side:'invalid'})];a=boot(JSON.stringify(corrupt));assert(!a.error);assert.equal(a.state().prev.length,0);assert.equal(a.state().side,'R');
const old=boot();old.nodes.draw.onclick();const good=old.state().prev[0];const mixed=structuredClone(valid);mixed.prev=[good,'bad',JSON.stringify({...valid,side:'invalid'})];a=boot(JSON.stringify(mixed));assert(!a.error);assert.equal(a.state().prev.length,1);a.nodes.undo.onclick();assert.equal(a.state().side,'R');
a=boot();const beforeGuard=a.state();a.injectHistory('not JSON');a.nodes.undo.onclick();assert.deepEqual(a.state(),beforeGuard);assert.match(a.nodes.notice.textContent,/damaged.*skipped/);
checks.push('R04 malformed and invalid-side snapshots dropped on restore');checks.push('R04 mixed history retains valid step');checks.push('R04 use-time guard skips damaged history');
const result={mode:'DOM/storage doubles; not a real browser',passedChecks:checks,normalDrawReloads:216,bonusChecks:80,R04:'all original and additional recovery cases pass'};
fs.writeFileSync(out+'/helper-results.json',JSON.stringify(result,null,2));console.log(JSON.stringify(result,null,2));
