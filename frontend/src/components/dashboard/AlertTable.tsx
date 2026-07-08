const alerts=[

{

machine:"CP330",

severity:"Critical",

time:"2 mins"

},

{

machine:"CP120",

severity:"Medium",

time:"20 mins"

},

{

machine:"CP210",

severity:"Low",

time:"1 hour"

}

];

export default function AlertTable(){

return(

<div className="bg-slate-900 rounded-xl p-5">

<h2 className="text-xl mb-5">

Recent Alerts

</h2>

<table className="w-full">

<thead>

<tr>

<th>Machine</th>

<th>Severity</th>

<th>Time</th>

</tr>

</thead>

<tbody>

{

alerts.map((a)=>(

<tr key={a.machine}>

<td>{a.machine}</td>

<td>{a.severity}</td>

<td>{a.time}</td>

</tr>

))

}

</tbody>

</table>

</div>

)

}