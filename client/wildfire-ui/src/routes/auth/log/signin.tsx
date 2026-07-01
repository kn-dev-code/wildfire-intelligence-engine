import { FeatherChrome, FeatherFlame } from "@subframe/core";
import { Button } from "../../../ui/components/ui/button";
import { useForm } from "react-hook-form";
import { z } from "zod";
import { zodResolver } from "@hookform/resolvers/zod";
import {
  Field,
  FieldLabel,
  FieldGroup,
  FieldDescription,
} from "../../../ui/components/ui/field";
import { Input } from "../../../ui/components/ui/input";
import { Link, useNavigate } from "react-router-dom";
import { useLogUser } from "../../../hooks/use-auth";
import { GoogleLogin, type CredentialResponse } from "@react-oauth/google";
import { useGoogleAuth } from "../../../hooks/use-auth";
import { toast } from "sonner"

const SignIn = () => {
  const navigate = useNavigate();
  const { mutate: logUser, isPending } = useLogUser();
  const { mutateAsync: loginWithGoogle } = useGoogleAuth();

  const userValidation = z.object({
    email: z.string().email("Invalid email address"),
    password: z.string().min(8, "Password must be 8 characters"),
  });

  type userLogin = z.infer<typeof userValidation>;

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<userLogin>({
    resolver: zodResolver(userValidation),
    defaultValues: {
      email: "",
      password: "",
    },
  });

  const onSubmit = (data: userLogin) => {
    logUser(data, {
      onSuccess: () => {
        navigate("/");
      },
    });
  };

  const handleGoogleResponse = async (
    credentialResponse: CredentialResponse,
  ) => {
    if (!credentialResponse.credential) return;
    try {
      const userData = await loginWithGoogle(credentialResponse.credential);
      toast.success("User sign-in successful!")
      navigate("/")
    } catch (e: any) {
      toast.error("User sign-in unsuccessful", e)
      console.error(e)
    }
  };

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
          <div className="flex flex-col pb-[50%] gap-y-3">
            <GoogleLogin
              onSuccess={(res) => handleGoogleResponse(res)}
              onError={() => console.log("Google pop-up failed")}
            />
            <div className="flex h-px grow shrink-0 basis-0 flex-col items-center gap-2 bg-neutral-border" />
            <span className="text-caption font-caption text-subtext-color text-md">
              or
            </span>
            <div className="flex h-px grow shrink-0 basis-0 flex-col items-center gap-2 bg-neutral-border" />
            {/* Form Component */}
            <form onSubmit={handleSubmit(onSubmit)}>
              <FieldGroup>
                <Field>
                  <FieldLabel htmlFor="email">Email</FieldLabel>
                  <Input
                    id="name"
                    placeholder="you@pyrosense.io"
                    required
                    {...register("email")}
                  />
                  {errors.email && (
                    <span className="text-red-500 text-xs">
                      {errors.email.message}
                    </span>
                  )}
                </Field>
                <Field>
                  <FieldLabel>Password</FieldLabel>
                  <Input
                    id="password"
                    placeholder="Enter your password"
                    required
                    {...register("password")}
                  />
                  {errors.password && (
                    <span className="text-red-500 text-xs">
                      {errors.password.message}
                    </span>
                  )}
                  <Link
                    to="/forgot-password"
                    className="pl-[68%] text-[#2563EB] text-sm"
                  >
                    Forgot password?
                  </Link>
                </Field>
              </FieldGroup>
              <Button
                type="submit"
                disabled={isPending}
                className="bg-[#2563EB] text-white w-sm p-5 relative top-5 rounded-lg hover:cursor-pointer hover:scale-105 duration-300 hover:bg-[#537de7] hover:text-black"
              >
                {isPending ? "Signing In..." : "Sign In"}
              </Button>
            </form>
            <div className="pt-5 flex flex-col justify-center items-center">
              <FieldDescription>
                Don't have an account?{" "}
                <Link className="text-[#2563EB] no-underline" to="/register">
                  Sign Up
                </Link>
              </FieldDescription>
            </div>
          </div>
        </div>
      </div>
    </>
  );
};

export default SignIn;
