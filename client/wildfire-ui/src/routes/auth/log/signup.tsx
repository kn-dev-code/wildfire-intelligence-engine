import { FeatherChrome, FeatherFlame } from "@subframe/core";
import { Button } from "../../../ui/components/ui/button";
import { useForm } from "react-hook-form";
import { z } from "zod";
import { zodResolver } from "@hookform/resolvers/zod";
import {
  Field,
  FieldLabel,
  FieldGroup,
} from "../../../ui/components/ui/field";
import { Input } from "../../../ui/components/ui/input";
import { Link } from "react-router-dom";

const SignUp = () => {
  const userValidation = z.object({
    username: z.string().min(8, "Username must be more than 8 characters"),
    email: z.string().email("Invalid email address"),
    password: z.string().min(8, "Password must be 8 characters"),
  });

  type userRegister = z.infer<typeof userValidation>;

  const formData = useForm<userRegister>({
    resolver: zodResolver(userValidation),
    defaultValues: {
      username: "",
      email: "",
      password: "",
    },
  });

  const onSubmit = (data: z.infer<userRegister>) => {};
  return (
    <>
      <div className="bg-black h-screen flex flex-col justify-center place-items-center overflow-hidden overscroll-none">
        <div className="bg-white grid grid-rows-3 h-[70%] rounded-2xl place-items-center text-center w-[30%]">
          {/* Title Header*/}
          <div className="flex flex-row items-center gap-x-2 pb-15">
            <FeatherFlame className="bg-[#e9590c] font-body text-white p-2 rounded-md" />
            <h1 className="text-2xl font-bold">PyroSense</h1>
          </div>
          {/* Welcome Header */}
          <div className="flex flex-col pb-[70%]">
            <h2 className="text-xl font-bold">Welcome back</h2>
            <p>Sign in to your wildfire intelligence dashboard</p>
          </div>
          {/* Google Directory Header */}
          <div className="flex flex-col pb-[60%] gap-y-3">
            <Button className="border-2 border-[#a19f9f] p-4 w-sm h-md cursor-pointer hover:bg-[#605d5d] hover:text-white transition-all duration-300 hover:scale-105">
              <FeatherChrome />
              Continue with Google
            </Button>
            <div className="flex h-px grow shrink-0 basis-0 flex-col items-center gap-2 bg-neutral-border" />
            <span className="text-caption font-caption text-subtext-color text-md">
              or
            </span>
            <div className="flex h-px grow shrink-0 basis-0 flex-col items-center gap-2 bg-neutral-border" />
            {/* Form Component */}
            <form>
              <FieldGroup>
                <Field>
                  <FieldLabel htmlFor="email">Email</FieldLabel>
                  <Input id="name" placeholder="you@pyrosense.io" required />
                </Field>
                <Field>
                  <FieldLabel>Password</FieldLabel>
                  <Input
                    id="password"
                    placeholder="Enter your password"
                    required
                  />
                  <Link to = "/forgot-password" className = "pl-[68%] text-[#2563EB] text-sm">
                    Forgot password?
                  </Link>
                </Field>
              </FieldGroup>
              <Button className = "bg-[#2563EB] text-white w-sm p-5 relative top-5 rounded-lg hover:cursor-pointer hover:scale-105 duration-300 hover:bg-[#537de7] hover:text-black">
                Sign Up
              </Button>
            </form>
          </div>
        </div>
      </div>
    </>
  );
};

export default SignUp;
