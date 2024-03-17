// // src/App.tsx
// src/App.tsx
import React from "react";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import Home from "./pages/Home";
import { ChakraProvider } from "@chakra-ui/react";

const App: React.FC = () => {
  return (
    <ChakraProvider>
      
      <Router>
          <Routes>
            
            <Route path="/" element={<Home />} />
            {/* Add other routes here */}
          </Routes>
      </Router>
    </ChakraProvider>
  );
};

export default App;



// import React, { useState } from "react";
// import { useAction } from "convex/react";
// import { api } from "../convex/_generated/api";

// function App() {
//   const [question, setQuestion] = useState("");
//   const [answer, setAnswer] = useState("");
  
//   const sendTextToFlask = useAction(api.myFunctions.sendTextToFlask);

//   const handleSubmit = async (e: React.FormEvent) => {
//     e.preventDefault();
//     try {
//       // Call the action function to send the question to Flask API
//       const response = await sendTextToFlask({ text: question });
//       // Update state with the response from Flask API
//       setAnswer(response.answer);
//     } catch (error) {
//       console.error("Error sending text to Flask API:", error);
//       // Handle error if necessary
//     }
//   };

//   return (
//     <div className="App">
//       <form onSubmit={handleSubmit}>
//         <input 
//           type="text" 
//           placeholder="Enter your question" 
//           value={question} 
//           onChange={(e) => setQuestion(e.target.value)} 
//         />
//         <button type="submit">Submit</button>
//       </form>
//       {answer && <div>{answer}</div>}
//     </div>
//   );
// }

// export default App;
