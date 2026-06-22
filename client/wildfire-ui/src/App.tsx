import { BrowserRouter, Routes, Route } from "react-router-dom";
import SignIn from "./routes/auth/log/signin";
import SignUp from "./routes/auth/log/signup";
import Navbar from "./routes/constants/navbar";
import Dashboard from "./routes/home/dashboard";
import { Toaster } from "sonner";

const App = () => {
  return (
    <BrowserRouter>
      <Navbar />
      <Toaster/>
      <Routes>
        <Route path="/" element={<Dashboard />} />
        <Route path="/login" element={<SignIn />} />
        <Route path="/register" element={<SignUp />} />
      </Routes>
    </BrowserRouter>
  );
};

export default App;
