import { Link } from "react-router-dom";
import { IconWithBackground } from "../../ui";
import { Button } from "../../ui/components/ui/button";
import {
  FeatherSparkles,
  FeatherMapPin,
  FeatherActivity,
  FeatherClipboardList,
} from "@subframe/core";
import Footer from "../constants/footer";
import { useGetUser } from "../../hooks/use-auth";

const Dashboard = () => {
  const {data: user, isLoading} = useGetUser();
  const cards = {
    cardOne: {
      icon: FeatherMapPin,
      title: "Real-time hotspot mapping",
      description:
        "Live NASA FIRMS satellite detections plotted on an interactive map so you always know where heat is building.",
    },
    cardTwo: {
      icon: FeatherActivity,
      title: "ML risk scoring",
      description:
        "An XGBoost model weighs weather, fuel, and terrain to assign each zone a clear, trustworthy risk score.",
    },
    cardThree: {
      icon: FeatherClipboardList,
      title: "Field incident logging",
      description:
        "Crews log observations and incidents from the field, keeping every report synced with command in seconds.",
    },
  };

  if (isLoading) {
    return (
      <div className="w-screen h-screen bg-black flex items-center justify-center text-white">
        Loading PyroSense...
      </div>
    );
  }

  if (user) {
    return (
       <div className="w-screen h-screen ">
      {/* Black Container -> Description/Intro */}
      <div className="flex flex-col h-screen bg-black justify-center items-center text-center gap-y-5 pb-80">
        <div className="bg-white rounded-sm p-2 w-[22%] h-8 py-1 pr-4">
          <FeatherSparkles className="text-[#e9590c]" />
          Powered by XGBoost • NASA FIRMS
        </div>
        <h1 className="text-6xl w-4xl font-bold text-white">
          Welcome back, {user.username}!
        </h1>
        <p className="text-[#D4D4D4] w-[48%] text-shadow-2xs text-2xl">
          PyroSense fuses satellite hostpot data with machine learning to score
          wildfire risk in realtime, so response teams act earlier and protect
          more.
        </p>
        <div className="flex flex-row gap-x-5">
          <Button className="bg-[#e9590c] p-5 hover:scale-105">
            <Link
              className="text-md font-bold text-white cursor-pointer"
              to="/register"
            >
              Get Started
            </Link>
          </Button>
          <Button className="border-2 border-[#737373] p-5 cursor-pointer hover:scale-105">
            <Link
              className="text-[#222222] hover:text-white transition-all duration-300 cursor-pointer"
              to="/login"
            >
              Sign In
            </Link>
          </Button>
        </div>
      </div>
      {/* White Container -> More Information/Benefits */}
      <div className="bg-white flex flex-col items-center p-10 translate-y-[-75%]">
        <h2 className="text-2xl font-bold">Built for the front line</h2>
        <span className="">
          Everything your teams needs to monitor, access, and respond to
          wildfire threats in one platform.
        </span>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-8 max-w-6xl w-full pt-20">
          {Object.values(cards).map((card, index) => {
            const CustomIcon = card.icon;

            return (
              <div
                key={index}
                className="border border-gray-200 p-7 rounded-lg shadow-sm flex flex-col items-start gap-y-3 bg-white"
              >
                {CustomIcon ? (
                  <IconWithBackground size="medium" variant="neutral">
                    <CustomIcon className="text-[#e9590c]" />
                  </IconWithBackground>
                ) : (
                  <div className="text-red-500 text-xs">
                    Icon missing or failed to import
                  </div>
                )}

                <h3 className="font-bold text-lg text-black mt-2">
                  {card.title}
                </h3>
                <p className="text-gray-600 text-sm leading-relaxed">
                  {card.description}
                </p>
              </div>
            );
          })}
        </div>
      </div>
      <Footer/>
    </div>
    )
  }
  return (
    <div className="w-screen h-screen ">
      {/* Black Container -> Description/Intro */}
      <div className="flex flex-col h-screen bg-black justify-center items-center text-center gap-y-5 pb-80">
        <div className="bg-white rounded-sm p-2 w-[22%] h-8 py-1 pr-4">
          <FeatherSparkles className="text-[#e9590c]" />
          Powered by XGBoost • NASA FIRMS
        </div>
        <h1 className="text-6xl w-4xl font-bold text-white">
          Predict wildfire risk before it spreads
        </h1>
        <p className="text-[#D4D4D4] w-[48%] text-shadow-2xs text-2xl">
          PyroSense fuses satellite hostpot data with machine learning to score
          wildfire risk in realtime, so response teams act earlier and protect
          more.
        </p>
        <div className="flex flex-row gap-x-5">
          <Button className="bg-[#e9590c] p-5 hover:scale-105">
            <Link
              className="text-md font-bold text-white cursor-pointer"
              to="/register"
            >
              Get Started
            </Link>
          </Button>
          <Button className="border-2 border-[#737373] p-5 cursor-pointer hover:scale-105">
            <Link
              className="text-[#222222] hover:text-white transition-all duration-300 cursor-pointer"
              to="/login"
            >
              Sign In
            </Link>
          </Button>
        </div>
      </div>
      {/* White Container -> More Information/Benefits */}
      <div className="bg-white flex flex-col items-center p-10 translate-y-[-75%]">
        <h2 className="text-2xl font-bold">Built for the front line</h2>
        <span className="">
          Everything your teams needs to monitor, access, and respond to
          wildfire threats in one platform.
        </span>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-8 max-w-6xl w-full pt-20">
          {Object.values(cards).map((card, index) => {
            const CustomIcon = card.icon;

            return (
              <div
                key={index}
                className="border border-gray-200 p-7 rounded-lg shadow-sm flex flex-col items-start gap-y-3 bg-white"
              >
                {CustomIcon ? (
                  <IconWithBackground size="medium" variant="neutral">
                    <CustomIcon className="text-[#e9590c]" />
                  </IconWithBackground>
                ) : (
                  <div className="text-red-500 text-xs">
                    Icon missing or failed to import
                  </div>
                )}

                <h3 className="font-bold text-lg text-black mt-2">
                  {card.title}
                </h3>
                <p className="text-gray-600 text-sm leading-relaxed">
                  {card.description}
                </p>
              </div>
            );
          })}
        </div>
      </div>
      <Footer/>
    </div>
  );
};

export default Dashboard;