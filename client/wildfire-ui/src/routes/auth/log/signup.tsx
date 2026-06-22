import { FeatherChrome, FeatherFlame } from "@subframe/core";
import { Button } from "../../../ui/components/ui/button";
import { useForm } from "react-hook-form";
import { z } from "zod";
import { toast } from "sonner";
import { zodResolver } from "@hookform/resolvers/zod";
import { Field, FieldLabel, FieldGroup } from "../../../ui/components/ui/field";
import { Input } from "../../../ui/components/ui/input";
import { Link, useNavigate } from "react-router-dom";
import { FieldDescription } from "../../../ui/components/ui/field";
import { useRegisterUser } from "../../../hooks/use-auth";
import { GoogleLogin, type CredentialResponse } from "@react-oauth/google";
import { googleLoginAuth } from "../../../hooks/use-google-auth";

const SignUp = () => {
  const navigate = useNavigate();
  const { mutate: regUser, isPending } = useRegisterUser();
  const userValidation = z.object({
    username: z.string().min(8, "Username must be more than 8 characters"),
    email: z.string().email("Invalid email address"),
    password: z.string().min(8, "Password must be 8 characters"),
  });

  type userRegister = z.infer<typeof userValidation>;

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<userRegister>({
    resolver: zodResolver(userValidation),
    defaultValues: {
      username: "",
      email: "",
      password: "",
    },
  });

  const onSubmit = (data: userRegister) => {
    regUser(data, {
      onSuccess: () => {
        navigate("/dashboard");
      },
    });
  };

  const handleGoogleResponse = async (
    credentialResponse: CredentialResponse,
  ) => {
    if (!credentialResponse.credential) return;
    try {
      const userData = await googleLoginAuth(credentialResponse.credential);
      toast.success("User sign-up successful!");
      navigate("/")
    } catch (e: any) {
      toast.error("User sign-up unsucessful: ", e)
      console.error(e);
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
            <h2 className="text-xl font-bold">Create your account</h2>
            <p>Start monitoring wildfire risk with real-time intelligence</p>
          </div>
          {/* Google Directory Header */}
          <div className="flex flex-col pb-[50%] gap-y-1">
            <GoogleLogin
              onSuccess={handleGoogleResponse}
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
                  <FieldLabel htmlFor="username">Username</FieldLabel>
                  <Input
                    id="username"
                    placeholder="johndoe450"
                    {...register("username")}
                  />
                  {errors.username && (
                    <span className="text-red-500 text-xs">
                      {errors.username.message}
                    </span>
                  )}
                </Field>
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
                </Field>
              </FieldGroup>
              <Button
                disabled={isPending}
                className="bg-[#2563EB] text-white w-sm p-5 relative top-5 rounded-lg hover:cursor-pointer hover:scale-105 duration-300 hover:bg-[#537de7] hover:text-black"
              >
                {isPending ? "Registering..." : "Sign Up"}
              </Button>
            </form>
            <div className="pt-5 flex flex-col justify-center items-center">
              <FieldDescription>
                Already have an account?{" "}
                <Link className="text-[#2563EB] no-underline" to="/login">
                  Sign In
                </Link>
              </FieldDescription>
            </div>
          </div>
        </div>
      </div>
    </>
  );
};

export default SignUp;
