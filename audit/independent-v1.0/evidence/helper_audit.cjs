'use strict';
// Executes the exact shipped script with DOM/storage doubles. This is not a browser test.
// node helper_audit.cjs REPO OUTPUT_DIR
const fs=require('fs'),path=require('path'),vm=require('vm'),assert=require('assert/strict');
const root=path.resolve(process.argv[2]),out=path.resolve(process.argv[3]);
const html=fs.readFileSync(root+'/print/Caesar_Solo_Deck.html','utf8');
let script=html.match(/<script>([\s\S]*?)<\/script>/)[1];const k=script.lastIndexOf('\n}');
script=script.slice(0,k)+'\nglobalThis.audit={state:()=>JSON.parse(JSON.stringify(S)),D,LV,REF,M};'+script.slice(k);
function boot(saved,failWrite=false){
 const nodes={};for(const m of html.matchAll(/\bid="([^"]+)"/g))nodes[m[1]]={value:'',innerHTML:'',textContent:'',attrs:{},setAttribute(k,v){this.attrs[k]=v}};
 const store=new Map();if(saved!==undefined)store.set('caesarSoloDeck',saved);
 let seed=12345;const math=Object.create(Math);math.random=()=>{seed=(Math.imul(1664525,seed)+1013904223)>>>0;return seed/4294967296};
 const c=vm.createContext({document:{body:{className:'R'},getElementById:id=>nodes[id]},localStorage:{getItem:k=>store.get(k)||null,setItem:(k,v)=>{if(failWrite)throw Error('QuotaExceededError');store.set(k,v)}},Math:math,JSON});
 let error=null;try{vm.runInContext(script,c)}catch(e){error=e.message}
 return {nodes,store,error,state:()=>c.audit.state(),data:()=>JSON.parse(JSON.stringify(c.audit.D))};
}
const checks=[];const ok=(x,n)=>{assert(x,n);checks.push(n)};
let a=boot();ok(!a.error,'first launch');
const printed=JSON.parse(fs.readFileSync(root+'/print/cards.json','utf8'));
for(const side of ['R','G']){
 const d=a.data()[side],p=printed.filter(c=>c.side===side);ok(d.length===9&&p.length===9,side+' has nine cards');
 for(let i=0;i<9;i++)assert.deepEqual(d[i],[p[i].id,p[i].name,p[i].missions.join(' '),p[i].compass]);
 checks.push(side+' helper cards equal print data');
 a.nodes['b'+side].onclick();
 for(let cycle=0;cycle<12;cycle++){
  const seen=[];for(let i=0;i<9;i++){a.nodes.draw.onclick();seen.push(a.state().cur.i);const saved=a.store.get('caesarSoloDeck');const b=boot(saved);assert(!b.error);assert.deepEqual(b.state(),a.state());a=b;}
  assert.equal(new Set(seen).size,9);
 }
 checks.push(side+' twelve complete cycles; reload after every draw');
}
a=boot();for(let i=0;i<9;i++)a.nodes.draw.onclick();const end=a.state();a.nodes.draw.onclick();a.nodes.undo.onclick();ok(JSON.stringify(a.state())===JSON.stringify(end),'Undo of reshuffle restores exact state');
const deckCounter={actualDeck:a.state().deck.R.length,shown:a.nodes.left.textContent};
// Level values and first-four boundaries. No claim of automatic strategy-card entry.
let bonuses=0;
for(const side of ['R','G'])for(let level=1;level<=5;level++){
 a=boot();a.nodes['b'+side].onclick();a.nodes.lvl.onchange({target:{value:String(level)}});
 for(let n=1;n<=8;n++){
  a.nodes.draw.onclick();const has=a.nodes.bonus.innerHTML.includes('class="ap"');
  const want=side==='R'?(level>=3||(level===2&&n<=4)):(level===5&&n<=4);assert.equal(has,want,side+level+' play '+n);bonuses++;
 }
}
checks.push('80 level/play bonus boundaries');
// Reproduce a persistent failure after loading syntactically valid damaged state.
a=boot();const valid=a.state(),bad={...valid,side:'invalid'};let c=boot(JSON.stringify(bad));ok(!!c.error,'C05 invalid saved side crashes startup');
const crash={saved:bad,error:c.error};
const dup=structuredClone(valid);dup.deck.R=Array(9).fill(0);c=boot(JSON.stringify(dup));const draws=[];for(let i=0;i<9;i++){c.nodes.draw.onclick();draws.push(c.state().cur.i)}
ok(new Set(draws).size===1,'C05 a damaged duplicate deck is accepted');
fs.writeFileSync(out+'/C05-damaged-session.json',JSON.stringify(bad,null,2));
// Other usability observations, recorded rather than claimed as corrected behavior.
c=boot(undefined,true);c.nodes.draw.onclick();const storage={error:c.error,bytesSaved:c.store.size,warningPresent:Object.values(c.nodes).some(n=>/not saved|storage|quota/i.test(n.textContent+' '+n.innerHTML))};
a=boot();for(let i=0;i<4;i++)a.nodes.draw.onclick();a.nodes.bG.onclick();a.nodes.lvl.onchange({target:{value:'5'}});a.nodes.draw.onclick();
const sideSwitch={play:a.state().play,bonus:a.nodes.bonus.innerHTML};
const result={mode:'shipped JavaScript with DOM/storage doubles; not a real browser',checks:checks.length,descriptions:checks,bonuses,deckCounter,damagedSession:crash,duplicateDraws:draws,storage,sideSwitch};
fs.writeFileSync(out+'/helper-results.json',JSON.stringify(result,null,2));console.log(JSON.stringify(result,null,2));
