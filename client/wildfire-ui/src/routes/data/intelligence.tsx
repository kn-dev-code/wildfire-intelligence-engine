
import { FeatherShieldCheck } from "@subframe/core"
import { Button } from "../../ui/components/ui/button"
import SideBar from "../constants/sidebar"

const Intelligence = () => {
  return (
    <div className="bg-white h-full"> {/* Main Box */}
      {/* Top Bar */}
      <div className="flex flex-row justify-between border-2 border-black w-[86%] relative left-[14.9%] place-items-center">
        <div className="flex flex-col justify-center pl-4">
          <h1 className = " text-shadow-black font-bold text-xl">Wildfire Risk Intelligence</h1>
          <span className = "text-sm">NASA FIRMS Ingestion • XGBoost Inference</span>
        </div>
        <div className="grow shrink-0 relative left-[65%]">
          <Button className="p-1 bg-[#DAFBE6] text-[#639273] w-[9%] h-[15%]"><FeatherShieldCheck/>user</Button>
        </div>
      </div>
      <SideBar />

      {/* Coordinate Box */}
      <div>

      </div>

      {/* Hotspot Box */}
      <div>

      </div>

      {/* Result Box */}
      <div>

      </div>

    </div>
  )
}

export default Intelligence
