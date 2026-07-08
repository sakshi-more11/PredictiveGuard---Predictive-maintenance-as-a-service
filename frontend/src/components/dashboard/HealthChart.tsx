import{

LineChart,
Line,
CartesianGrid,
XAxis,
YAxis,
Tooltip,
ResponsiveContainer

}from"recharts";

const data=[

{day:"Mon",health:98},
{day:"Tue",health:96},
{day:"Wed",health:95},
{day:"Thu",health:93},
{day:"Fri",health:90},
{day:"Sat",health:88},
{day:"Sun",health:85}

];

export default function HealthChart(){

return(

<div className="bg-slate-900 rounded-xl p-5">

<h2 className="text-xl mb-5">

Machine Health Trend

</h2>

<ResponsiveContainer width="100%" height={300}>

<LineChart data={data}>

<CartesianGrid strokeDasharray="3 3"/>

<XAxis dataKey="day"/>

<YAxis/>

<Tooltip/>

<Line
dataKey="health"
stroke="#22d3ee"
strokeWidth={4}
/>

</LineChart>

</ResponsiveContainer>

</div>

)

}