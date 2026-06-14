import { FeatherChrome, FeatherFlame } from "@subframe/core";
import { Button } from "../../../ui/components/ui/button";
import {useForm} from "react-hook-form"

const SignIn = () => {
  return (
    <>
      <div className="bg-black h-screen">
        <div className="bg-white">
          <h1>
            <FeatherFlame />
            PyroSense
          </h1>
          <h2>
            Welcome back
          </h2>
          <p>Sign in to your wildfire intelligence dashboard</p>
          <Button><FeatherChrome/> Continue with Google</Button>
          <div className="flex h-px grow shrink-0 basis-0 flex-col items-center gap-2 bg-neutral-border" />
            <span className="text-caption font-caption text-subtext-color">
              or
            </span>
            <div className="flex h-px grow shrink-0 basis-0 flex-col items-center gap-2 bg-neutral-border" />

        </div>
      </div>
    </>
  );
};

export default SignIn;
