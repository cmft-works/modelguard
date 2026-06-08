import React, {useEffect, useState} from 'react';
import { createRoot } from 'react-dom/client';
import { Shield, DollarSign, Activity, Ban, Send } from 'lucide-react';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer } from 'recharts';
import './style.css';

const API = import.meta.env.VITE_API_URL || '';

function Card({title, value, icon}) { return <div className="card"><div className="cardTop"><span>{title}</span>{icon}</div><h2>{value}</h2></div> }

function App(){
  const [summary,setSummary]=useState({});
  const [providers,setProviders]=useState([]);
  const [departments,setDepartments]=useState([]);
  const [requests,setRequests]=useState([]);
  const [form,setForm]=useState({user_email:'chanakya@company.com',department:'IT',role:'employee',app_name:'AI Assistant',provider:'openai',model:'gpt-4o-mini',data_classification:'internal',prompt:'Summarize this internal policy document'});
  const [result,setResult]=useState(null);

  const load=()=>{
    fetch(`${API}/v1/dashboard/summary`).then(r=>r.json()).then(setSummary);
    fetch(`${API}/v1/dashboard/by-provider`).then(r=>r.json()).then(setProviders);
    fetch(`${API}/v1/dashboard/by-department`).then(r=>r.json()).then(setDepartments);
    fetch(`${API}/v1/requests`).then(r=>r.json()).then(setRequests);
  };
  useEffect(load,[]);

  const submit=async(e)=>{e.preventDefault(); const res=await fetch(`${API}/v1/ai/chat`,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(form)}); const data=await res.json(); setResult(data); load();};

  return <main>
    <header><div><h1>ModelGuard AI</h1><p>AI usage, cost, access control, and audit in one place.</p></div><div className="pill"><Shield size={18}/> Control Tower</div></header>
    <section className="grid4">
      <Card title="Total Calls" value={summary.total_calls ?? 0} icon={<Activity/>}/>
      <Card title="Total Cost" value={`$${summary.total_cost ?? 0}`} icon={<DollarSign/>}/>
      <Card title="Blocked Calls" value={summary.blocked_calls ?? 0} icon={<Ban/>}/>
      <Card title="Avg Risk" value={summary.avg_risk_score ?? 0} icon={<Shield/>}/>
    </section>
    <section className="grid2">
      <div className="panel"><h3>Spend by Provider</h3><ResponsiveContainer width="100%" height={240}><BarChart data={providers}><XAxis dataKey="provider"/><YAxis/><Tooltip/><Bar dataKey="cost" /></BarChart></ResponsiveContainer></div>
      <div className="panel"><h3>Usage by Department</h3><ResponsiveContainer width="100%" height={240}><BarChart data={departments}><XAxis dataKey="department"/><YAxis/><Tooltip/><Bar dataKey="calls" /></BarChart></ResponsiveContainer></div>
    </section>
    <section className="grid2">
      <form className="panel" onSubmit={submit}><h3>Test Guarded AI Request</h3>
        {['user_email','department','role','app_name','provider','model','data_classification'].map(k=><label key={k}>{k}<input value={form[k]} onChange={e=>setForm({...form,[k]:e.target.value})}/></label>)}
        <label>prompt<textarea value={form.prompt} onChange={e=>setForm({...form,prompt:e.target.value})}/></label>
        <button><Send size={16}/> Send through gateway</button>
        {result && <pre>{JSON.stringify(result,null,2)}</pre>}
      </form>
      <div className="panel"><h3>Recent Audit Logs</h3><div className="tableWrap"><table><thead><tr><th>Status</th><th>User</th><th>Dept</th><th>Model</th><th>Risk</th><th>Cost</th><th>Reason</th></tr></thead><tbody>{requests.map(r=><tr key={r.request_id}><td><span className={r.status==='blocked'?'bad':'good'}>{r.status}</span></td><td>{r.user_email}</td><td>{r.department}</td><td>{r.model}</td><td>{r.risk_score}</td><td>${r.cost}</td><td>{r.reason}</td></tr>)}</tbody></table></div></div>
    </section>
  </main>
}

createRoot(document.getElementById('root')).render(<App/>);
