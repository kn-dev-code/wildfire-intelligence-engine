
import { FeatherCloudSun } from "@subframe/core";
import { FeatherFlame } from "@subframe/core";
import { FeatherMap } from "@subframe/core";
import { FeatherMapPin } from "@subframe/core";
import { FeatherMoreHorizontal } from "@subframe/core";
import { FeatherSatellite } from "@subframe/core";
import { FeatherScan } from "@subframe/core";
import { FeatherShieldCheck } from "@subframe/core";
import { FeatherTriangleAlert } from "@subframe/core";
import { FeatherZap } from "@subframe/core";
import { IconWithBackground } from "../../ui";

const SideBar = () => {
    return (
        <div className="flex flex-initial flex-col justify-between pl-10 border-r-2 w-[15%] border-b-2 h-screen [&>div[class*='items-start']]:">
            {/* Header */}
            <div className = "flex flex-col items-start">  
                <span className="text-md">Pyro Intelligence</span>
                <span className="text-md">Wildfire Engine</span>
                </div>

            {/* Access Menu */}
            <div className = "flex flex-col justify-center"> 
                <span className="text-sm text-[#868686]"><FeatherMap />Dashboard / Map</span>
                <span className="text-sm text-[#868686]"><FeatherCloudSun />Micro Climate</span>
                <span className="text-sm text-[#868686]"><FeatherFlame />Incident Logger</span>
                </div>


            {/* Bottom Header */}
            <div className = "flex flex-col justify-end">
                <span className="text-sm text-[#000000] font-bold">Example Name</span>
                <span className="text-sm text-[#808080]">Example Role</span>
                </div>

        </div>
    )
}

export default SideBar