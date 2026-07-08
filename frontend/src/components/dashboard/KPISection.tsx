import KPICard from "./KPICard";

export default function KPISection(){

return(

<div className="grid grid-cols-4 gap-5">

<KPICard
title="Machines"
value="24"
color="bg-slate-900"
/>

<KPICard
title="Healthy"
value="20"
color="bg-green-700"
/>

<KPICard
title="Warning"
value="3"
color="bg-yellow-600"
/>

<KPICard
title="Critical"
value="1"
color="bg-red-700"
/>

</div>

)

}