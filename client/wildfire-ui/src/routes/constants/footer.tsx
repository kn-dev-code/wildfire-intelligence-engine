import { FeatherFlame } from "@subframe/core";
import { Link } from "react-router-dom";

const Footer = () => {
  return (
    <div className="flex w-full flex-col items-center justify-center gap-6 border-t border-solid border-neutral-border px-8 py-12 mobile:px-4">
      <div className="flex w-full max-w-5xl flex-wrap items-center justify-between">
        <div className="flex flex-col items-start gap-2">
          <div className="flex items-center gap-2">
            <div className="flex h-7 w-7 flex-none items-center justify-center rounded-md bg-[#ea580c]">
              <FeatherFlame className="text-body font-body text-white" />
            </div>
            <span className="text-body-bold font-body-bold text-default-font">
              PyroSense
            </span>
          </div>
          <span className="text-caption font-caption text-subtext-color">
            Wildfire risk intelligence for response teams.
          </span>
        </div>
        <div className="flex flex-wrap items-center gap-6">
          <Link
            to="/product"
            className="text-caption font-caption text-subtext-color"
          >
            Product
          </Link>
          <Link
            to="/documentation"
            className="text-caption font-caption text-subtext-color"
          >
            Docs
          </Link>
          <Link
            to="/privacy-notes"
            className="text-caption font-caption text-subtext-color"
          >
            Privacy
          </Link>
          <Link
            to="/contact"
            className="text-caption font-caption text-subtext-color"
          >
            Contact
          </Link>
        </div>
      </div>
      <div className="flex w-full max-w-5xl items-center border-t border-solid border-neutral-border pt-6">
        <span className="text-caption font-caption text-subtext-color">
          © 2026 PyroSense. All rights reserved.
        </span>
      </div>
    </div>
  );
};

export default Footer;
