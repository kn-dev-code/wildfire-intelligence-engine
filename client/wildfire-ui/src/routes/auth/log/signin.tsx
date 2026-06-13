import { FeatherChrome, FeatherFlame } from "@subframe/core";
import { Button } from "../../../ui/components/ui/button";
const SignIn = () => {
  return (
    <div className="bg-black h-screen flex flex-col justify-center place-items-center">
      <div className="bg-white p-30 w-[25%] rounded-2xl h-[70%]">
        <div className = "flex flex-row items-center gap-x-2">
          <FeatherFlame className="bg-[#e9590c] font-body text-white p-2 rounded-md cursor-pointer" />
          <h1 className="text-black font-bold text-2xl">PyroSense</h1>
        </div>
        <div className = "flex flex-col">
        <h1>Welcome back</h1>
        <span>Sign in to your wildfire intelligence dashboard</span>
        <Button className = "p-5 w-2xl "><FeatherChrome/>Continue with Google</Button>
        
        </div>
      </div>
    </div>
  );
};

export default SignIn;
