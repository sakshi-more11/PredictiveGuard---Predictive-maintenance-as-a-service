import{

BarChart,
Bar,
CartesianGrid,
XAxis,
YAxis,
Tooltip,
ResponsiveContainer

}from"recharts";

const data=[

{name:"M1",rul:93},

{name:"M2",rul:75},

{name:"M3",rul:54},

{name:"M4",rul:28},

{name:"M5",rul:12}

];

export default function RULChart(){

return(

<div className="bg-slate-900 rounded-xl p-5">

<h2 className="text-xl mb-5">

Remaining Useful Life

</h2>

<ResponsiveContainer width="100%" height={300}>

<BarChart data={data}>

<CartesianGrid/>

<XAxis dataKey="name"/>

<YAxis/>

<Tooltip/>

<Bar dataKey="rul"/>

</BarChart>

</ResponsiveContainer>

</div>

)

}