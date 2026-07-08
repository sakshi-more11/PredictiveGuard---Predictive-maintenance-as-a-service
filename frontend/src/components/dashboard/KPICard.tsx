interface Props{
title:string
value:string
color:string
}

export default function KPICard({title,value,color}:Props){

return(

<div className={`rounded-xl p-6 ${color} shadow-lg`}>

<p className="text-sm text-slate-300">

{title}

</p>

<h1 className="text-4xl font-bold mt-3">

{value}

</h1>

</div>

)

}