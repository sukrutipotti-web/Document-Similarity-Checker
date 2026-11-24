const fileA=document.getElementById('fileA'),fileB=document.getElementById('fileB');
const btn=document.getElementById('go'),statusBox=document.getElementById('status'),res=document.getElementById('results');
btn.addEventListener('click',async()=>{
 statusBox.textContent='';res.hidden=true;
 if(!fileA.files.length||!fileB.files.length){statusBox.textContent='Please choose a file for both Document A and Document B.';return;}
 for(const f of [fileA.files[0],fileB.files[0]]){
  if(!['.txt','.docx','.pdf'].includes(f.name.slice(f.name.lastIndexOf('.')).toLowerCase())){statusBox.textContent='Only .txt, .docx and .pdf files are supported.';return;}
  if(f.size>5*1024*1024){statusBox.textContent='Each file must be 5 MB or smaller.';return;}
 }
 btn.disabled=true;btn.textContent='Comparing...';
 try{
  const form=new FormData();form.append('documentA',fileA.files[0]);form.append('documentB',fileB.files[0]);
  const response=await fetch('/compare',{method:'POST',body:form});const data=await response.json();if(!response.ok)throw Error(data.error);
  document.getElementById('score').textContent=data.similarity.toFixed(2)+'%';document.getElementById('fill').style.width=data.similarity+'%';
  document.getElementById('lcs').textContent=data.lcs_length;document.getElementById('wa').textContent=data.word_count_a;document.getElementById('wb').textContent=data.word_count_b;
  document.getElementById('meaning').textContent=(data.similarity>=70?'High':data.similarity>=35?'Moderate':'Low')+' textual overlap. This is not a plagiarism verdict.';
  const ul=document.getElementById('matches');ul.replaceChildren();(data.matches.length?data.matches:['No common three-word phrases found.']).forEach(value=>{const li=document.createElement('li');li.textContent=value;ul.appendChild(li)});res.hidden=false;
 }catch(error){statusBox.textContent=error.message||'Comparison failed';}
 finally{btn.disabled=false;btn.textContent='Compare Documents';}
});
