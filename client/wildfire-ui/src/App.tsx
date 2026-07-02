import { BrowserRouter, Routes, Route, Outlet } from "react-router-dom";
import SignIn from "./routes/auth/log/signin";
import SignUp from "./routes/auth/log/signup";
import Navbar from "./routes/constants/navbar";
import Dashboard from "./routes/home/dashboard";
import { Toaster } from "sonner";
import Intelligence from "./routes/data/intelligence";

const NavbarLayout = () => {
  return (
    <>
      <Navbar />
      <Outlet /> 
    </>
  );
};
const App = () => {
  return (
    <BrowserRouter>
    <Toaster />
    {/* With Navbar */}
      <Routes>
        <Route element = {<NavbarLayout/>}>
        <Route path="/" element={<Dashboard />} />
        <Route path="/login" element={<SignIn />} />
        <Route path="/register" element={<SignUp />} />
        </Route>
      
      {/* No Navbar */}
      <Route path = "/predictions" element = {<Intelligence/>}/>
      </Routes>
    </BrowserRouter>
  );
};

export default App;
